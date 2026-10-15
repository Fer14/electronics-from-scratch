import numpy as np

from sim import Circuit

RAILS = (-12.0, 12.0)


def ramp(input_volts, ohms, farads, stop, offset_volts=0.0, leak_ohms=None):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("R", "in", "n", ohms)
    circuit.capacitor("C", "n", "out", farads, v0=0.0)
    if leak_ohms:
        circuit.resistor("RLEAK", "n", "out", leak_ohms)
    circuit.voltage_source("VOS", "p", "0", offset_volts)
    circuit.opamp("U1", plus="p", minus="n", out="out", gain=1e5, rails=RAILS)
    return circuit.transient(t_stop=stop, dt=stop / 2000)


def show_ramp():
    result = ramp(-1.0, 10e3, 100e-9, 5e-3)
    time = np.asarray(result.time)
    out = np.asarray(result.v("out"))
    print("Integrator: -1 V into R = 10 k, C = 100 nF. Ideal: V_out = (1 / RC) x t = 1000 V/s x t")
    for ms in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        print(f"  t = {ms:3.1f} ms   V_out = {np.interp(ms * 1e-3, time, out):7.4f} V   (ideal {ms:5.2f} V)")
    print(f"  current through R and C: {result.i('R')[-1] * 1e6:.3f} uA, constant, so the capacitor charges linearly")
    print()


def show_drift():
    print("The integrator's weakness: it integrates every tiny DC error. A 1 mV offset, no input, R = 10 k, C = 100 nF")
    plain = ramp(0.0, 10e3, 100e-9, 0.5, offset_volts=1e-3)
    leaky = ramp(0.0, 10e3, 100e-9, 0.5, offset_volts=1e-3, leak_ohms=1e6)
    time = np.asarray(plain.time)
    for seconds in [0.05, 0.1, 0.2, 0.5]:
        print(f"  t = {seconds:4.2f} s   plain {np.interp(seconds, time, np.asarray(plain.v('out'))):8.3f} V   "
              f"with 1 Mohm across C {np.interp(seconds, time, np.asarray(leaky.v('out'))):7.4f} V")
    print("  Plain: the 1 mV drives 0.1 uA into C forever, until the output hits the rail.")
    print("  Leaky: DC gain is limited to 1 + 1M/10k = 101, so the output settles at 101 x 1 mV.")
    print()


def square_chain():
    circuit = Circuit()
    circuit.pulse_source("VSQ", "sq", "0", low=-1.0, high=1.0, period=1e-3, duty=0.5)
    circuit.resistor("RI", "sq", "n1", 10e3)
    circuit.capacitor("CI", "n1", "tri", 10e-9, v0=0.0)
    circuit.resistor("RLEAK", "n1", "tri", 1e6)
    circuit.opamp("U1", plus="0", minus="n1", out="tri", gain=1e5, rails=RAILS)
    circuit.capacitor("CD", "tri", "x", 10e-9, v0=0.0)
    circuit.resistor("RD", "x", "n2", 1e3)
    circuit.resistor("RF", "n2", "back", 10e3)
    circuit.opamp("U2", plus="0", minus="n2", out="back", gain=1e5, rails=RAILS)
    return circuit.transient(t_stop=40e-3, dt=1e-6)


def show_chain():
    result = square_chain()
    time = np.asarray(result.time)
    window = time >= 38e-3
    triangle = np.asarray(result.v("tri"))[window]
    back = np.asarray(result.v("back"))[window]
    print("Square (+/-1 V, 1 kHz) -> integrator (10 k, 10 nF) -> differentiator (10 nF, 10 k) -> ?")
    print(f"  integrator output: triangle from {triangle.min():6.3f} V to {triangle.max():6.3f} V "
          f"(ideal swing 1 V x 0.5 ms / 0.1 ms = 5 V peak-to-peak, measured {triangle.max() - triangle.min():.3f} V)")
    print(f"  differentiator output: from {back.min():6.3f} V to {back.max():6.3f} V "
          f"(ideal: R C x slope = 10k x 10n x 10000 V/s = 1 V, so a square of +/-1 V again)")
    print()


def show_frequency_response():
    print("Frequency response, |V_out / V_in|")
    integrator = Circuit()
    integrator.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    integrator.resistor("R", "in", "n", 10e3)
    integrator.capacitor("C", "n", "out", 10e-9)
    integrator.resistor("RLEAK", "n", "out", 1e6)
    integrator.opamp("U1", plus="0", minus="n", out="out", gain=1e5)
    differentiator = Circuit()
    differentiator.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    differentiator.capacitor("C", "in", "x", 10e-9)
    differentiator.resistor("RS", "x", "n", 1e3)
    differentiator.resistor("RF", "n", "out", 10e3)
    differentiator.opamp("U1", plus="0", minus="n", out="out", gain=1e5)
    pure = Circuit()
    pure.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    pure.capacitor("C", "in", "n", 10e-9)
    pure.resistor("RF", "n", "out", 10e3)
    pure.opamp("U1", plus="0", minus="n", out="out", gain=1e5)
    freqs = [10.0, 100.0, 1591.5, 10e3, 100e3]
    a = integrator.ac(freqs, source="VIN")
    b = differentiator.ac(freqs, source="VIN")
    c = pure.ac(freqs, source="VIN")
    print(f"  {'freq':>9} {'integrator':>11} {'1/(2 pi f RC)':>14} {'pure diff.':>11} {'2 pi f RC':>10} {'with 1 k in series':>19}")
    for k, freq in enumerate(freqs):
        rc = 10e3 * 10e-9
        print(f"  {freq:>7.0f}Hz {abs(a.v('out')[k]):>11.3f} {1 / (2 * np.pi * freq * rc):>14.3f} {abs(c.v('out')[k]):>11.3f} "
              f"{2 * np.pi * freq * rc:>10.3f} {abs(b.v('out')[k]):>19.3f}")
    print("  The pure differentiator's gain keeps rising with frequency: it amplifies high-frequency noise.")


def main():
    show_ramp()
    show_drift()
    show_chain()
    show_frequency_response()


if __name__ == "__main__":
    main()
