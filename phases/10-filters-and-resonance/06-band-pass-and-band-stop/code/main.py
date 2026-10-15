import math

import numpy as np

from sim import Circuit

FREQS = np.logspace(0, 6, 3001)


def band_edges(freqs, gain_db, drop=3.0103):
    peak = int(np.argmax(gain_db))
    target = gain_db[peak] - drop
    below = np.where(gain_db[:peak] <= target)[0]
    above = np.where(gain_db[peak:] <= target)[0]
    low = freqs[below[-1]] if len(below) else math.nan
    high = freqs[peak + above[0]] if len(above) else math.nan
    return low, freqs[peak], high


def voice_band_pass(f_low, f_high):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    r = 10e3
    c.capacitor("C1", "in", "hp", 1 / (2 * math.pi * f_low * r))
    c.resistor("R1", "hp", "0", r)
    c.vcvs("E1", "buf", "0", "hp", "0", 1.0)
    c.resistor("R2", "buf", "out", r)
    c.capacitor("C2", "out", "0", 1 / (2 * math.pi * f_high * r))
    return c


def rlc_band_pass():
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    c.inductor("L1", "in", "a", 10e-3)
    c.capacitor("C1", "a", "out", 1e-6)
    c.resistor("R1", "out", "0", 10.0)
    return c


def lc_notch(capacitance=10e-6, inductance=1.0, winding=10.0):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=50.0)
    c.resistor("R1", "in", "out", 1000.0)
    c.capacitor("C1", "out", "m", capacitance)
    c.inductor("L1", "m", "w", inductance)
    c.resistor("Rw", "w", "0", winding)
    return c


def twin_t_notch(f_notch, capacitance=100e-9):
    r = 1 / (2 * math.pi * f_notch * capacitance)
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=50.0)
    c.resistor("Ra", "in", "x", r)
    c.resistor("Rb", "x", "out", r)
    c.capacitor("C2x", "x", "0", 2 * capacitance)
    c.capacitor("Ca", "in", "y", capacitance)
    c.capacitor("Cb", "y", "out", capacitance)
    c.resistor("Rhalf", "y", "0", r / 2)
    return c, r


def amplitude_at(signal, t, freq):
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), t[1] - t[0])
    return 2 * np.abs(spectrum[np.argmin(np.abs(freqs - freq))]) / len(signal)


def hum_removal():
    c = Circuit()
    c.sine_source("Vmusic", "in", "m0", amplitude=1.0, freq=440.0)
    c.sine_source("Vhum", "m0", "0", amplitude=1.0, freq=50.0)
    c.resistor("R1", "in", "out", 1000.0)
    c.capacitor("C1", "out", "m", 10.13e-6)
    c.inductor("L1", "m", "w", 1.0)
    c.resistor("Rw", "w", "0", 10.0)
    run = c.transient(t_stop=1.0, dt=20e-6)
    t = np.asarray(run.time)
    keep = t >= 0.8
    keep[-1] = False
    return t[keep], np.asarray(run.v("in"))[keep], np.asarray(run.v("out"))[keep]


def main():
    print("=== Step 1: A telephone-style band-pass, 300 Hz to 3.4 kHz (high-pass, buffer, low-pass) ===")
    sweep = voice_band_pass(300.0, 3400.0).ac(FREQS, source="V1")
    low, centre, high = band_edges(FREQS, sweep.gain_db("out"))
    print(f"  -3 dB edges: {low:.0f} Hz and {high:.0f} Hz, peak near {centre:.0f} Hz, bandwidth {high - low:.0f} Hz")
    for f in [50, 300, 1000, 3400, 20000]:
        print(f"  {f:>6} Hz: {sweep.gain_db_at(f, 'out'):+7.2f} dB")

    print("\n=== Step 2: The series RLC band-pass from Lesson 05 ===")
    rlc = rlc_band_pass().ac(FREQS, source="V1")
    low, centre, high = band_edges(FREQS, rlc.gain_db("out"))
    print(f"  centre {centre:.0f} Hz, -3 dB edges {low:.0f} Hz and {high:.0f} Hz, bandwidth {high - low:.0f} Hz")
    print(f"  centre / bandwidth = {centre / (high - low):.1f} (Lesson 07 calls this Q)")

    print("\n=== Step 3: A series LC to ground makes a notch (band-stop) ===")
    f_notch = 1 / (2 * math.pi * math.sqrt(1.0 * 10e-6))
    notch = lc_notch().ac(FREQS, source="V1")
    print(f"  L = 1 H, C = 10 uF -> notch at {f_notch:.2f} Hz")
    for f in [25, 50, f_notch, 100, 440, 1000]:
        print(f"  {f:>7.2f} Hz: {notch.gain_db_at(f, 'out'):+7.2f} dB")
    print(f"  deepest point of the sweep: {notch.gain_db('out').min():.1f} dB at {FREQS[np.argmin(notch.gain_db('out'))]:.2f} Hz")
    print(f"  depth limited by the winding: 20 log10(10 / 1010) = {20 * math.log10(10 / 1010):.1f} dB")

    print("\n=== Step 4: The twin-T notch uses only R and C ===")
    twin, r = twin_t_notch(50.0)
    tt = twin.ac(FREQS, source="V1")
    print(f"  C = 100 nF, R = 1 / (2 pi f C) = {r:.0f} ohm, R/2 = {r / 2:.0f} ohm, 2C = 200 nF")
    for f in [10, 25, 50, 100, 250, 1000]:
        print(f"  {f:>5} Hz: {tt.gain_db_at(f, 'out'):+7.2f} dB")
    print(f"  deepest point of the sweep: {tt.gain_db('out').min():.1f} dB at {FREQS[np.argmin(tt.gain_db('out'))]:.2f} Hz")

    print("\n=== Step 5: Removing 50 Hz hum from a 440 Hz note (time simulation) ===")
    t, v_in, v_out = hum_removal()
    for f, name in [(50.0, "hum"), (440.0, "note")]:
        before, after = amplitude_at(v_in, t, f), amplitude_at(v_out, t, f)
        print(f"  {name:<4} {f:5.0f} Hz: before {before:.3f} V, after {after:.4f} V ({20 * math.log10(after / before):+.1f} dB)")


if __name__ == "__main__":
    main()
