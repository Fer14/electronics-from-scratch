import math
from pathlib import Path

from sim import Circuit
from sim.lab import evaluate, load_task

VDD = 3.3
NODES = ("vbat", "vdd", "light", "bat_sense", "base", "led_a", "led_k")

GOOD = {"R1": 10e3, "R2": 470e3, "R3": 470e3, "R4": 2.2e3, "R5": 68.0, "LDR": 10e3, "D1": "normal", "Q1": "normal"}

FAULTS = {
    "board is good": {},
    "R5 is 330 Ohm (wrong reel)": {"R5": 330.0},
    "R4 is 22 kOhm (wrong reel)": {"R4": 22e3},
    "D1 soldered backwards": {"D1": "reversed"},
    "Q1 rotated (collector and emitter swapped)": {"Q1": "reversed"},
    "R1 not soldered (open)": {"R1": 1e12},
    "LDR leg cracked (open)": {"LDR": 1e12},
    "R3 not soldered (open)": {"R3": 1e12},
    "solder bridge LED_K to GND": {"bridge": True},
}


def board(values, vbat=4.5, pwm_high=True, powered=True, ohmmeter=None):
    c = Circuit()
    if powered:
        c.voltage_source("BAT", "vbat", "0", vbat)
        c.voltage_source("U1", "vdd", "0", VDD)
        c.voltage_source("PB2", "ldr_pwr", "0", VDD)
        c.voltage_source("PB1", "pwm", "0", VDD if pwm_high else 0.0)
    c.resistor("LDR1", "ldr_pwr", "light", values["LDR"])
    c.resistor("R1", "light", "0", values["R1"])
    c.resistor("R2", "vbat", "bat_sense", values["R2"])
    c.resistor("R3", "bat_sense", "0", values["R3"])
    c.resistor("R4", "pwm", "base", values["R4"])
    if values["Q1"] == "normal":
        c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    else:
        c.npn("Q1", c="0", b="base", e="led_k", beta=100)
    c.resistor("R5", "vbat", "led_a", values["R5"])
    if values["D1"] == "normal":
        c.led("D1", "led_a", "led_k", color="white")
    else:
        c.led("D1", "led_k", "led_a", color="white")
    if values.get("bridge"):
        c.resistor("BRIDGE", "led_k", "0", 1e-3)
    if ohmmeter:
        c.current_source("OHM", "0", ohmmeter, 1e-5)
    return c


def measure(values):
    r = board(values).dc()
    readings = {node: r.v(node) for node in NODES}
    readings["i_led_ma"] = r.i("D1") * 1000
    readings["i_supply_ma"] = (abs(r.i("BAT")) + abs(r.i("PB1")) + abs(r.i("PB2"))) * 1000
    return readings


def resistance_to_ground(values, node):
    r = board(values, powered=False, ohmmeter=node).dc()
    return r.v(node) / 1e-5


def diagnose(measured, dictionary):
    keys = ("light", "bat_sense", "base", "led_a", "led_k")
    ranked = []
    for name, expected in dictionary.items():
        volts = sum((measured[k] - expected[k]) ** 2 for k in keys)
        amps = (0.1 * (measured["i_supply_ma"] - expected["i_supply_ma"])) ** 2
        ranked.append((math.sqrt(volts + amps), name))
    return sorted(ranked)


def main():
    print("Step 1: bring-up plan for the night light")
    for n, step in enumerate([
        "inspect: LED and transistor orientation, solder bridges, missing parts",
        "power off: resistance from VBAT and from VDD to GND",
        "power on from a lab supply at 4.5 V, current limit 50 mA; expect a few uA when asleep",
        "load test firmware that holds PB1 and PB2 high; measure every test point",
        "compare with the golden values below; diagnose any difference",
        "load the real firmware; cover and uncover the LDR; watch the LED and the supply current",
    ], start=1):
        print(f"  {n}. {step}")

    print("\nStep 2: power-off resistance (ohmmeter injects 10 uA)")
    print(f"  VBAT to GND on a good board: {resistance_to_ground(GOOD, 'vbat') / 1000:8.1f} kOhm (the 940 kOhm battery divider)")
    print(f"  LIGHT to GND on a good board: {resistance_to_ground(GOOD, 'light') / 1000:8.1f} kOhm (R1)")
    bridged = dict(GOOD, bridge=True)
    print(f"  LED_K to GND, good board: {resistance_to_ground(GOOD, 'led_k') / 1e6:8.1f} MOhm;"
          f" with a solder bridge: {resistance_to_ground(bridged, 'led_k'):.3f} Ohm")

    print("\nStep 3: golden values (test firmware: PB1 high, PB2 high, LDR at 10 lux = 10 kOhm)")
    golden = measure(GOOD)
    for node in NODES:
        print(f"  V({node:9s}) = {golden[node]:6.3f} V")
    print(f"  LED current = {golden['i_led_ma']:.2f} mA, battery (supply) current = {golden['i_supply_ma']:.2f} mA")

    print("\nStep 4: fault dictionary")
    dictionary = {name: measure(dict(GOOD, **fault)) for name, fault in FAULTS.items()}
    header = " ".join(f"{k:>9s}" for k in ("light", "bat_sense", "base", "led_a", "led_k", "I_supply"))
    print(f"  {'fault':44s} {header}")
    for name, m in dictionary.items():
        row = " ".join(f"{m[k]:9.3f}" for k in ("light", "bat_sense", "base", "led_a", "led_k"))
        print(f"  {name:44s} {row} {m['i_supply_ma']:7.2f}mA")

    print("\nStep 5: three boards from the first batch")
    boards = {
        "board 1, LED very dim": {"light": 1.65, "bat_sense": 2.25, "base": 0.71, "led_a": 3.10, "led_k": 0.05, "i_supply_ma": 5.6},
        "board 2, never turns on at night": {"light": 3.29, "bat_sense": 2.25, "base": 0.74, "led_a": 3.21, "led_k": 0.08, "i_supply_ma": 20.1},
        "board 3, LED dark": {"light": 1.65, "bat_sense": 2.25, "base": 0.68, "led_a": 4.49, "led_k": 0.02, "i_supply_ma": 1.4},
    }
    for label, measured in boards.items():
        ranked = diagnose(measured, dictionary)
        print(f"  {label}: supply current {measured['i_supply_ma']:.1f} mA")
        for distance, name in ranked[:2]:
            print(f"     distance {distance:6.3f} V  {name}")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        results = evaluate(task, {"S1": part})
        line = ", ".join(f"{res['label']}: {res['value']:.4f}" for res in results)
        print(f"  R5 = {part['ohms']:5.0f} Ohm: {line} -> {'PASS' if all(x['passed'] for x in results) else 'fail'}")


if __name__ == "__main__":
    main()
