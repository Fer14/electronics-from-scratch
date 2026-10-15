from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

CLOCK_HZ = 16_000_000
VDD = 5.0


class PwmTimer:
    def __init__(self, prescaler, top=255):
        self.prescaler = prescaler
        self.top = top
        self.counter = 0
        self.compare = 0

    def write_compare(self, value):
        self.compare = max(0, min(self.top + 1, value))

    def tick(self):
        output = 1 if self.counter < self.compare else 0
        self.counter = 0 if self.counter == self.top else self.counter + 1
        return output

    @property
    def period_seconds(self):
        return self.prescaler * (self.top + 1) / CLOCK_HZ

    @property
    def frequency_hz(self):
        return 1.0 / self.period_seconds

    @property
    def duty(self):
        return self.compare / (self.top + 1)


def pin_waveform(timer, periods):
    return np.array([timer.tick() for _ in range(periods * (timer.top + 1))]) * VDD


def filter_pwm(timer, ohms, farads, t_stop, dt):
    circuit = Circuit()
    circuit.pulse_source("PWM", "pwm", "0", low=0.0, high=VDD, period=timer.period_seconds, duty=timer.duty)
    circuit.resistor("R1", "pwm", "out", ohms)
    circuit.capacitor("C1", "out", "0", farads, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=dt)
    return np.asarray(result.time), np.asarray(result.v("out")), np.asarray(result.v("pwm"))


def last_periods(time, values, period, count):
    mask = time >= time[-1] - count * period
    return values[mask]


def predicted_ripple(duty, period, tau):
    return VDD * duty * (1 - duty) * period / tau


def main():
    timer = PwmTimer(prescaler=64)
    print(f"Timer: {CLOCK_HZ / 1e6:.0f} MHz clock / prescaler {timer.prescaler} / {timer.top + 1} counts")
    print(f"  PWM period = {timer.period_seconds * 1e3:.3f} ms, frequency = {timer.frequency_hz:.2f} Hz")

    print("\nThe pin, tick by tick, for one period (compare = 64): first and last ticks of each level")
    timer.write_compare(64)
    wave = pin_waveform(timer, 1)
    edges = np.flatnonzero(np.diff(wave)) + 1
    print(f"  high for ticks 0..{edges[0] - 1}, low for ticks {edges[0]}..{len(wave) - 1}")
    print(f"  average of the pin over the period = {wave.mean():.4f} V  (duty {timer.duty:.4f} x {VDD} V = {timer.duty * VDD:.4f} V)")

    ohms, farads = 10_000, 1e-6
    tau = ohms * farads
    t_stop, dt = 0.08, 2e-6
    print(f"\nPWM into an RC low-pass: R = {ohms / 1e3:.0f} kohm, C = {farads * 1e6:.0f} uF, tau = RC = {tau * 1e3:.0f} ms")
    print(f"  {'compare':>7s} {'duty':>6s} {'target V':>8s} {'mean out':>8s} {'ripple p-p':>10s} {'predicted':>9s}")
    plot_data = {}
    for compare in [32, 64, 128, 192]:
        timer.write_compare(compare)
        time, out, pwm = filter_pwm(timer, ohms, farads, t_stop, dt)
        tail = last_periods(time, out, timer.period_seconds, 5)
        print(f"  {compare:7d} {timer.duty:6.3f} {timer.duty * VDD:8.3f} {tail.mean():8.3f} "
              f"{(tail.max() - tail.min()) * 1e3:8.1f} mV {predicted_ripple(timer.duty, timer.period_seconds, tau) * 1e3:7.1f} mV")
        plot_data[compare] = (time, out, pwm)

    print("\nThe filter trade-off at duty 0.5: small RC ripples, big RC is slow")
    print(f"  {'tau':>7s} {'ripple p-p':>10s} {'time to 95% (3 tau)':>20s}")
    timer.write_compare(128)
    for tau_choice in [1e-3, 1e-2, 1e-1]:
        print(f"  {tau_choice * 1e3:5.0f} ms {predicted_ripple(0.5, timer.period_seconds, tau_choice) * 1e3:8.1f} mV "
              f"{3 * tau_choice * 1e3:16.0f} ms")

    time, out, pwm = plot_data[64]
    figure, axis = plt.subplots(figsize=(9, 4))
    axis.plot(time * 1e3, pwm, color="#bbbbbb", linewidth=0.6, label="pin (PWM, duty 0.25)")
    axis.plot(time * 1e3, out, color="#8a5a2b", linewidth=1.5, label="after the RC filter")
    axis.axhline(0.25 * VDD, color="black", linestyle="--", linewidth=0.8, label="duty x VDD")
    axis.set_xlabel("time (ms)")
    axis.set_ylabel("volts")
    axis.legend(loc="upper right")
    figure.tight_layout()
    path = Path(__file__).parent / "pwm_rc.png"
    figure.savefig(path, dpi=120)
    print(f"\nSaved {path.name}")


if __name__ == "__main__":
    main()
