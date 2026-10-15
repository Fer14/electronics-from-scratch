import numpy as np

from sim import Circuit

RAILS = (0.0, 5.0)


def threshold_detector(sensor_volts, top_ohms, bottom_ohms=10e3):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", 5.0)
    circuit.voltage_source("VS", "sensor", "0", sensor_volts)
    circuit.resistor("RT", "vcc", "ref", top_ohms)
    circuit.resistor("RB", "ref", "0", bottom_ohms)
    circuit.opamp("U1", plus="sensor", minus="ref", out="out", gain=1e5, rails=RAILS)
    return circuit.dc()


def show_threshold():
    reference = 5.0 * 10e3 / (15e3 + 10e3)
    print(f"Threshold set by a divider: 15 k over 10 k from 5 V gives V_ref = {reference:.2f} V")
    for volts in [1.0, 1.9, 1.99, 2.0, 2.01, 2.1, 3.0]:
        result = threshold_detector(volts, 15e3)
        print(f"  sensor {volts:5.2f} V  ->  output {result.v('out'):6.3f} V")
    print()


def noisy_input(circuit):
    circuit.sine_source("VSLOW", "a", "0", amplitude=2.0, freq=10.0, offset=2.5)
    circuit.sine_source("VNOISE", "in", "a", amplitude=0.08, freq=900.0, offset=0.0)


def plain_comparator():
    circuit = Circuit()
    noisy_input(circuit)
    circuit.voltage_source("VREF", "ref", "0", 2.5)
    circuit.opamp("U1", plus="ref", minus="in", out="out", gain=1e5, rails=RAILS)
    return circuit.transient(t_stop=0.2, dt=1e-5)


def schmitt_trigger(feedback_ohms):
    circuit = Circuit()
    noisy_input(circuit)
    circuit.voltage_source("VREF", "ref", "0", 2.5)
    circuit.resistor("R1", "ref", "p", 10e3)
    circuit.resistor("R2", "out", "p", feedback_ohms)
    circuit.opamp("U1", plus="p", minus="in", out="out", gain=1e5, rails=RAILS)
    return circuit.transient(t_stop=0.2, dt=1e-5)


def count_edges(result):
    output = np.asarray(result.v("out")) > 2.5
    return int(np.sum(output[1:] != output[:-1]))


def show_noise():
    print("A slow 10 Hz signal (0.5 V to 4.5 V) with 80 mV of 900 Hz 'noise' on top; 0.2 s = 2 slow cycles")
    print(f"  plain comparator at 2.5 V:              {count_edges(plain_comparator()):>3} output edges (4 would be right)")
    for feedback in [1e6, 100e3, 47e3]:
        fraction = 10e3 / (10e3 + feedback)
        low = 2.5 * (1 - fraction)
        high = low + 5.0 * fraction
        result = schmitt_trigger(feedback)
        print(f"  Schmitt, R2 = {feedback / 1e3:>5.0f} k: thresholds {low:.3f} / {high:.3f} V (hysteresis {high - low:.3f} V): {count_edges(result):>3} output edges")
    print()


def show_speed_of_decision():
    print("Inverting comparator: output HIGH when the input is BELOW the reference (input on the minus pin)")
    circuit = Circuit()
    circuit.voltage_source("VREF", "ref", "0", 2.5)
    circuit.voltage_source("VIN", "in", "0", 2.4)
    circuit.opamp("U1", plus="ref", minus="in", out="out", gain=1e5, rails=RAILS)
    print(f"  input 2.4 V, reference 2.5 V -> output {circuit.dc().v('out'):.3f} V")


def main():
    show_threshold()
    show_noise()
    show_speed_of_decision()


if __name__ == "__main__":
    main()
