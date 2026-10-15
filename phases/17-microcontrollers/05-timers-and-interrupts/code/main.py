import numpy as np

from sim import Circuit

VDD = 3.3
VIH = 0.6 * VDD


class CompareTimer:
    def __init__(self, prescaler, compare):
        self.prescaler = prescaler
        self.compare = compare
        self.prescale_count = 0
        self.counter = 0
        self.flag = False
        self.flag_set_at = None
        self.matches = 0

    def clock(self, now):
        self.prescale_count += 1
        if self.prescale_count < self.prescaler:
            return
        self.prescale_count = 0
        if self.counter == self.compare:
            self.counter = 0
            self.matches += 1
            if not self.flag:
                self.flag_set_at = now
            self.flag = True
        else:
            self.counter += 1


class Mcu:
    ISR_ENTRY_CYCLES = 4
    ISR_BODY_CYCLES = 10
    ISR_EXIT_CYCLES = 4

    def __init__(self, timer, use_interrupts, work_chunk_cycles):
        self.timer = timer
        self.use_interrupts = use_interrupts
        self.work_chunk_cycles = work_chunk_cycles
        self.now = 0
        self.ticks_counted = 0
        self.latencies = []
        self.work_done = 0

    def burn(self, cycles):
        for _ in range(cycles):
            self.timer.clock(self.now)
            self.now += 1

    def handle_tick(self):
        self.latencies.append(self.now - self.timer.flag_set_at)
        self.timer.flag = False
        self.ticks_counted += 1

    def run(self, total_cycles):
        while self.now < total_cycles:
            if self.use_interrupts:
                for _ in range(self.work_chunk_cycles):
                    if self.timer.flag:
                        self.burn(self.ISR_ENTRY_CYCLES)
                        self.handle_tick()
                        self.burn(self.ISR_BODY_CYCLES + self.ISR_EXIT_CYCLES)
                    self.burn(1)
                    self.work_done += 1
            else:
                self.burn(self.work_chunk_cycles)
                self.work_done += self.work_chunk_cycles
                if self.timer.flag:
                    self.handle_tick()
                    self.burn(self.ISR_BODY_CYCLES)


def compare_value(clock_hz, prescaler, interrupt_hz):
    return clock_hz / (prescaler * interrupt_hz) - 1


def bouncy_button(duration_ms, press_at_ms, sample_us=50):
    generator = np.random.default_rng(7)
    times = np.arange(0, duration_ms * 1000, sample_us) / 1000
    level = np.ones_like(times)
    level[times >= press_at_ms] = 0
    bounce_end = press_at_ms + 3.0
    bouncing = (times >= press_at_ms) & (times < bounce_end)
    level[bouncing] = generator.integers(0, 2, bouncing.sum())
    return times, level


def count_edges(levels):
    return int(np.sum(np.diff(levels) < 0))


def software_debounce(times, levels, period_ms=1.0, needed=5):
    stable_level, candidate, run_length = 1, 1, 0
    presses = []
    next_sample = 0.0
    for time, level in zip(times, levels):
        if time < next_sample:
            continue
        next_sample += period_ms
        if level == candidate:
            run_length += 1
        else:
            candidate, run_length = level, 1
        if run_length >= needed and candidate != stable_level:
            stable_level = candidate
            if stable_level == 0:
                presses.append(time)
    return presses


def rc_debounce_time(pull_up_ohms, farads):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RPU", "vdd", "pin", pull_up_ohms)
    circuit.capacitor("C1", "pin", "0", farads, v0=0.0)
    tau = pull_up_ohms * farads
    result = circuit.transient(t_stop=4 * tau, dt=tau / 1000)
    time, volts = np.asarray(result.time), np.asarray(result.v("pin"))
    return float(np.interp(VIH, volts, time)), tau


def main():
    clock_hz = 16_000_000
    print(f"Choosing prescaler and compare for a {clock_hz / 1e6:.0f} MHz clock")
    print(f"  {'want':>8s} {'prescaler':>9s} {'compare':>10s} {'fits 16 bits?':>13s} {'actual':>10s}")
    for interrupt_hz in [1.0, 1000.0]:
        for prescaler in [1, 8, 64, 256, 1024]:
            exact = compare_value(clock_hz, prescaler, interrupt_hz)
            rounded = round(exact)
            fits = 0 <= rounded <= 65535
            actual = clock_hz / (prescaler * (rounded + 1))
            print(f"  {interrupt_hz:6.0f} Hz {prescaler:9d} {exact:10.2f} {'yes' if fits else 'no':>13s} {actual:8.4f} Hz")

    slow_clock = 1_000_000
    total_cycles = 50_000
    print(f"\nA 1 ms tick at {slow_clock / 1e6:.0f} MHz (prescaler 1, compare 999), main loop busy in chunks of 2500 cycles,"
          f" {total_cycles / slow_clock * 1e3:.0f} ms of run time")
    for use_interrupts in [False, True]:
        timer = CompareTimer(prescaler=1, compare=999)
        mcu = Mcu(timer, use_interrupts, work_chunk_cycles=2500)
        mcu.run(total_cycles)
        latencies = np.array(mcu.latencies)
        print(f"  {'interrupts' if use_interrupts else 'polling   '}: timer matched {timer.matches} times, "
              f"program counted {mcu.ticks_counted}, latency avg {latencies.mean():7.1f} max {latencies.max():5d} cycles "
              f"({latencies.max() / slow_clock * 1e6:.0f} us)")

    print("\nA bouncing button (pressed at 10 ms, contacts bounce for 3 ms), read every 50 us")
    times, levels = bouncy_button(duration_ms=40, press_at_ms=10.0)
    print(f"  raw falling edges seen: {count_edges(levels)}")
    presses = software_debounce(times, levels)
    print(f"  1 ms timer interrupt, 5 equal samples in a row: {len(presses)} press, accepted at t = {presses[0]:.2f} ms")

    print("\nHardware debounce: pull-up charging a capacitor after the button is released")
    print(f"  the pin reads 1 once it passes VIH = {VIH:.2f} V; theory: t = RC x ln(VDD / (VDD - VIH)) = {np.log(1 / 0.4):.3f} RC")
    for farads in [100e-9, 1e-6, 10e-6]:
        crossing, tau = rc_debounce_time(10_000, farads)
        print(f"  10 kohm, {farads * 1e6:5.1f} uF: tau = {tau * 1e3:6.2f} ms, crosses VIH at {crossing * 1e3:7.2f} ms "
              f"(theory {0.9163 * tau * 1e3:7.2f} ms)")


if __name__ == "__main__":
    main()
