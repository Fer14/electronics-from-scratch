import numpy as np

from sim import Circuit

BOLTZMANN = 1.380649e-23
ELECTRON = 1.602176634e-19
KELVIN_ROOM = 300.0


def thermal_noise_volts(ohms, bandwidth, kelvin=KELVIN_ROOM):
    return np.sqrt(4 * BOLTZMANN * kelvin * ohms * bandwidth)


def shot_noise_amps(current, bandwidth):
    return np.sqrt(2 * ELECTRON * current * bandwidth)


def thevenin_resistance(top_ohms, bottom_ohms):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", 0.0)
    circuit.resistor("RTOP", "vdd", "out", top_ohms)
    circuit.resistor("RBOT", "out", "0", bottom_ohms)
    circuit.current_source("ITEST", "0", "out", 1e-3)
    return circuit.dc().v("out") / 1e-3


def band_limited_rms(noise, rate, bandwidth):
    spectrum = np.fft.rfft(noise)
    freqs = np.fft.rfftfreq(len(noise), 1 / rate)
    spectrum[freqs > bandwidth] = 0
    return np.std(np.fft.irfft(spectrum, len(noise)))


def pink_noise(points, generator):
    white = np.fft.rfft(generator.normal(0, 1, points))
    freqs = np.fft.rfftfreq(points)
    freqs[0] = freqs[1]
    pink = np.fft.irfft(white / np.sqrt(freqs), points)
    return pink / np.std(pink)


def block_average_spread(values, block):
    usable = len(values) // block * block
    return np.std(values[:usable].reshape(-1, block).mean(axis=1))


def main():
    print(f"Thermal (Johnson) noise sqrt(4 k T R B) at {KELVIN_ROOM:.0f} K over 10 kHz")
    for ohms in [100, 1_000, 10_000, 100_000, 1_000_000]:
        print(f"  {ohms:9,d} ohm: {thermal_noise_volts(ohms, 10e3) * 1e6:7.3f} uV RMS "
              f"({thermal_noise_volts(ohms, 1.0) * 1e9:6.2f} nV per root hertz)")

    source = thevenin_resistance(10_000, 10_000)
    print(f"\nA 10 k / 10 k sensor divider looks like {source:.0f} ohm to the ADC (found with a 1 mA test current in sim)")
    print(f"  its thermal noise over 1 kHz: {thermal_noise_volts(source, 1e3) * 1e9:.0f} nV RMS, far below a 12-bit LSB of 806 uV")

    print("\nShot noise sqrt(2 q I B) of a photodiode current over 10 kHz")
    for amps in [1e-9, 1e-6, 1e-3]:
        noise = shot_noise_amps(amps, 10e3)
        print(f"  I = {amps:7.0e} A: noise {noise:9.3e} A RMS, SNR {20 * np.log10(amps / noise):6.1f} dB")

    rate, points = 100_000.0, 2 ** 17
    generator = np.random.default_rng(5)
    white = generator.normal(0, 1, points)
    print("\nWhite noise: RMS grows with the square root of the bandwidth you let through")
    reference = band_limited_rms(white, rate, 1000)
    for bandwidth in [1000, 4000, 16000, 50000]:
        measured = band_limited_rms(white, rate, bandwidth)
        print(f"  bandwidth {bandwidth:6d} Hz: RMS {measured:.3f}  (ratio to 1 kHz {measured / reference:.2f}, "
              f"sqrt ratio {np.sqrt(bandwidth / 1000):.2f})")

    print("\nAveraging N readings of 1.000 mV buried in 10 mV RMS of white noise")
    signal = 1.0e-3
    readings = signal + 10e-3 * generator.normal(0, 1, 2 ** 16)
    print(f"  {'N':>6s} {'noise left':>11s} {'10 mV / sqrt(N)':>16s} {'SNR':>8s}")
    for count in [1, 16, 256, 4096]:
        spread = block_average_spread(readings, count)
        print(f"  {count:6d} {spread * 1e3:8.3f} mV {10 / np.sqrt(count):13.3f} mV {20 * np.log10(signal / spread):6.1f} dB")

    print("\nWhite versus 1/f (pink) noise of the same RMS: does averaging longer keep helping?")
    pink = pink_noise(2 ** 16, generator)
    white_unit = generator.normal(0, 1, 2 ** 16)
    for count in [1, 16, 256, 4096]:
        print(f"  blocks of {count:5d}: white spread {block_average_spread(white_unit, count):.4f}, "
              f"pink spread {block_average_spread(pink, count):.4f}")

    print("\nMains hum (50 Hz, 5 mV) on a 1 mV DC signal, sampled at 10 000 samples/s and averaged")
    sample_rate = 10_000.0
    for window_ms in [15.0, 20.0, 40.0, 50.0]:
        count = int(sample_rate * window_ms / 1000)
        errors = []
        for start in np.linspace(0, 0.02, 9, endpoint=False):
            t = start + np.arange(count) / sample_rate
            average = (1e-3 + 5e-3 * np.sin(2 * np.pi * 50 * t)).mean()
            errors.append(abs(average - 1e-3))
        print(f"  averaging {window_ms:4.0f} ms ({window_ms / 20:4.2f} mains periods): worst error {max(errors) * 1e6:8.2f} uV")


if __name__ == "__main__":
    main()
