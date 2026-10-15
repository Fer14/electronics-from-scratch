from sim import Circuit

CLOCK_HZ = 16_000_000
SUPPLY_VOLTS = 3.3
LED_RESISTOR_OHMS = 330

PROGRAM = """
        ldi r0, 5
        ldi r1, 1
countdown:
        out PORTB, r1
        ldi r2, 0
        out PORTB, r2
        dec r0
        brne countdown
        ldi r3, 42
        st 0x10, r3
        ld r4, 0x10
        halt
"""

IO_ADDRESSES = {"PORTB": 0x05}
CYCLE_COST = {"ldi": 1, "mov": 1, "add": 1, "sub": 1, "inc": 1, "dec": 1, "out": 1, "in": 1,
              "st": 2, "ld": 2, "jmp": 2, "brne": 1, "breq": 1, "halt": 1, "nop": 1}


def assemble(source):
    labels = {}
    instructions = []
    for raw_line in source.strip().splitlines():
        text = raw_line.strip()
        if not text:
            continue
        if text.endswith(":"):
            labels[text[:-1]] = len(instructions)
            continue
        mnemonic, _, rest = text.partition(" ")
        operands = [part.strip() for part in rest.split(",") if part.strip()]
        instructions.append((mnemonic.lower(), operands))
    return [(mnemonic, [labels.get(operand, operand) for operand in operands])
            for mnemonic, operands in instructions]


class TinyCore:
    def __init__(self, program, ram_size=64):
        self.program = program
        self.registers = [0] * 8
        self.ram = [0] * ram_size
        self.io = {address: 0 for address in IO_ADDRESSES.values()}
        self.pc = 0
        self.zero_flag = False
        self.cycles = 0
        self.halted = False
        self.io_writes = []

    def register_index(self, token):
        return int(token[1:])

    def number(self, token):
        if isinstance(token, int):
            return token
        if token in IO_ADDRESSES:
            return IO_ADDRESSES[token]
        return int(token, 0)

    def set_register(self, index, value):
        self.registers[index] = value & 0xFF
        self.zero_flag = self.registers[index] == 0

    def step(self):
        mnemonic, operands = self.program[self.pc]
        next_pc = self.pc + 1
        cost = CYCLE_COST[mnemonic]
        if mnemonic == "ldi":
            self.registers[self.register_index(operands[0])] = self.number(operands[1]) & 0xFF
        elif mnemonic == "mov":
            self.registers[self.register_index(operands[0])] = self.registers[self.register_index(operands[1])]
        elif mnemonic == "add":
            destination = self.register_index(operands[0])
            self.set_register(destination, self.registers[destination] + self.registers[self.register_index(operands[1])])
        elif mnemonic == "sub":
            destination = self.register_index(operands[0])
            self.set_register(destination, self.registers[destination] - self.registers[self.register_index(operands[1])])
        elif mnemonic == "inc":
            destination = self.register_index(operands[0])
            self.set_register(destination, self.registers[destination] + 1)
        elif mnemonic == "dec":
            destination = self.register_index(operands[0])
            self.set_register(destination, self.registers[destination] - 1)
        elif mnemonic == "out":
            address = self.number(operands[0])
            self.io[address] = self.registers[self.register_index(operands[1])]
            self.io_writes.append((self.cycles, address, self.io[address]))
        elif mnemonic == "in":
            self.registers[self.register_index(operands[0])] = self.io[self.number(operands[1])]
        elif mnemonic == "st":
            self.ram[self.number(operands[0])] = self.registers[self.register_index(operands[1])]
        elif mnemonic == "ld":
            self.registers[self.register_index(operands[0])] = self.ram[self.number(operands[1])]
        elif mnemonic == "jmp":
            next_pc = operands[0]
        elif mnemonic == "brne":
            if not self.zero_flag:
                next_pc = operands[0]
                cost += 1
        elif mnemonic == "breq":
            if self.zero_flag:
                next_pc = operands[0]
                cost += 1
        elif mnemonic == "halt":
            self.halted = True
            next_pc = self.pc
        self.cycles += cost
        self.pc = next_pc
        return mnemonic, operands

    def run(self, max_steps=1000):
        trace = []
        while not self.halted and len(trace) < max_steps:
            pc_before = self.pc
            mnemonic, operands = self.step()
            trace.append((self.cycles, pc_before, mnemonic, operands, list(self.registers[:5])))
        return trace


def led_current_for_pin(pin_volts):
    circuit = Circuit()
    circuit.voltage_source("PIN", "pin", "0", pin_volts)
    circuit.resistor("R1", "pin", "a", LED_RESISTOR_OHMS)
    circuit.led("D1", "a", "0", color="red")
    return circuit.dc().i("D1")


def main():
    program = assemble(PROGRAM)
    print("The program after assembly (address: instruction)")
    for address, (mnemonic, operands) in enumerate(program):
        print(f"  {address:2d}: {mnemonic:5s} {', '.join(str(operand) for operand in operands)}")

    core = TinyCore(program)
    trace = core.run()
    print("\nFetch-decode-execute trace (cycles counted at the end of each instruction)")
    print(f"  {'cycle':>5s} {'pc':>3s}  {'instruction':18s} r0  r1  r2  r3  r4")
    for cycles, pc, mnemonic, operands, registers in trace:
        text = f"{mnemonic} {', '.join(str(operand) for operand in operands)}"
        print(f"  {cycles:5d} {pc:3d}  {text:18s} " + "  ".join(f"{value:<2d}" for value in registers))

    print(f"\nInstructions executed: {len(trace)}")
    print(f"Clock cycles used:     {core.cycles}")
    print(f"Time at {CLOCK_HZ / 1e6:.0f} MHz:        {core.cycles / CLOCK_HZ * 1e6:.3f} us")
    print(f"RAM[0x10] = {core.ram[0x10]}, read back into r4 = {core.registers[4]}")

    print(f"\nWhat the outside world sees on PORTB bit 0 (LED with {LED_RESISTOR_OHMS} ohm from a {SUPPLY_VOLTS} V pin)")
    current_on = led_current_for_pin(SUPPLY_VOLTS)
    current_off = led_current_for_pin(0.0)
    for cycle, address, value in core.io_writes:
        pin_high = value & 1
        current = current_on if pin_high else current_off
        print(f"  t = {cycle / CLOCK_HZ * 1e9:7.1f} ns  PORTB = {value:08b}  pin = {SUPPLY_VOLTS if pin_high else 0.0:.1f} V  "
              f"LED current = {current * 1e3:6.3f} mA")
    pulses = sum(1 for _, _, value in core.io_writes if value & 1)
    print(f"\nThe LED flashed {pulses} times, each flash lasting {CYCLE_COST['ldi'] + CYCLE_COST['out']} cycles = "
          f"{(CYCLE_COST['ldi'] + CYCLE_COST['out']) / CLOCK_HZ * 1e9:.1f} ns: far too fast for an eye to see.")


if __name__ == "__main__":
    main()
