import numpy as np

from sim import Circuit

VDD = 3.3
ADC_BITS = 12


def difference_amplifier(v_sensor, v_reference, r1, r2, rails=None, mismatch=1.0):
    circuit = Circuit()
    circuit.voltage_source("VS", "sensor", "0", v_sensor)
    circuit.voltage_source("VREF", "ref", "0", v_reference)
    circuit.resistor("R1A", "sensor", "plus", r1)
    circuit.resistor("R2A", "plus", "0", r2 * mismatch)
    circuit.resistor("R1B", "ref", "minus", r1)
    circuit.resistor("R2B", "minus", "out", r2)
    circuit.opamp("U1", plus="plus", minus="minus", out="out", gain=1e5, rails=rails)
    return circuit.dc().v("out")


def source_into_adc(source_volts, source_ohms, adc_ohms, buffered):
    circuit = Circuit()
    circuit.voltage_source("VS", "s", "0", source_volts)
    circuit.resistor("RS", "s", "sensor", source_ohms)
    if buffered:
        circuit.opamp("U1", plus="sensor", minus="adc", out="adc", gain=1e5)
    else:
        circuit.resistor("RWIRE", "sensor", "adc", 1e-3)
    circuit.resistor("RADC", "adc", "0", adc_ohms)
    return circuit.dc().v("adc")


def bridge_output(strain, excitation=5.0, r_gauge=350.0, gauge_factor=2.0):
    delta = r_gauge * gauge_factor * strain
    circuit = Circuit()
    circuit.voltage_source("VEX", "ex", "0", excitation)
    circuit.resistor("R1", "ex", "left", r_gauge)
    circuit.resistor("R2", "left", "0", r_gauge)
    circuit.resistor("R3", "ex", "right", r_gauge)
    circuit.resistor("RG", "right", "0", r_gauge + delta)
    result = circuit.dc()
    return result.v("right", "left"), result.v("left")


def instrumentation_stage(v_plus, v_minus, gain, mismatch=1.0):
    r1 = 1_000.0
    circuit = Circuit()
    circuit.voltage_source("VP", "inp", "0", v_plus)
    circuit.voltage_source("VM", "inm", "0", v_minus)
    circuit.resistor("R1A", "inp", "plus", r1)
    circuit.resistor("R2A", "plus", "0", gain * r1 * mismatch)
    circuit.resistor("R1B", "inm", "minus", r1)
    circuit.resistor("R2B", "minus", "out", gain * r1)
    circuit.opamp("U1", plus="plus", minus="minus", out="out", gain=1e7)
    return circuit.dc().v("out")


def main():
    lsb = VDD / 2 ** ADC_BITS
    print(f"A TMP36-like sensor gives 0.5 V at 0 C and 1.0 V at 50 C; the {ADC_BITS}-bit ADC spans 0 to {VDD} V "
          f"(LSB {lsb * 1e3:.3f} mV)")
    print(f"  raw: 0.5 V of a {VDD} V range is used -> {lsb / 0.010:.3f} C per code")
    r1, r2 = 10_000, 62_000
    gain = r2 / r1
    print(f"  difference amplifier: Vout = (R2 / R1) x (Vsensor - 0.5 V), R2 / R1 = {r2 / 1e3:.0f} k / {r1 / 1e3:.0f} k = {gain:.1f}")
    print(f"  {'temp':>5s} {'sensor':>8s} {'amp out':>8s} {'ideal':>7s}")
    for celsius in [0, 10, 25, 40, 50]:
        sensor = 0.5 + 0.010 * celsius
        out = difference_amplifier(sensor, 0.5, r1, r2)
        print(f"  {celsius:3d} C {sensor:6.3f} V {out:6.3f} V {gain * (sensor - 0.5):5.3f} V")
    print(f"  conditioned: {lsb / (0.010 * gain):.4f} C per code, {gain:.1f} times finer")

    print("\nIf the op-amp runs from 0 V and 3.3 V, outputs beyond its rails are clipped")
    for celsius in [-5, 50, 60]:
        sensor = 0.5 + 0.010 * celsius
        free = difference_amplifier(sensor, 0.5, r1, r2)
        clipped = difference_amplifier(sensor, 0.5, r1, r2, rails=(0.0, VDD))
        print(f"  {celsius:3d} C: ideal {free:6.3f} V, with rails {clipped:6.3f} V")

    print("\nA high-impedance source (1.000 V behind 100 kohm) into an ADC that looks like 1 Mohm")
    direct = source_into_adc(1.0, 100_000, 1e6, buffered=False)
    buffered = source_into_adc(1.0, 100_000, 1e6, buffered=True)
    print(f"  direct: {direct:.4f} V (error {(direct - 1) * 100:+.2f}%), through a voltage follower: {buffered:.5f} V")

    print("\nStrain gauge in a Wheatstone bridge (350 ohm, gauge factor 2, 5 V excitation)")
    print(f"  {'strain':>10s} {'bridge out':>11s} {'formula':>9s} {'x 400 amp':>10s}")
    for microstrain in [0, 250, 500, 1000]:
        strain = microstrain * 1e-6
        diff, common = bridge_output(strain)
        amplified = instrumentation_stage(common + diff, common, 400)
        formula = 5.0 * 2.0 * strain / 4
        print(f"  {microstrain:6d} ue {diff * 1e3:8.3f} mV {formula * 1e3:7.3f} mV {amplified:8.3f} V")
    _, common = bridge_output(0.0)
    print(f"  both bridge outputs sit near {common:.2f} V: that common-mode voltage must NOT be amplified")
    for mismatch in [1.0, 1.001, 1.01]:
        error = instrumentation_stage(common, common, 400, mismatch)
        print(f"  resistor ratio off by {(mismatch - 1) * 100:4.1f}%: output with zero strain = {error * 1e3:8.2f} mV "
              f"(equivalent to {error / 400 / (5.0 * 2.0 / 4) * 1e6:6.1f} microstrain)")


if __name__ == "__main__":
    main()
