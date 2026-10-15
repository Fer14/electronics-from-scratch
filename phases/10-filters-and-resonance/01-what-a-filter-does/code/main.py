import numpy as np

from sim import Circuit

R = 1000.0
C = 100e-9
TONE = 200.0
HISS = 5000.0


def cutoff_frequency(resistance, capacitance):
    return 1 / (2 * np.pi * resistance * capacitance)


def low_pass_gain(freq, fc):
    return 1 / np.sqrt(1 + (freq / fc) ** 2)


def high_pass_gain(freq, fc):
    return (freq / fc) / np.sqrt(1 + (freq / fc) ** 2)


def amplitude_at(signal, t, freq):
    n = len(signal)
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, t[1] - t[0])
    return 2 * np.abs(spectrum[np.argmin(np.abs(freqs - freq))]) / n


def two_tone_through(kind):
    c = Circuit()
    c.sine_source("Vtone", "in", "m", amplitude=1.0, freq=TONE)
    c.sine_source("Vhiss", "m", "0", amplitude=0.5, freq=HISS)
    if kind == "low-pass":
        c.resistor("R1", "in", "out", R)
        c.capacitor("C1", "out", "0", C)
    else:
        c.capacitor("C1", "in", "out", C)
        c.resistor("R1", "out", "0", R)
    run = c.transient(t_stop=20e-3, dt=2e-6)
    t = np.asarray(run.time)
    keep = t >= 10e-3
    keep[-1] = False
    return t[keep], np.asarray(run.v("in"))[keep], np.asarray(run.v("out"))[keep]


def square_wave_harmonics(fundamental, count):
    return [(n * fundamental, 4 / (np.pi * n)) for n in range(1, 2 * count, 2)]


def ac_gain_low_pass(freqs):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    c.resistor("R1", "in", "out", R)
    c.capacitor("C1", "out", "0", C)
    return c.ac(freqs, source="V1").gain("out")


def main():
    fc = cutoff_frequency(R, C)
    print("=== Step 1: Our RC filter ===")
    print(f"  R = {R:.0f} ohm, C = {C * 1e9:.0f} nF -> cutoff fc = 1 / (2 pi R C) = {fc:.1f} Hz")

    for kind, formula in [("low-pass", low_pass_gain), ("high-pass", high_pass_gain)]:
        print(f"\n=== Step 2: A {TONE:.0f} Hz tone plus {HISS:.0f} Hz hiss through the {kind} (simulator) ===")
        t, v_in, v_out = two_tone_through(kind)
        for freq in [TONE, HISS]:
            a_in = amplitude_at(v_in, t, freq)
            a_out = amplitude_at(v_out, t, freq)
            print(f"  {freq:>6.0f} Hz: in {a_in:.3f} V, out {a_out:.3f} V, ratio {a_out / a_in:.3f} "
                  f"(formula {formula(freq, fc):.3f})")

    print("\n=== Step 3: A 100 Hz square wave is a sum of sines, and the low-pass trims the high ones ===")
    for freq, amplitude in square_wave_harmonics(100.0, 6):
        kept = amplitude * low_pass_gain(freq, fc)
        print(f"  harmonic {freq:>6.0f} Hz: amplitude {amplitude:.3f} V -> after the filter {kept:.3f} V "
              f"({low_pass_gain(freq, fc) * 100:5.1f} % kept)")

    print("\n=== Step 4: The filter's gain at any frequency (simulator AC analysis) ===")
    freqs = np.array([10, 100, 1000, fc, 10000, 100000])
    gains = ac_gain_low_pass(freqs)
    for freq, gain in zip(freqs, gains):
        print(f"  {freq:>9.1f} Hz: gain {gain:.4f} (formula {low_pass_gain(freq, fc):.4f})")


if __name__ == "__main__":
    main()
