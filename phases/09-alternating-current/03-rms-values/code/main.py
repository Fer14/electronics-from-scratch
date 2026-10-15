import math

import numpy as np

from sim import Circuit

SAMPLES_PER_PERIOD = 100_000


def one_period(freq):
    return np.arange(SAMPLES_PER_PERIOD) / (SAMPLES_PER_PERIOD * freq)


def mean(values):
    return float(np.mean(values))


def rms(values):
    return math.sqrt(mean(np.square(values)))


def waveforms(peak, freq):
    t = one_period(freq)
    phase = (t * freq) % 1.0
    s = np.sin(2 * np.pi * freq * t)
    return {
        "sine": peak * s,
        "square": np.where(phase < 0.5, peak, -peak),
        "triangle": peak * (1 - 4 * np.abs(phase - 0.5)),
        "half-wave rectified sine": peak * np.maximum(s, 0),
        "full-wave rectified sine": peak * np.abs(s),
        "sine on a DC offset of peak/2": peak / 2 + peak * s,
        "PWM 0 to peak, 25% duty": np.where(phase < 0.25, peak, 0.0),
    }


def average_power(time, volts, amps, freq, cycles):
    keep = time >= time[-1] - cycles / freq
    p = volts[keep] * amps[keep]
    return float(np.trapezoid(p, time[keep]) / (time[keep][-1] - time[keep][0]))


def main():
    print("=== Step 1: The plain average of a sine wave is useless ===")
    peak, freq = 325.27, 50.0
    v = peak * np.sin(2 * np.pi * freq * one_period(freq))
    print(f"  peak = {peak} V")
    print(f"  average of v over one period     = {mean(v):10.6f} V")
    print(f"  average of |v| (rectified mean)  = {mean(np.abs(v)):10.3f} V   (2/pi x peak = {2 / math.pi * peak:.3f} V)")

    print("\n=== Step 2: Root of the mean of the square ===")
    print(f"  mean of v^2       = {mean(v**2):10.1f} V^2")
    print(f"  square root (RMS) = {rms(v):10.3f} V   (peak / sqrt(2) = {peak / math.sqrt(2):.3f} V)")

    print("\n=== Step 3: A 1000 W kettle on 230 V mains ===")
    resistance = 230.0**2 / 1000.0
    p = v**2 / resistance
    print(f"  heater resistance = 230^2 / 1000 = {resistance:.2f} ohm")
    print(f"  instantaneous power swings from {p.min():.1f} W to {p.max():.1f} W")
    print(f"  average power     = {mean(p):.1f} W   (230^2 / R = {230.0**2 / resistance:.1f} W)")

    print("\n=== Step 4: RMS of other waveforms (peak = 1 V) ===")
    for name, wave in waveforms(1.0, 1.0).items():
        print(f"  {name:<32} average {mean(wave):7.4f} V   RMS {rms(wave):7.4f} V")

    print("\n=== Step 5: Simulated heater: AC sine vs equivalent DC ===")
    amplitude, heater = 10.0, 50.0
    ac = Circuit()
    ac.sine_source("V1", "a", "0", amplitude=amplitude, freq=freq)
    ac.resistor("Rheater", "a", "0", heater)
    t = ac.transient(t_stop=0.04, dt=1e-5)
    p_ac = average_power(t.time, t.v("a"), t.i("Rheater"), freq, cycles=2)
    dc = Circuit()
    dc.voltage_source("B1", "a", "0", amplitude / math.sqrt(2))
    dc.resistor("Rheater", "a", "0", heater)
    p_dc = dc.dc().p("Rheater")
    print(f"  AC: {amplitude:.0f} V peak sine into {heater:.0f} ohm, average power = {p_ac:.4f} W")
    print(f"  DC: {amplitude / math.sqrt(2):.4f} V battery into {heater:.0f} ohm, power        = {p_dc:.4f} W")
    print(f"  DC at the peak value {amplitude:.0f} V would give {amplitude**2 / heater:.2f} W (twice too much)")

    print("\n=== Step 6: Mains numbers ===")
    for v_rms, hz in ((230.0, 50), (120.0, 60), (100.0, 50)):
        v_peak = v_rms * math.sqrt(2)
        print(f"  {v_rms:5.0f} V RMS, {hz} Hz -> peak {v_peak:6.1f} V, peak-to-peak {2 * v_peak:6.1f} V")


if __name__ == "__main__":
    main()
