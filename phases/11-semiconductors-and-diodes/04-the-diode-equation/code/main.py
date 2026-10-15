from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

BOLTZMANN_EV = 8.617333e-5
SILICON_GAP_EV = 1.12
SATURATION_CURRENT = 1e-14
IDEALITY = 1.0


def thermal_voltage(kelvin=300.0):
    return BOLTZMANN_EV * kelvin


def diode_current(volts, saturation=SATURATION_CURRENT, ideality=IDEALITY, kelvin=300.0):
    return saturation * (np.exp(volts / (ideality * thermal_voltage(kelvin))) - 1.0)


def diode_voltage(amps, saturation=SATURATION_CURRENT, ideality=IDEALITY, kelvin=300.0):
    return ideality * thermal_voltage(kelvin) * np.log(amps / saturation + 1.0)


def saturation_at(kelvin, saturation_300=SATURATION_CURRENT):
    return saturation_300 * (kelvin / 300.0) ** 3 * np.exp(-SILICON_GAP_EV / BOLTZMANN_EV * (1 / kelvin - 1 / 300.0))


def show_table():
    print(f"Shockley diode equation, I_S = {SATURATION_CURRENT:.0e} A, n = {IDEALITY}, V_T = {thermal_voltage() * 1000:.2f} mV")
    print(f"  {'V (V)':>6} {'I':>14}")
    for volts in [-1.0, 0.0, 0.1, 0.3, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8]:
        amps = diode_current(volts)
        print(f"  {volts:>6.2f} {amps:>14.4e} A")
    print()


def show_decades():
    print("Voltage needed for each current (each decade costs n * V_T * ln 10 volts)")
    previous = None
    for amps in [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
        volts = diode_voltage(amps)
        step = "" if previous is None else f"   (+{(volts - previous) * 1000:.1f} mV)"
        print(f"  I = {amps:7.0e} A  ->  V = {volts:.4f} V{step}")
        previous = volts
    print()


def show_temperature():
    print("Same diode at 1 mA, different temperatures")
    reference = None
    for celsius in [0, 25, 50, 75, 100]:
        kelvin = celsius + 273.15
        volts = diode_voltage(1e-3, saturation_at(kelvin), kelvin=kelvin)
        if reference is None:
            reference = (celsius, volts)
        print(f"  {celsius:>4} C   I_S = {saturation_at(kelvin):.2e} A   V = {volts:.4f} V")
    slope = (volts - reference[1]) / (celsius - reference[0])
    print(f"  slope = {slope * 1000:.2f} mV per degree C")
    print()


def compare_with_simulator():
    print("Diode alone across a voltage source: formula versus our simulator")
    for volts in [0.4, 0.55, 0.65, 0.7]:
        circuit = Circuit()
        circuit.voltage_source("V1", "a", "0", volts)
        circuit.diode("D1", "a", "0", Is=SATURATION_CURRENT, n=IDEALITY)
        result = circuit.dc()
        simulated = result.i("D1")
        print(f"  V = {volts:.2f} V   formula I = {diode_current(volts):.4e} A   simulator I = {simulated:.4e} A")
    print()


def compare_models(source_volts, ohms):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", source_volts)
    circuit.resistor("R1", "in", "a", ohms)
    circuit.diode("D1", "a", "0", Is=SATURATION_CURRENT, n=IDEALITY)
    result = circuit.dc()
    ideal = source_volts / ohms
    constant_drop = max(source_volts - 0.7, 0.0) / ohms
    print(f"{source_volts} V source, {ohms} ohm resistor, diode to ground")
    print(f"  ideal switch (0 V drop)   I = {ideal * 1000:8.3f} mA")
    print(f"  constant drop (0.7 V)     I = {constant_drop * 1000:8.3f} mA")
    print(f"  exponential (simulator)   I = {result.i('D1') * 1000:8.3f} mA   V_D = {result.v('a'):.4f} V")
    print()


def plot_curves():
    volts = np.linspace(0.0, 0.8, 400)
    amps = diode_current(volts)
    figure, (linear, logarithmic) = plt.subplots(1, 2, figsize=(10, 4))
    linear.plot(volts, amps * 1000)
    linear.set_ylim(-1, 20)
    linear.set_xlabel("diode voltage (V)")
    linear.set_ylabel("current (mA)")
    linear.set_title("linear scale: a 'knee' near 0.65 V")
    logarithmic.semilogy(volts[1:], amps[1:])
    logarithmic.set_xlabel("diode voltage (V)")
    logarithmic.set_ylabel("current (A)")
    logarithmic.set_title("log scale: a straight line, x10 every 60 mV")
    figure.tight_layout()
    path = Path(__file__).parent / "out.png"
    figure.savefig(path, dpi=120)
    print(f"Saved the I-V curves to {path.name}")


def main():
    show_table()
    show_decades()
    show_temperature()
    compare_with_simulator()
    compare_models(5.0, 1000)
    compare_models(1.0, 100)
    plot_curves()


if __name__ == "__main__":
    main()
