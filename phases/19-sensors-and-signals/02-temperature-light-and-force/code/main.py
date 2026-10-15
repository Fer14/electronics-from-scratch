import numpy as np

from sim import Circuit

VDD = 3.3
R25 = 10_000.0
BETA = 3950.0
KELVIN = 273.15
DISSIPATION_CONSTANT = 1.5e-3


def thermistor_ohms(celsius):
    return R25 * np.exp(BETA * (1 / (celsius + KELVIN) - 1 / (25 + KELVIN)))


def thermistor_celsius(ohms):
    return 1 / (1 / (25 + KELVIN) + np.log(ohms / R25) / BETA) - KELVIN


def divider_volts(sensor_ohms, fixed_ohms):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RSENSOR", "vdd", "out", float(sensor_ohms))
    circuit.resistor("RFIX", "out", "0", float(fixed_ohms))
    result = circuit.dc()
    return result.v("out"), result.p("RSENSOR")


def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7


def fsr_ohms(newtons):
    return 1e6 if newtons <= 0.2 else 30_000 / newtons


def thermocouple_microvolts(hot_c, cold_c, seebeck=41.0):
    return seebeck * (hot_c - cold_c)


def main():
    print(f"NTC thermistor: R25 = {R25 / 1e3:.0f} kohm, B = {BETA:.0f} K")
    for celsius in [0, 25, 50, 100]:
        print(f"  {celsius:4d} C: {thermistor_ohms(celsius) / 1e3:8.3f} kohm")

    low, high = thermistor_ohms(0), thermistor_ohms(50)
    best = np.sqrt(low * high)
    print(f"\nDivider with the thermistor on top and a fixed resistor below, read from 0 C to 50 C")
    print(f"  fixed resistor that maximises the swing: sqrt(R(0 C) x R(50 C)) = {best / 1e3:.2f} kohm")
    print(f"  {'fixed':>8s} {'V at 0 C':>9s} {'V at 50 C':>10s} {'swing':>7s} {'mV/C at 25 C':>13s} {'self-heat at 50 C':>18s}")
    for fixed in [1_000, 3_300, 10_000, 33_000, 100_000]:
        cold, _ = divider_volts(low, fixed)
        hot, power = divider_volts(high, fixed)
        below, _ = divider_volts(thermistor_ohms(24.5), fixed)
        above, _ = divider_volts(thermistor_ohms(25.5), fixed)
        heating = power / DISSIPATION_CONSTANT
        print(f"  {fixed / 1e3:6.1f} k {cold:7.3f} V {hot:8.3f} V {hot - cold:5.3f} V {(above - below) * 1e3:11.1f} "
              f"{heating:13.3f} C")

    print("\nReading it back: 10-bit ADC code -> volts -> resistance -> temperature (10 k fixed)")
    for celsius in [5.0, 21.3, 37.0, 48.0]:
        volts, _ = divider_volts(thermistor_ohms(celsius), 10_000)
        code = int(np.floor(volts / VDD * 1024))
        measured = (code + 0.5) * VDD / 1024
        sensor = 10_000 * (VDD - measured) / measured
        print(f"  true {celsius:5.1f} C -> {volts:.4f} V -> code {code:4d} -> {sensor / 1e3:7.3f} kohm -> "
              f"{thermistor_celsius(sensor):6.2f} C")

    print("\nLight: LDR on top of a 10 k resistor")
    for lux in [1, 10, 100, 1000, 10000]:
        volts, _ = divider_volts(ldr_ohms(lux), 10_000)
        print(f"  {lux:6d} lux: LDR {ldr_ohms(lux) / 1e3:8.2f} kohm -> {volts:.3f} V")

    print("\nForce: force-sensitive resistor on top of a 10 k resistor (resistance roughly 30 k / F)")
    for newtons in [0.0, 0.5, 1.0, 5.0, 20.0]:
        volts, _ = divider_volts(fsr_ohms(newtons), 10_000)
        print(f"  {newtons:5.1f} N: FSR {fsr_ohms(newtons) / 1e3:8.2f} kohm -> {volts:.3f} V")

    print("\nThermocouple (type K, about 41 uV/C): the voltage depends on BOTH junctions")
    for hot, cold in [(100, 25), (100, 0), (400, 25)]:
        microvolts = thermocouple_microvolts(hot, cold)
        print(f"  hot {hot:4d} C, cold junction {cold:3d} C: {microvolts:8.0f} uV "
              f"(needs a gain of about {1.0 / (microvolts * 1e-6):.0f} to reach 1 V)")


if __name__ == "__main__":
    main()
