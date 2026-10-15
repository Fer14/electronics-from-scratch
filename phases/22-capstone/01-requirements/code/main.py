from pathlib import Path

from sim import Circuit
from sim.lab import evaluate, load_task

VDD = 3.3
ADC_BITS = 10
R_FIXED = 10_000
LUX_ON = 5.0
LUX_OFF = 15.0
LED_TARGET_A = 0.019
NIGHT_DUTY = 0.3
NIGHT_HOURS = 10
BATTERY_MAH = 2000
MIN_NIGHTS = 30

REQUIREMENTS = [
    ("R1", "turns the light on when the room gets dark", f"on below {LUX_ON:.0f} lux, off above {LUX_OFF:.0f} lux"),
    ("R2", "never flickers at dusk or when a car's headlights pass", "hysteresis of 3x in lux, decisions on a 4 s average"),
    ("R3", "gives a soft, even light", f"white LED at about {NIGHT_DUTY * 100:.0f}% of {LED_TARGET_A * 1000:.0f} mA, PWM above 200 Hz"),
    ("R4", "runs a month on one set of batteries", f"3 x AA ({BATTERY_MAH} mAh), at least {MIN_NIGHTS} nights of {NIGHT_HOURS} h"),
    ("R5", "keeps the same brightness as the batteries run down", "LED average current within 20% from 4.5 V to 3.6 V"),
    ("R6", "is safe and cheap", "below 5 V everywhere, parts under $3, board under 40 x 30 mm"),
]


def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7


def divider(lux, r_fixed=R_FIXED):
    c = Circuit()
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.resistor("LDR", "vdd", "sense", ldr_ohms(lux))
    c.resistor("R_FIX", "sense", "0", r_fixed)
    return c.dc().v("sense")


def adc_code(volts):
    return int(round(volts / VDD * (2 ** ADC_BITS - 1)))


def main():
    print("Step 1: what the user wants, and what we will measure")
    for tag, need, spec in REQUIREMENTS:
        print(f"  {tag}: {need:52s} -> {spec}")

    print("\nStep 2: the light levels in the world (lux)")
    for name, lux in (("summer sunlight", 50_000), ("office", 400), ("living room evening", 100),
                      ("dusk", 15), ("dark room, street light outside", 5), ("moonlight", 0.2)):
        print(f"  {name:32s} {lux:>8,.1f} lux -> LDR {ldr_ohms(lux) / 1000:9.2f} kOhm")

    print("\nStep 3: the sensor divider at the two thresholds (simulated)")
    for name, lux in (("switch-on", LUX_ON), ("switch-off", LUX_OFF)):
        v = divider(lux)
        print(f"  {name:10s} {lux:4.0f} lux: LDR {ldr_ohms(lux) / 1000:5.2f} kOhm,"
              f" sense {v:.3f} V, ADC code {adc_code(v)} of {2 ** ADC_BITS - 1}")
    print(f"  the on and off codes are {adc_code(divider(LUX_OFF)) - adc_code(divider(LUX_ON))} codes apart: room for noise")

    print("\nStep 4: the energy budget behind R4")
    night_ma = NIGHT_DUTY * LED_TARGET_A * 1000
    day_ma = 0.01
    per_day_mah = night_ma * NIGHT_HOURS + day_ma * (24 - NIGHT_HOURS)
    nights = BATTERY_MAH / per_day_mah
    print(f"  LED average {night_ma:.1f} mA for {NIGHT_HOURS} h + about {day_ma * 1000:.0f} uA the rest of the day")
    print(f"  {per_day_mah:.1f} mAh per day -> {nights:.0f} nights from {BATTERY_MAH} mAh"
          f" ({'meets' if nights >= MIN_NIGHTS else 'misses'} the {MIN_NIGHTS}-night target)")
    budget = BATTERY_MAH / MIN_NIGHTS
    print(f"  to last {MIN_NIGHTS} nights we may spend at most {budget:.1f} mAh per day")

    print("\nStep 5: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        results = evaluate(task, {"S1": part})
        summary = ", ".join(f"{r['label']}: {r['value']:.4g}" for r in results)
        print(f"  R_FIX {part['ohms']:>7,.0f} Ohm: {summary} -> {'PASS' if all(r['passed'] for r in results) else 'fail'}")


if __name__ == "__main__":
    main()
