import math
from pathlib import Path

import numpy as np

from sim import Circuit
from sim.lab import evaluate, load_task

AMBIENT_C = 25.0

ALLOYS = [
    ("Sn63Pb37 (leaded, eutectic)", 183, 183),
    ("SAC305 (Sn96.5 Ag3.0 Cu0.5)", 217, 220),
    ("Sn99.3 Cu0.7", 227, 227),
]

PADS = {
    "0402 pad": (0.50, 0.60),
    "0603 pad": (0.80, 0.90),
    "0805 pad": (1.00, 1.30),
    "QFN 0.5 mm pitch pin": (0.25, 0.70),
}

OVEN_ZONES = [(0, 25), (60, 150), (150, 190), (200, 250), (230, 250), (260, 150), (330, 50)]


def paste_volume(width_mm, length_mm, stencil_mm=0.12):
    aperture = width_mm * length_mm
    walls = 2 * (width_mm + length_mm) * stencil_mm
    return aperture * stencil_mm, aperture / walls


def oven_temperature(t):
    times = [z[0] for z in OVEN_ZONES]
    temps = [z[1] for z in OVEN_ZONES]
    return np.interp(t, times, temps)


def reflow(tau_s, dt=0.1, t_end=330.0):
    t = np.arange(0.0, t_end + dt, dt)
    temp = np.empty_like(t)
    temp[0] = AMBIENT_C
    for n in range(1, len(t)):
        temp[n] = temp[n - 1] + dt * (oven_temperature(t[n - 1]) - temp[n - 1]) / tau_s
    return t, temp


def iron_on_pad(link_k_per_w, seconds=6.0):
    c = Circuit()
    c.voltage_source("IRON", "tip", "0", 350.0 - AMBIENT_C)
    c.resistor("R_TIP", "tip", "joint", 15.0)
    c.capacitor("C_JOINT", "joint", "0", 0.02)
    c.resistor("S1", "joint", "plane", link_k_per_w)
    c.capacitor("C_PLANE", "plane", "0", 3.0)
    c.resistor("R_PLANE", "plane", "0", 10.0)
    return c.transient(t_stop=seconds, dt=2e-3)


def cracked_joint(joint_ohms):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 5.0)
    c.resistor("R1", "vcc", "a", 330)
    c.resistor("JOINT", "a", "b", joint_ohms)
    c.led("D1", "b", "0", color="red")
    return c.dc().i("D1")


def main():
    print("Step 1: solder alloys (solidus / liquidus, C)")
    for name, solidus, liquidus in ALLOYS:
        print(f"  {name:30s} {solidus} / {liquidus} C")

    print("\nStep 2: solder paste through a 0.12 mm stencil")
    for name, (w, l) in PADS.items():
        volume, ratio = paste_volume(w, l)
        verdict = "releases well" if ratio >= 0.66 else "may stick in the stencil"
        print(f"  {name:22s} {w:.2f} x {l:.2f} mm: paste {volume * 1000:6.1f} nL,"
              f" area ratio {ratio:.2f} ({verdict})")

    print("\nStep 3: reflow profile seen by a small and a large part")
    for name, tau in (("small 0402 resistor", 15.0), ("large connector", 45.0)):
        t, temp = reflow(tau)
        above = (temp >= 217).sum() * (t[1] - t[0])
        print(f"  {name:20s} (tau {tau:4.0f} s): peak {temp.max():5.1f} C,"
              f" {above:5.1f} s above 217 C")

    print("\nStep 4: a soldering iron on a pad joined to a ground plane")
    print("  (thermal circuit: volts = C above 25 C, amps = W, ohms = K/W, farads = J/K)")
    for link in (2.0, 8.0, 25.0):
        t = iron_on_pad(link)
        melt = t.time_to_cross("joint", 217 - AMBIENT_C)
        final = t.v("joint")[-1] + AMBIENT_C
        when = f"melts after {melt:4.2f} s" if math.isfinite(melt) else "never melts"
        print(f"  pad-to-plane link {link:4.1f} K/W: joint reaches {final:5.1f} C after 6 s, {when}")

    print("\nStep 5: a cracked joint in series with an LED")
    for ohms in (0.001, 10.0, 100.0, 1000.0):
        print(f"  joint resistance {ohms:8.3f} Ohm -> LED current {cracked_joint(ohms) * 1000:5.2f} mA")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        result = evaluate(task, {"S1": part})[0]
        verdict = "PASS" if result["passed"] else "fail"
        print(f"  link {part['ohms']:4.1f} K/W: time to melt {result['value']:.2f} s -> {verdict}")


if __name__ == "__main__":
    main()
