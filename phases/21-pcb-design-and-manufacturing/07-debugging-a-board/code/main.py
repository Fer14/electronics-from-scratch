import math
from pathlib import Path

from sim import Circuit
from sim.lab import evaluate, load_task

NODES = ("rail", "mid", "led_a")

GOOD = {"R1": 220.0, "R2": 10e3, "R3": 10e3, "R4": 330.0, "Z1": "normal", "D1": "normal"}

FAULTS = {
    "board is good": {},
    "R3 shorted by a solder bridge": {"R3": 1e-3},
    "R3 joint cracked (open)": {"R3": 1e12},
    "R3 loaded with 1 kOhm by mistake": {"R3": 1e3},
    "R2 loaded with 1 kOhm by mistake": {"R2": 1e3},
    "R1 joint cracked (open)": {"R1": 1e12},
    "Z1 missing": {"Z1": "missing"},
    "D1 (LED) soldered backwards": {"D1": "reversed"},
    "R4 joint cracked (open)": {"R4": 1e12},
}


def board(values, powered=True, ohmmeter_at=None):
    c = Circuit()
    if powered:
        c.voltage_source("B1", "vin", "0", 9.0)
    c.resistor("R1", "vin", "rail", values["R1"])
    if values["Z1"] == "normal":
        c.zener("Z1", "0", "rail", vz=5.1)
    c.resistor("R2", "rail", "mid", values["R2"])
    c.resistor("R3", "mid", "0", values["R3"])
    c.resistor("R4", "rail", "led_a", values["R4"])
    if values["D1"] == "normal":
        c.led("D1", "led_a", "0", color="red")
    else:
        c.led("D1", "0", "led_a", color="red")
    if ohmmeter_at:
        c.current_source("OHM", "0", ohmmeter_at, 1e-4)
    return c


def voltages(values):
    r = board(values).dc()
    return {node: r.v(node) for node in NODES}


def ohms_to_ground(values, node):
    r = board(values, powered=False, ohmmeter_at=node).dc()
    return r.v(node) / 1e-4


def with_fault(fault):
    return {**GOOD, **fault}


def diagnose(measured, dictionary):
    scores = []
    for name, expected in dictionary.items():
        error = math.sqrt(sum((measured[n] - expected[n]) ** 2 for n in NODES))
        scores.append((error, name))
    return sorted(scores)


def main():
    print("Step 1: bring-up order")
    for n, step in enumerate([
        "look: orientation of D1 and Z1, solder bridges, missing parts",
        "power off: resistance from each rail to ground (looking for shorts)",
        "power on through a current-limited supply, watch the current",
        "measure every rail, then every important node, and compare with simulation",
        "only then load firmware or connect anything expensive",
    ], start=1):
        print(f"  {n}. {step}")

    print("\nStep 2: what a good board should measure (simulation)")
    golden = voltages(GOOD)
    for node in NODES:
        print(f"  V({node:5s}) = {golden[node]:6.3f} V")

    print("\nStep 3: power-off resistance from node mid to ground (ohmmeter injects 0.1 mA)")
    for name in ("board is good", "R3 shorted by a solder bridge"):
        print(f"  {name:32s}: {ohms_to_ground(with_fault(FAULTS[name]), 'mid'):10.1f} Ohm")

    print("\nStep 4: the fault dictionary (simulated node voltages)")
    dictionary = {name: voltages(with_fault(fault)) for name, fault in FAULTS.items()}
    print(f"  {'fault':34s} " + " ".join(f"{n:>7s}" for n in NODES))
    for name, v in dictionary.items():
        print(f"  {name:34s} " + " ".join(f"{v[n]:7.3f}" for n in NODES))

    print("\nStep 5: diagnose three boards from their multimeter readings")
    readings = {
        "board A": {"rail": 5.09, "mid": 0.46, "led_a": 1.85},
        "board B": {"rail": 5.14, "mid": 2.56, "led_a": 5.12},
        "board C": {"rail": 6.08, "mid": 3.05, "led_a": 1.86},
    }
    for label, measured in readings.items():
        ranked = diagnose(measured, dictionary)
        print(f"  {label}: measured " + ", ".join(f"{n}={measured[n]:.2f} V" for n in NODES))
        for error, name in ranked[:3]:
            print(f"     distance {error:6.3f} V  {name}")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        results = evaluate(task, {"S1": part})
        values = ", ".join(f"{r['label']}: {r['value']:.3f} V" for r in results)
        verdict = "PASS" if all(r["passed"] for r in results) else "fail"
        print(f"  {part}: {values} -> {verdict}")


if __name__ == "__main__":
    main()
