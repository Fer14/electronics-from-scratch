import numpy as np

from sim import Circuit

VREF = 3.3


def quantize(volts, bits, vref=VREF):
    lsb = vref / 2 ** bits
    codes = np.clip(np.floor(volts / lsb), 0, 2 ** bits - 1)
    return codes, (codes + 0.5) * lsb


def sine_test(bits, cycles=127, points=8192, extra_noise_lsb=0.0, seed=3):
    lsb = VREF / 2 ** bits
    n = np.arange(points)
    amplitude = VREF / 2 - lsb
    signal = VREF / 2 + amplitude * np.sin(2 * np.pi * cycles * n / points)
    if extra_noise_lsb:
        signal = signal + np.random.default_rng(seed).normal(0, extra_noise_lsb * lsb, points)
    _, rebuilt = quantize(signal, bits)
    ideal = VREF / 2 + amplitude * np.sin(2 * np.pi * cycles * n / points)
    error = rebuilt - ideal
    signal_power = amplitude ** 2 / 2
    return 10 * np.log10(signal_power / np.mean(error ** 2))


def divider_volts(top_ohms, bottom_ohms):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VREF)
    circuit.resistor("RTOP", "vdd", "out", top_ohms)
    circuit.resistor("RBOT", "out", "0", bottom_ohms)
    return circuit.dc().v("out")


def main():
    bits = 8
    lsb = VREF / 2 ** bits
    print(f"An {bits}-bit quantizer on {VREF} V: {2 ** bits} codes, LSB = {lsb * 1e3:.3f} mV")
    ramp = np.linspace(0, VREF * 0.999, 100_001)
    _, rebuilt = quantize(ramp, bits)
    error = rebuilt - ramp
    print(f"  error on a slow ramp: min {error.min() / lsb:+.3f} LSB, max {error.max() / lsb:+.3f} LSB")
    print(f"  RMS error {np.sqrt(np.mean(error ** 2)) * 1e3:.3f} mV, theory LSB / sqrt(12) = {lsb / np.sqrt(12) * 1e3:.3f} mV")
    histogram, _ = np.histogram(error / lsb, bins=5, range=(-0.5, 0.5))
    print(f"  the error is spread evenly: fractions in 5 equal bins {np.round(histogram / histogram.sum(), 3)}")

    print("\nSignal-to-quantization-noise ratio of a full-scale sine")
    print(f"  {'bits':>4s} {'measured':>10s} {'6.02 N + 1.76':>14s}")
    for bits_choice in [4, 6, 8, 10, 12, 16]:
        print(f"  {bits_choice:4d} {sine_test(bits_choice):8.2f} dB {6.02 * bits_choice + 1.76:11.2f} dB")

    print("\nA 12-bit ADC whose input also carries 1 LSB RMS of noise")
    sinad = sine_test(12, extra_noise_lsb=1.0)
    print(f"  measured SINAD {sinad:.2f} dB -> effective number of bits (SINAD - 1.76) / 6.02 = {(sinad - 1.76) / 6.02:.2f}")

    print("\nA tiny sine (amplitude 0.7 LSB) through an 8-bit quantizer becomes a square-ish wave")
    points, cycles = 4096, 64
    n = np.arange(points)
    center = 100.5 * lsb
    tiny = center + 0.7 * lsb * np.sin(2 * np.pi * cycles * n / points)
    codes, _ = quantize(tiny, 8)
    print(f"  codes used: {sorted(set(codes.astype(int).tolist()))}")
    spectrum = np.abs(np.fft.rfft(codes - codes.mean()))
    fundamental = spectrum[cycles]
    for harmonic in [1, 3, 5, 7]:
        print(f"  harmonic {harmonic}: {20 * np.log10(spectrum[harmonic * cycles] / fundamental + 1e-12):7.1f} dB relative to the fundamental")

    print("\nDither: averaging cannot beat the LSB unless there is some noise")
    true_volts = divider_volts(10_000, 9_870)
    print(f"  a thermistor divider (10 k over 9.87 k) gives {true_volts:.5f} V = {true_volts / lsb:.3f} LSB")
    generator = np.random.default_rng(11)
    for label, noise in [("no noise", 0.0), ("0.5 LSB RMS noise", 0.5), ("1 LSB RMS noise", 1.0)]:
        samples = true_volts + generator.normal(0, noise * lsb, 4096) if noise else np.full(4096, true_volts)
        _, rebuilt = quantize(samples, 8)
        estimate = rebuilt.mean()
        print(f"  {label:18s}: average of 4096 readings {estimate / lsb:8.3f} LSB, error {(estimate - true_volts) / lsb:+.3f} LSB")


if __name__ == "__main__":
    main()
