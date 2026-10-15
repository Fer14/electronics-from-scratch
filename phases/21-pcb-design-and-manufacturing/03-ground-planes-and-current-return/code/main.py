import json
import math
from pathlib import Path

from sim import Circuit

MU0 = 4e-7 * math.pi


def plane_return_fraction(height_m, half_width_m):
    return 2 / math.pi * math.atan(half_width_m / height_m)


def wire_pair_inductance(length_m, spacing_m, radius_m):
    return MU0 * length_m / math.pi * math.log(spacing_m / radius_m)


def wire_over_plane_inductance(length_m, height_m, radius_m):
    return MU0 * length_m / (2 * math.pi) * math.log(2 * height_m / radius_m)


def shared_ground(shared_ohms):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 5.0)
    c.resistor("RL", "vcc", "ret", 4.7)
    c.resistor("R_TOP", "vcc", "sense", 10e3)
    c.resistor("R_BOT", "sense", "ret", 10e3)
    c.resistor("S1", "ret", "0", shared_ohms)
    return c.dc()


def star_ground(load_ohms, sensor_ohms):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 5.0)
    c.resistor("RL", "vcc", "ret", 4.7)
    c.resistor("R_LOAD_GND", "ret", "0", load_ohms)
    c.resistor("R_TOP", "vcc", "sense", 10e3)
    c.resistor("R_BOT", "sense", "sgnd", 10e3)
    c.resistor("R_SENSOR_GND", "sgnd", "0", sensor_ohms)
    return c.dc()


def supply_droop(decoupling_farads):
    c = Circuit()
    c.voltage_source("V1", "bat", "0", 5.0)
    c.resistor("R_LEADS", "bat", "mid", 0.05)
    c.inductor("L_LEADS", "mid", "vdd", 0.5e-6)
    c.resistor("R_LOAD", "vdd", "sw", 5.0)
    c.switch("S_LOAD", "sw", "0", closed=False, toggle_at=(5e-6,))
    if decoupling_farads:
        c.capacitor("C_DEC", "vdd", "0", decoupling_farads)
    t = c.transient(t_stop=60e-6, dt=20e-9, initial="dc")
    return t


def main():
    print("Step 1: where does the return current flow in a plane under a trace?")
    for h_mm in (0.2, 1.6):
        for half_mm in (0.5, 2.0, 5.0):
            share = plane_return_fraction(h_mm * 1e-3, half_mm * 1e-3)
            print(f"  trace {h_mm:3.1f} mm above the plane: {share * 100:5.1f}% of the return"
                  f" flows within +/-{half_mm:.1f} mm of the trace")

    print("\nStep 2: loop inductance of 100 mm of supply path")
    pair = wire_pair_inductance(0.1, 20e-3, 0.25e-3)
    two_layer = wire_over_plane_inductance(0.1, 1.6e-3, 0.25e-3)
    four_layer = wire_over_plane_inductance(0.1, 0.2e-3, 0.25e-3)
    print(f"  out-and-back wires 20 mm apart     : {pair * 1e9:6.1f} nH")
    print(f"  trace 1.6 mm over a ground plane   : {two_layer * 1e9:6.1f} nH")
    print(f"  trace 0.2 mm over a ground plane   : {four_layer * 1e9:6.1f} nH")
    for name, inductance in (("wires", pair), ("2-layer", two_layer), ("4-layer", four_layer)):
        spike = inductance * 0.5 / 2e-9
        print(f"  0.5 A switched in 2 ns through {name:7s}: V = L di/dt = {spike:5.2f} V")

    print("\nStep 3: a sensor sharing the load's ground return")
    for shared in (0.2, 0.02, 0.002):
        r = shared_ground(shared)
        print(f"  shared return {shared * 1000:6.1f} mOhm: load current {r.i('RL'):.3f} A,"
              f" ground lifted by {r.v('ret') * 1000:6.1f} mV, ADC reads {r.v('sense'):.4f} V")
    r = star_ground(0.2, 0.2)
    print(f"  star ground (two separate 200 mOhm returns): ADC reads {r.v('sense'):.4f} V")

    print("\nStep 4: supply droop when a 1 A load switches on at t = 5 us")
    for farads in (0.0, 1e-6, 10e-6, 100e-6):
        t = supply_droop(farads)
        vdd = t.v("vdd")
        after = t.time >= 5e-6
        label = "no capacitor" if not farads else f"{farads * 1e6:5.0f} uF"
        print(f"  {label:>12s}: lowest vdd {vdd[after].min():.3f} V,"
              f" droop {(5.0 - vdd[after].min()) * 1000:6.0f} mV")
    for farads in (1e-6, 10e-6, 100e-6):
        z0 = math.sqrt(0.5e-6 / farads)
        print(f"  estimate I * sqrt(L/C) for {farads * 1e6:5.0f} uF: {1.0 * z0 * 1000:5.0f} mV")

    task = json.loads((Path(__file__).parent.parent / "lab" / "task.json").read_text())
    goal = task["goals"][0]
    print("\nStep 5: check the lab task")
    for part in task["parts"]:
        reading = shared_ground(part["ohms"]).v("sense")
        verdict = "PASS" if goal["min"] <= reading <= goal["max"] else "fail"
        print(f"  shared return {part['ohms']:.3f} Ohm: ADC reads {reading:.4f} V -> {verdict}")


if __name__ == "__main__":
    main()
