import math

import numpy as np

from sim import Circuit

OPEN_LOOP_GAIN = 1e5
GAIN_BANDWIDTH = 1e6
SLEW_RATE = 0.5e6
STAGE_CAPACITOR = 1e-9
INPUT_GAIN = 2 * math.pi * GAIN_BANDWIDTH / SLEW_RATE
STAGE_GM = 2 * math.pi * GAIN_BANDWIDTH * STAGE_CAPACITOR / INPUT_GAIN
STAGE_RESISTOR = OPEN_LOOP_GAIN / (INPUT_GAIN * STAGE_GM)


def real_opamp(circuit, name, plus, minus, out, rails=(-12.0, 12.0), offset=0.0):
    inner = f"{name}_pi"
    circuit.voltage_source(f"{name}_VOS", inner, plus, offset)
    circuit.opamp(f"{name}_IN", plus=inner, minus=minus, out=f"{name}_x", gain=INPUT_GAIN, rails=(-1.0, 1.0))
    circuit.vccs(f"{name}_GM", "0", f"{name}_y", f"{name}_x", "0", STAGE_GM)
    circuit.resistor(f"{name}_R", f"{name}_y", "0", STAGE_RESISTOR)
    circuit.capacitor(f"{name}_C", f"{name}_y", "0", STAGE_CAPACITOR)
    circuit.opamp(f"{name}_OUT", plus=f"{name}_y", minus=out, out=out, gain=1e5, rails=rails)


def show_model():
    pole = 1 / (2 * math.pi * STAGE_RESISTOR * STAGE_CAPACITOR)
    print("Our 'real' op-amp model, built from simulator parts")
    print(f"  input stage: gain {INPUT_GAIN:.2f}, output limited to +/-1 V (it saturates for inputs above about {1 / INPUT_GAIN * 1000:.0f} mV)")
    print(f"  integrating stage: g_m = {STAGE_GM * 1e6:.1f} uA/V into C = {STAGE_CAPACITOR * 1e9:.0f} nF in parallel with {STAGE_RESISTOR / 1e6:.2f} Mohm")
    print(f"  DC gain = {INPUT_GAIN:.2f} x {STAGE_GM:.3e} x {STAGE_RESISTOR:.3e} = {OPEN_LOOP_GAIN:.0f} ({20 * math.log10(OPEN_LOOP_GAIN):.0f} dB)")
    print(f"  dominant pole at {pole:.1f} Hz, gain-bandwidth product {OPEN_LOOP_GAIN * pole / 1e6:.2f} MHz")
    print(f"  slew rate = g_m x 1 V / C = {STAGE_GM / STAGE_CAPACITOR / 1e6:.2f} V/us")
    print()


def open_loop_response():
    circuit = Circuit()
    circuit.sine_source("VIN", "p", "0", amplitude=1.0, freq=1000.0)
    real_opamp(circuit, "U1", "p", "0", "out")
    freqs = [1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6]
    result = circuit.ac(freqs, source="VIN")
    print("Open-loop gain versus frequency")
    for k, freq in enumerate(freqs):
        print(f"  {freq:>9.0f} Hz: {result.gain_db('out')[k]:6.1f} dB   (x{abs(result.v('out')[k]):9.1f})")
    print("  Above the pole, gain x frequency stays at 1 MHz: 10 kHz -> x100, 100 kHz -> x10, 1 MHz -> x1.")
    print()


def non_inverting(gain, extra=None):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    real_opamp(circuit, "U1", "in", "n", "out")
    if gain == 1:
        circuit.resistor("RF", "out", "n", 1.0)
    else:
        circuit.resistor("RF", "out", "n", 1e3 * (gain - 1))
        circuit.resistor("RG", "n", "0", 1e3)
    return circuit


def show_bandwidth():
    freqs = np.logspace(1, 7, 601)
    print("Closed loop: the more gain you ask for, the less bandwidth you get (GBW / gain)")
    for gain in [1, 10, 100, 1000]:
        result = non_inverting(gain).ac(freqs, source="VIN")
        print(f"  gain {gain:>5}: low-frequency gain {result.gain_db_at(100.0, 'out'):6.2f} dB, "
              f"bandwidth {result.cutoff('out') / 1e3:8.1f} kHz   (1 MHz / {gain} = {GAIN_BANDWIDTH / gain / 1e3:7.1f} kHz)")
    print()


def show_slew():
    circuit = Circuit()
    circuit.pulse_source("VIN", "in", "0", low=0.0, high=5.0, period=40e-6, duty=0.5)
    real_opamp(circuit, "U1", "in", "out", "out")
    result = circuit.transient(t_stop=20e-6, dt=10e-9)
    time = np.asarray(result.time)
    out = np.asarray(result.v("out"))
    t10 = time[np.argmax(out > 0.5)]
    t90 = time[np.argmax(out > 4.5)]
    print("Slew rate: a follower asked to jump from 0 to 5 V")
    print(f"  output goes from 0.5 V to 4.5 V in {(t90 - t10) * 1e6:.2f} us -> {4.0 / (t90 - t10) / 1e6:.3f} V/us (model: 0.50 V/us)")
    full_power = SLEW_RATE / (2 * math.pi * 5.0)
    print(f"  full-power bandwidth for a 5 V-peak sine: SR / (2 pi V_peak) = {full_power / 1e3:.1f} kHz")
    for freq in [5e3, 15e3, 50e3]:
        circuit = Circuit()
        circuit.sine_source("VIN", "in", "0", amplitude=5.0, freq=freq)
        real_opamp(circuit, "U1", "in", "out", "out")
        run = circuit.transient(t_stop=6 / freq, dt=1 / freq / 400)
        tail = np.asarray(run.v("out"))[np.asarray(run.time) > 3 / freq]
        print(f"  5 V-peak sine at {freq / 1e3:>4.0f} kHz through a follower: output peak {tail.max():5.2f} V")
    print()


def show_offset():
    print("Input offset voltage: a 2 mV error source in series with the plus input, input grounded")
    for gain in [1, 10, 100, 1000]:
        circuit = Circuit()
        circuit.voltage_source("VIN", "in", "0", 0.0)
        real_opamp(circuit, "U1", "in", "n", "out", offset=2e-3)
        if gain == 1:
            circuit.resistor("RF", "out", "n", 1.0)
        else:
            circuit.resistor("RF", "out", "n", 1e3 * (gain - 1))
            circuit.resistor("RG", "n", "0", 1e3)
        print(f"  gain {gain:>5}: output {circuit.dc().v('out') * 1000:9.2f} mV with no signal at all")
    print()


def show_bias_current():
    print("Input bias current: 100 nA flowing into each input, sensor with 100 kohm source resistance, gain 1")
    for label, compensation in [("no compensation", None), ("100 k in the feedback path too", 100e3)]:
        circuit = Circuit()
        circuit.voltage_source("VS", "s", "0", 0.0)
        circuit.resistor("RS", "s", "in", 100e3)
        circuit.current_source("IBP", "in", "0", 100e-9)
        circuit.current_source("IBN", "n", "0", 100e-9)
        circuit.opamp("U1", plus="in", minus="n", out="out", gain=1e5, rails=(-12.0, 12.0))
        circuit.resistor("RF", "out", "n", compensation or 1.0)
        print(f"  {label:<32}: output {circuit.dc().v('out') * 1000:7.3f} mV")
    print()


def show_swing():
    print("Output swing: an older op-amp on a single 5 V supply can only reach about 0 to 3.5 V")
    for volts in [1.0, 3.0, 4.0, 4.9]:
        circuit = Circuit()
        circuit.voltage_source("VIN", "in", "0", volts)
        real_opamp(circuit, "U1", "in", "out", "out", rails=(0.0, 3.5))
        rail_to_rail = Circuit()
        rail_to_rail.voltage_source("VIN", "in", "0", volts)
        real_opamp(rail_to_rail, "U1", "in", "out", "out", rails=(0.0, 5.0))
        print(f"  follower, input {volts:.1f} V: limited swing {circuit.dc().v('out'):.3f} V   rail-to-rail {rail_to_rail.dc().v('out'):.3f} V")


def main():
    show_model()
    open_loop_response()
    show_bandwidth()
    show_slew()
    show_offset()
    show_bias_current()
    show_swing()


if __name__ == "__main__":
    main()
