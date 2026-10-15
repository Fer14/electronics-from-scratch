import numpy as np

from sim import Circuit

VDD = 3.3
ADC_BITS = 10


def adc_code(volts):
    return int(np.clip(np.floor(volts / VDD * 2 ** ADC_BITS), 0, 2 ** ADC_BITS - 1))


def code_to_volts(code):
    return code * VDD / 2 ** ADC_BITS


def tmp36_volts(celsius):
    return 0.5 + 0.010 * celsius


def potentiometer_reading(fraction, pot_ohms, load_ohms):
    top = max(pot_ohms * (1 - fraction), 1e-3)
    bottom = max(pot_ohms * fraction, 1e-3)
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RTOP", "vdd", "wiper", top)
    circuit.resistor("RBOT", "wiper", "0", bottom)
    if load_ohms:
        circuit.resistor("RLOAD", "wiper", "0", load_ohms)
    return circuit.dc().v("wiper")


def main():
    print("A linear temperature sensor (TMP36-like: 500 mV at 0 C, 10 mV per C) read by a 10-bit, 3.3 V ADC")
    lsb = VDD / 2 ** ADC_BITS
    print(f"  sensitivity 10 mV/C, ADC step {lsb * 1e3:.3f} mV -> resolution {lsb / 0.010:.3f} C per code")
    print(f"  {'true C':>7s} {'sensor V':>9s} {'code':>5s} {'reading C':>10s}")
    for celsius in [-10.0, 0.0, 21.7, 25.0, 85.0, 125.0]:
        volts = tmp36_volts(celsius)
        code = adc_code(volts)
        reading = (code_to_volts(code) - 0.5) / 0.010
        print(f"  {celsius:7.1f} {volts:7.3f} V {code:5d} {reading:9.2f} C")

    print("\nA potentiometer as an angle sensor (0 to 270 degrees), loaded by what reads it")
    print(f"  {'angle':>6s} {'ideal V':>8s} {'100 k load':>11s} {'10 k load':>10s} {'error at 10 k':>14s}")
    worst = 0.0
    for angle in [0, 45, 90, 135, 180, 225, 270]:
        fraction = angle / 270
        ideal = potentiometer_reading(fraction, 10_000, None)
        light = potentiometer_reading(fraction, 10_000, 100_000)
        heavy = potentiometer_reading(fraction, 10_000, 10_000)
        error_degrees = (heavy - ideal) / VDD * 270
        worst = min(worst, error_degrees)
        print(f"  {angle:4d} deg {ideal:6.3f} V {light:9.3f} V {heavy:8.3f} V {error_degrees:11.1f} deg")
    print(f"  worst error with a 10 kohm load: {worst:.1f} degrees, so the transfer function is no longer a straight line")

    print("\nTwo-point calibration of a sensor with a 2% gain error and a +15 mV offset")
    generator = np.random.default_rng(1)
    true_celsius = np.array([0.0, 20.0, 40.0, 60.0, 80.0, 100.0])
    raw = 0.5 + 1.02 * 0.010 * true_celsius + 0.015
    naive = (raw - 0.5) / 0.010
    low_true, high_true = 0.0, 100.0
    low_raw, high_raw = raw[0], raw[-1]
    gain = (high_true - low_true) / (high_raw - low_raw)
    calibrated = low_true + (raw - low_raw) * gain
    for t, n, c in zip(true_celsius, naive, calibrated):
        print(f"  true {t:5.1f} C: datasheet formula says {n:6.2f} C (error {n - t:+5.2f}), calibrated {c:6.2f} C")

    print("\nAccuracy versus precision: 1000 readings of a 25.00 C object")
    readings = {
        "precise but inaccurate": 25.0 + 1.5 + generator.normal(0, 0.05, 1000),
        "accurate but imprecise": 25.0 + generator.normal(0, 1.0, 1000),
        "accurate and precise": 25.0 + generator.normal(0, 0.05, 1000),
    }
    for name, values in readings.items():
        print(f"  {name:24s} mean {values.mean():6.2f} C (error {values.mean() - 25:+5.2f}), spread (std) {values.std():5.2f} C")


if __name__ == "__main__":
    main()
