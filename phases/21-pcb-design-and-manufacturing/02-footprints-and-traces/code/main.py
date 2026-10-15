import json
from pathlib import Path

from sim import Circuit

RHO_COPPER = 1.72e-8
TEMPCO_COPPER = 0.00393
OZ_TO_METRES = 35e-6
METRES_PER_MIL = 25.4e-6

CHIP_SIZES_MM = {
    "0402": (1.0, 0.5),
    "0603": (1.6, 0.8),
    "0805": (2.0, 1.25),
    "1206": (3.2, 1.6),
}

PIN_PITCHES_MM = {
    "DIP (through-hole)": 2.54,
    "SOIC": 1.27,
    "TSSOP": 0.65,
    "QFN (small)": 0.5,
}


def trace_resistance(length_m, width_m, copper_oz=1.0, temperature_c=20.0):
    thickness = copper_oz * OZ_TO_METRES
    rho = RHO_COPPER * (1 + TEMPCO_COPPER * (temperature_c - 20.0))
    return rho * length_m / (width_m * thickness)


def ipc2221_width(current_a, rise_c, copper_oz=1.0, outer=True):
    k = 0.048 if outer else 0.024
    area_mil2 = (current_a / (k * rise_c ** 0.44)) ** (1 / 0.725)
    thickness_mil = copper_oz * OZ_TO_METRES / METRES_PER_MIL
    return area_mil2 / thickness_mil * METRES_PER_MIL


def ipc2221_rise(current_a, width_m, copper_oz=1.0, outer=True):
    k = 0.048 if outer else 0.024
    area_mil2 = (width_m / METRES_PER_MIL) * (copper_oz * OZ_TO_METRES / METRES_PER_MIL)
    return (current_a / (k * area_mil2 ** 0.725)) ** (1 / 0.44)


def heater_through_trace(trace_ohms):
    c = Circuit()
    c.voltage_source("B1", "vcc", "0", 12.0)
    c.resistor("S1", "vcc", "load", trace_ohms)
    c.resistor("RL", "load", "0", 6.0)
    return c.dc()


def main():
    print("Step 1: footprint sizes")
    for code, (length, width) in CHIP_SIZES_MM.items():
        print(f"  chip {code}: {length:.2f} mm x {width:.2f} mm")
    for name, pitch in PIN_PITCHES_MM.items():
        print(f"  {name:20s} pin pitch {pitch:.2f} mm")

    print("\nStep 2: resistance of 100 mm of 1 oz copper (35 um thick)")
    for width_mm in (0.15, 0.25, 0.5, 1.0, 2.0, 5.0):
        r = trace_resistance(0.1, width_mm * 1e-3)
        print(f"  width {width_mm:4.2f} mm -> {r * 1000:7.1f} mOhm ({r * 10:.2f} mOhm per mm)")
    hot = trace_resistance(0.1, 0.25e-3, temperature_c=70.0)
    cold = trace_resistance(0.1, 0.25e-3)
    print(f"  the 0.25 mm trace at 70 C: {hot * 1000:.1f} mOhm ({(hot / cold - 1) * 100:.0f}% more than at 20 C)")

    print("\nStep 3: IPC-2221 minimum width for a 10 C temperature rise")
    print(f"  {'current':>8s} {'outer 1oz':>10s} {'inner 1oz':>10s} {'outer 2oz':>10s}")
    for current in (0.1, 0.5, 1.0, 2.0, 5.0):
        outer = ipc2221_width(current, 10) * 1000
        inner = ipc2221_width(current, 10, outer=False) * 1000
        thick = ipc2221_width(current, 10, copper_oz=2.0) * 1000
        print(f"  {current:6.1f} A {outer:8.2f} mm {inner:8.2f} mm {thick:8.2f} mm")

    print("\nStep 4: how hot does a 0.25 mm outer trace get?")
    for current in (0.25, 0.5, 1.0, 2.0):
        print(f"  {current:4.2f} A -> about {ipc2221_rise(current, 0.25e-3):6.1f} C above the board")

    print("\nStep 5: a 12 V, 6 Ohm heater fed through a 200 mm trace")
    print(f"  {'width':>6s} {'R trace':>9s} {'I':>7s} {'V heater':>9s} {'P trace':>8s}")
    for width_mm in (0.2, 1.0, 3.0):
        r_trace = trace_resistance(0.2, width_mm * 1e-3)
        result = heater_through_trace(r_trace)
        print(f"  {width_mm:4.1f}mm {r_trace * 1000:6.1f} mOhm {result.i('RL'):5.3f} A"
              f" {result.v('load'):7.3f} V {result.p('S1'):6.3f} W")

    task_path = Path(__file__).parent.parent / "lab" / "task.json"
    task = json.loads(task_path.read_text())
    print("\nStep 6: check the lab task with every candidate trace")
    for part in task["parts"]:
        result = heater_through_trace(part["ohms"])
        v_ok = result.v("load") >= task["goals"][0]["min"]
        p_ok = result.p("S1") <= task["goals"][1]["max"]
        verdict = "PASS" if v_ok and p_ok else "fail"
        print(f"  trace of {part['ohms']:.3f} Ohm: V heater {result.v('load'):.3f} V,"
              f" trace power {result.p('S1'):.3f} W -> {verdict}")


if __name__ == "__main__":
    main()
