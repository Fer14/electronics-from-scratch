import numpy as np

from sim import Circuit


def sample(frequency, rate, seconds, phase=0.0, amplitude=1.0):
    n = np.arange(int(round(rate * seconds)))
    return amplitude * np.cos(2 * np.pi * frequency * n / rate + phase)


def strongest_frequency(samples, rate):
    spectrum = np.abs(np.fft.rfft(samples * np.hanning(len(samples))))
    freqs = np.fft.rfftfreq(len(samples), 1 / rate)
    return freqs[np.argmax(spectrum)]


def alias_of(frequency, rate):
    return abs(frequency - rate * round(frequency / rate))


def sinc_reconstruct(samples, rate, times):
    n = np.arange(len(samples))
    return np.array([np.sum(samples * np.sinc(rate * t - n)) for t in times])


def rc_lowpass_gain(ohms, farads, frequencies):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", 0.0)
    circuit.resistor("R1", "in", "out", ohms)
    circuit.capacitor("C1", "out", "0", farads)
    result = circuit.ac(np.asarray(frequencies, float), source="VIN")
    return np.abs(np.asarray(result.v("out")))


def main():
    rate = 1000.0
    print(f"Sampling at {rate:.0f} samples per second: the Nyquist frequency is {rate / 2:.0f} Hz")
    print(f"  {'tone':>8s} {'alias formula':>14s} {'FFT of the samples says':>24s}")
    for tone in [100, 400, 600, 900, 1100, 1900, 2400]:
        samples = sample(tone, rate, 1.0)
        print(f"  {tone:5d} Hz {alias_of(tone, rate):11.0f} Hz {strongest_frequency(samples, rate):20.0f} Hz")

    print("\nThe first samples of a 900 Hz tone and of a 100 Hz tone, both at 1000 samples/s")
    high, low = sample(900, rate, 0.006), sample(100, rate, 0.006)
    for index, (a, b) in enumerate(zip(high, low)):
        print(f"  n = {index}: t = {index / rate * 1e3:3.0f} ms   900 Hz -> {a:+.4f}   100 Hz -> {b:+.4f}")
    print("  identical: after sampling, nothing can tell them apart")

    print("\nRebuilding a 300 Hz tone from its samples (sinc interpolation) between the sample points")
    samples = sample(300, rate, 0.2)
    times = np.linspace(0.095, 0.105, 11)
    rebuilt = sinc_reconstruct(samples, rate, times)
    truth = np.cos(2 * np.pi * 300 * times)
    print(f"  largest error over 10 ms in the middle: {np.max(np.abs(rebuilt - truth)):.4f} (amplitude 1)")
    samples = sample(700, rate, 0.2)
    rebuilt = sinc_reconstruct(samples, rate, times)
    truth_low = np.cos(2 * np.pi * 300 * times)
    print(f"  the same for a 700 Hz tone: the rebuilt wave matches a 300 Hz tone to within "
          f"{np.max(np.abs(rebuilt - truth_low)):.4f}")

    print("\nA 20 Hz sensor signal plus switching noise at 950 Hz, sampled at 1000 samples/s")
    signal_hz, noise_hz = 20.0, 950.0
    print(f"  the noise aliases to {alias_of(noise_hz, rate):.0f} Hz, inside the band we care about (0-100 Hz)")
    print(f"  {'RC filter':>16s} {'cutoff':>8s} {'gain at 20 Hz':>14s} {'gain at 950 Hz':>15s} {'alias left':>11s}")
    for ohms, farads in [(1_600, 1e-6), (16_000, 1e-6), (160_000, 1e-6)]:
        cutoff = 1 / (2 * np.pi * ohms * farads)
        g_signal, g_noise = rc_lowpass_gain(ohms, farads, [signal_hz, noise_hz])
        print(f"  {ohms / 1e3:5.1f} k + 1 uF {cutoff:6.1f} Hz {20 * np.log10(g_signal):10.2f} dB "
              f"{20 * np.log10(g_noise):11.2f} dB {g_noise * 100:9.1f}%")

    n = np.arange(int(rate))
    g_signal, g_noise = rc_lowpass_gain(1_600, 1e-6, [signal_hz, noise_hz])
    cases = {
        "no filter": (1.0, 1.0),
        "1.6 k + 1 uF RC first": (g_signal, g_noise),
    }
    print("  what the ADC samples contain after one second (amplitude 1 signal, amplitude 0.5 noise)")
    for name, (gain_s, gain_n) in cases.items():
        values = gain_s * np.cos(2 * np.pi * signal_hz * n / rate) + 0.5 * gain_n * np.cos(2 * np.pi * noise_hz * n / rate)
        spectrum = np.abs(np.fft.rfft(values)) / (len(values) / 2)
        freqs = np.fft.rfftfreq(len(values), 1 / rate)
        print(f"    {name:22s}: at 20 Hz {spectrum[freqs == 20][0]:.3f}, at 50 Hz (the alias) {spectrum[freqs == 50][0]:.3f}")


if __name__ == "__main__":
    main()
