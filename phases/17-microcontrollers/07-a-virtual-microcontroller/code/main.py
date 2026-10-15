from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

CLOCK_HZ = 1_000_000
VDD = 3.3
ADC_BITS = 8
PWM_PRESCALER = 8
TIMER_PRESCALER = 64
FIXED_OHMS = 4_700
SCENE_SECONDS = 0.25
SCENES_LUX = [1000, 100, 10, 1]

FIRMWARE = """
.vector timer, tick
reset:
        ldi r0, 0b00000010
        out DDRB, r0
        ldi r0, 155
        out TCOMP, r0
        ldi r0, 1
        out TCTRL, r0
        sei
idle:
        sleep
        jmp idle
tick:
        out ADCSTART, r0
        in r1, ADCH
        cpi r1, 200
        brsh daylight
        ldi r2, 255
        sub r2, r1
        jmp apply
daylight:
        ldi r2, 0
apply:
        out PWMDUTY, r2
        inc r3
        cpi r3, 25
        brne done
        ldi r3, 0
        out UDR, r1
        out UDR, r2
done:
        reti
"""

IO = {"PINB": 0x03, "DDRB": 0x04, "PORTB": 0x05, "TCTRL": 0x10, "TCOMP": 0x11,
      "ADCSTART": 0x20, "ADCH": 0x21, "PWMDUTY": 0x30, "UDR": 0x40}
CYCLES = {"ldi": 1, "mov": 1, "add": 1, "sub": 1, "inc": 1, "dec": 1, "cpi": 1, "out": 1, "in": 1,
          "jmp": 2, "breq": 1, "brne": 1, "brlo": 1, "brsh": 1, "sei": 1, "cli": 1, "sleep": 1, "reti": 4, "nop": 1}
INTERRUPT_ENTRY_CYCLES = 4


def assemble(source):
    labels, vectors, instructions = {}, {}, []
    for raw_line in source.strip().splitlines():
        text = raw_line.strip()
        if not text:
            continue
        if text.startswith(".vector"):
            name, label = [part.strip() for part in text[len(".vector"):].split(",")]
            vectors[name] = label
            continue
        if text.endswith(":"):
            labels[text[:-1]] = len(instructions)
            continue
        mnemonic, _, rest = text.partition(" ")
        instructions.append((mnemonic, [part.strip() for part in rest.split(",") if part.strip()]))
    program = [(mnemonic, [labels.get(operand, operand) for operand in operands]) for mnemonic, operands in instructions]
    return program, {name: labels[label] for name, label in vectors.items()}


def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7


class LightWorld:
    def __init__(self, scenes_lux, scene_seconds):
        self.scenes_lux = scenes_lux
        self.scene_seconds = scene_seconds
        self.cache = {}

    def lux_at(self, seconds):
        index = min(int(seconds / self.scene_seconds), len(self.scenes_lux) - 1)
        return self.scenes_lux[index]

    def sensor_volts(self, seconds):
        lux = self.lux_at(seconds)
        if lux not in self.cache:
            circuit = Circuit()
            circuit.voltage_source("VDD", "vdd", "0", VDD)
            circuit.resistor("RLDR", "vdd", "sense", ldr_ohms(lux))
            circuit.resistor("RFIX", "sense", "0", FIXED_OHMS)
            self.cache[lux] = circuit.dc().v("sense")
        return self.cache[lux]


class Timer:
    def __init__(self):
        self.enabled = False
        self.compare = 255
        self.next_match = None

    @property
    def period_cycles(self):
        return TIMER_PRESCALER * (self.compare + 1)

    def start(self, now):
        self.enabled = True
        self.next_match = now + self.period_cycles


class VirtualMcu:
    def __init__(self, source, world):
        self.program, self.vectors = assemble(source)
        self.world = world
        self.registers = [0] * 16
        self.zero = False
        self.carry = False
        self.interrupts_enabled = False
        self.sleeping = False
        self.stack = []
        self.pc = 0
        self.now = 0
        self.busy_cycles = 0
        self.pending = set()
        self.timer = Timer()
        self.io = {address: 0 for address in IO.values()}
        self.adc_result = 0
        self.pwm_log = []
        self.uart_log = []
        self.adc_log = []
        self.interrupts_served = 0

    def seconds(self):
        return self.now / CLOCK_HZ

    def reg(self, token):
        return int(token[1:])

    def value(self, token):
        if isinstance(token, int):
            return token
        if token in IO:
            return IO[token]
        return int(token, 0)

    def set_result(self, index, raw):
        self.carry = raw < 0 or raw > 0xFF
        self.registers[index] = raw & 0xFF
        self.zero = self.registers[index] == 0

    def io_write(self, address, data):
        self.io[address] = data
        if address == IO["TCOMP"]:
            self.timer.compare = data
        elif address == IO["TCTRL"] and data & 1:
            self.timer.start(self.now)
        elif address == IO["ADCSTART"]:
            volts = self.world.sensor_volts(self.seconds())
            self.adc_result = max(0, min(int(volts / VDD * 2 ** ADC_BITS), 2 ** ADC_BITS - 1))
            self.adc_log.append((self.seconds(), volts, self.adc_result))
        elif address == IO["PWMDUTY"]:
            self.pwm_log.append((self.seconds(), data, bool(self.io[IO["DDRB"]] & 0b10)))
        elif address == IO["UDR"]:
            self.uart_log.append((self.seconds(), data))

    def io_read(self, address):
        if address == IO["ADCH"]:
            return self.adc_result
        return self.io[address]

    def update_timer(self):
        while self.timer.enabled and self.now >= self.timer.next_match:
            self.pending.add("timer")
            self.timer.next_match += self.timer.period_cycles

    def execute(self):
        mnemonic, operands = self.program[self.pc]
        next_pc = self.pc + 1
        cost = CYCLES[mnemonic]
        branch = None
        if mnemonic == "ldi":
            self.registers[self.reg(operands[0])] = self.value(operands[1]) & 0xFF
        elif mnemonic == "mov":
            self.registers[self.reg(operands[0])] = self.registers[self.reg(operands[1])]
        elif mnemonic in ("add", "sub"):
            a, b = self.registers[self.reg(operands[0])], self.registers[self.reg(operands[1])]
            self.set_result(self.reg(operands[0]), a + b if mnemonic == "add" else a - b)
        elif mnemonic in ("inc", "dec"):
            index = self.reg(operands[0])
            self.set_result(index, self.registers[index] + (1 if mnemonic == "inc" else -1))
        elif mnemonic == "cpi":
            difference = self.registers[self.reg(operands[0])] - self.value(operands[1])
            self.zero = difference == 0
            self.carry = difference < 0
        elif mnemonic == "out":
            self.io_write(self.value(operands[0]), self.registers[self.reg(operands[1])])
        elif mnemonic == "in":
            self.registers[self.reg(operands[0])] = self.io_read(self.value(operands[1]))
        elif mnemonic == "jmp":
            next_pc = operands[0]
        elif mnemonic == "breq":
            branch = self.zero
        elif mnemonic == "brne":
            branch = not self.zero
        elif mnemonic == "brlo":
            branch = self.carry
        elif mnemonic == "brsh":
            branch = not self.carry
        elif mnemonic == "sei":
            self.interrupts_enabled = True
        elif mnemonic == "cli":
            self.interrupts_enabled = False
        elif mnemonic == "sleep":
            self.sleeping = True
        elif mnemonic == "reti":
            next_pc = self.stack.pop()
            self.interrupts_enabled = True
        if branch:
            next_pc = operands[0]
            cost += 1
        self.pc = next_pc
        self.now += cost
        self.busy_cycles += cost

    def serve_interrupt(self, name):
        self.pending.discard(name)
        self.stack.append(self.pc)
        self.interrupts_enabled = False
        self.sleeping = False
        self.pc = self.vectors[name]
        self.now += INTERRUPT_ENTRY_CYCLES
        self.busy_cycles += INTERRUPT_ENTRY_CYCLES
        self.interrupts_served += 1

    def run(self, seconds):
        stop = int(seconds * CLOCK_HZ)
        while self.now < stop:
            self.update_timer()
            if self.interrupts_enabled and self.pending:
                self.serve_interrupt(sorted(self.pending)[0])
                continue
            if self.sleeping:
                wake = self.timer.next_match if self.timer.enabled else stop
                self.now = max(self.now, min(wake, stop))
                continue
            self.execute()


def pwm_filtered_volts(duty_code):
    period = PWM_PRESCALER * 2 ** 8 / CLOCK_HZ
    circuit = Circuit()
    if duty_code == 0:
        circuit.voltage_source("PWM", "pwm", "0", 0.0)
    else:
        circuit.pulse_source("PWM", "pwm", "0", low=0.0, high=VDD, period=period, duty=duty_code / 256)
    circuit.resistor("R1", "pwm", "out", 10_000)
    circuit.capacitor("C1", "out", "0", 1e-6, v0=0.0)
    result = circuit.transient(t_stop=0.06, dt=4e-6)
    time, out = np.asarray(result.time), np.asarray(result.v("out"))
    return float(out[time >= 0.06 - 5 * period].mean())


def led_on_current():
    circuit = Circuit()
    circuit.voltage_source("PIN", "drv", "0", VDD)
    circuit.resistor("RDRV", "drv", "pb1", 40)
    circuit.resistor("R1", "pb1", "a", 150)
    circuit.led("D1", "a", "0", color="red")
    return circuit.dc().i("D1")


def main():
    world = LightWorld(SCENES_LUX, SCENE_SECONDS)
    mcu = VirtualMcu(FIRMWARE, world)
    print(f"Firmware: {len(mcu.program)} instructions, vectors {mcu.vectors}")
    tick_hz = CLOCK_HZ / (TIMER_PRESCALER * 156)
    pwm_hz = CLOCK_HZ / (PWM_PRESCALER * 256)
    print(f"Clock {CLOCK_HZ / 1e6:.0f} MHz, tick {tick_hz:.2f} Hz, PWM {pwm_hz:.1f} Hz, ADC {ADC_BITS} bits on {VDD} V")

    total_seconds = SCENE_SECONDS * len(SCENES_LUX)
    mcu.run(total_seconds)
    awake = mcu.busy_cycles / mcu.now
    print(f"Ran {total_seconds:.2f} s: {mcu.interrupts_served} timer interrupts, CPU awake {mcu.busy_cycles} of {mcu.now} "
          f"cycles ({awake * 100:.2f}%)")

    print("\nUART log (bytes sent every 25 ticks: light code, PWM duty)")
    for (time_a, light), (_, duty) in zip(mcu.uart_log[0::2], mcu.uart_log[1::2]):
        print(f"  t = {time_a:6.3f} s  light = {light:3d}  duty = {duty:3d}")

    led_current = led_on_current()
    print(f"\nWhat the circuits do in each scene (LED on-current {led_current * 1e3:.2f} mA through 150 ohm)")
    print(f"  {'lux':>5s} {'LDR':>9s} {'sensor V':>8s} {'ADC':>4s} {'duty':>5s} {'RC out':>7s} {'ideal':>6s} {'LED avg':>8s}")
    for index, lux in enumerate(SCENES_LUX):
        end = (index + 1) * SCENE_SECONDS
        samples = [entry for entry in mcu.adc_log if entry[0] < end]
        duties = [entry for entry in mcu.pwm_log if entry[0] < end]
        if not samples or not duties:
            print(f"  {lux:5d} {ldr_ohms(lux) / 1e3:7.2f} k  no ADC reading or PWM write yet: did the firmware run?")
            continue
        _, volts, code = samples[-1]
        _, duty, pin_is_output = duties[-1]
        filtered = pwm_filtered_volts(duty) if pin_is_output else float("nan")
        print(f"  {lux:5d} {ldr_ohms(lux) / 1e3:7.2f} k {volts:7.3f} V {code:4d} {duty:5d} {filtered:6.3f} V "
              f"{duty / 256 * VDD:5.3f} V {duty / 256 * led_current * 1e3:6.2f} mA")

    if not mcu.adc_log:
        return
    times = np.array([entry[0] for entry in mcu.adc_log])
    codes = np.array([entry[2] for entry in mcu.adc_log])
    duties = np.array([entry[1] for entry in mcu.pwm_log])
    figure, axis = plt.subplots(figsize=(9, 4))
    axis.step(times, codes, where="post", color="#bbbbbb", label="ADC light code")
    axis.step(times, duties, where="post", color="#8a5a2b", label="PWM duty code")
    axis.set_xlabel("time (s)")
    axis.set_ylabel("8-bit value")
    axis.legend(loc="center right")
    figure.tight_layout()
    path = Path(__file__).parent / "night_light.png"
    figure.savefig(path, dpi=120)
    print(f"\nSaved {path.name}")


if __name__ == "__main__":
    main()
