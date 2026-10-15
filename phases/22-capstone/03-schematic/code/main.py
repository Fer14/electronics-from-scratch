from pathlib import Path

from sim import Circuit
from sim.lab import evaluate, load_task

VDD = 3.3
ADC_MAX = 1023
R_INTERNAL = 0.5
PIN_OHMS = 25.0

PARTS = {
    "BT1": "3 x AA holder, 4.5 V",
    "U1": "LDO 3.3 V (MCP1700-3302, SOT-23)",
    "C1": "1 uF ceramic, LDO input",
    "C2": "1 uF ceramic, LDO output",
    "C3": "100 nF ceramic, microcontroller decoupling",
    "U2": "8-pin microcontroller (ATtiny-class, SOIC-8)",
    "LDR1": "photoresistor, 10 kOhm at 10 lux",
    "R1": "10 kOhm, LDR divider",
    "R2": "470 kOhm, battery divider top",
    "R3": "470 kOhm, battery divider bottom",
    "C4": "100 nF, battery-sense ADC input",
    "R4": "2.2 kOhm, NPN base",
    "Q1": "NPN switch (MMBT3904, SOT-23)",
    "R5": "68 Ohm, LED current",
    "D1": "white LED",
}

NETS = {
    "VBAT": ["BT1.+", "U1.IN", "C1.1", "R2.1", "R5.1"],
    "VDD": ["U1.OUT", "C2.1", "C3.1", "U2.VCC"],
    "LDR_PWR": ["U2.PB2", "LDR1.1"],
    "LIGHT": ["LDR1.2", "R1.1", "U2.ADC0"],
    "BAT_SENSE": ["R2.2", "R3.1", "C4.1", "U2.ADC1"],
    "PWM": ["U2.PB1", "R4.1"],
    "BASE": ["R4.2", "Q1.B"],
    "LED_A": ["R5.2", "D1.A"],
    "LED_K": ["D1.K", "Q1.C"],
    "GND": ["BT1.-", "U1.GND", "C1.2", "C2.2", "C3.2", "U2.GND", "R1.2", "R3.2", "C4.2", "Q1.E"],
}


def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7


def night_light(lux, vbat, pwm_high):
    c = Circuit("night light")
    c.voltage_source("BAT", "bat_ideal", "0", vbat)
    c.resistor("R_INT", "bat_ideal", "vbat", R_INTERNAL)
    c.voltage_source("U1", "vdd", "0", VDD)
    c.voltage_source("PB2", "pb2_ideal", "0", VDD)
    c.resistor("R_PB2", "pb2_ideal", "ldr_pwr", PIN_OHMS)
    c.resistor("LDR1", "ldr_pwr", "light", ldr_ohms(lux))
    c.resistor("R1", "light", "0", 10e3)
    c.resistor("R2", "vbat", "bat_sense", 470e3)
    c.resistor("R3", "bat_sense", "0", 470e3)
    c.voltage_source("PB1", "pb1_ideal", "0", VDD if pwm_high else 0.0)
    c.resistor("R_PB1", "pb1_ideal", "pwm", PIN_OHMS)
    c.resistor("R4", "pwm", "base", 2.2e3)
    c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    c.resistor("R5", "vbat", "led_a", 68)
    c.led("D1", "led_a", "led_k", color="white")
    return c.dc()


def code(volts):
    return int(round(volts / VDD * ADC_MAX))


def main():
    print("Step 1: bill of materials")
    for ref, what in PARTS.items():
        print(f"  {ref:5s} {what}")

    print("\nStep 2: netlist (every pin on every net)")
    for net, pins in NETS.items():
        print(f"  {net:9s} {', '.join(pins)}")
    all_pins = [p for pins in NETS.values() for p in pins]
    print(f"  {len(NETS)} nets, {len(all_pins)} pin connections, no pin on two nets: {len(all_pins) == len(set(all_pins))}")

    print("\nStep 3: the light input across the day (battery 4.2 V, LED off)")
    for lux in (0.2, 1, 5, 10, 15, 50, 400):
        r = night_light(lux, 4.2, False)
        v = r.v("light")
        print(f"  {lux:6.1f} lux: LDR {ldr_ohms(lux) / 1000:7.2f} kOhm, ADC0 {v:.3f} V = code {code(v):4d}")

    print("\nStep 4: the battery input")
    for vbat in (4.5, 4.2, 3.9, 3.6):
        r = night_light(10, vbat, False)
        v = r.v("bat_sense")
        print(f"  battery {vbat:.1f} V: ADC1 {v:.3f} V = code {code(v)}, divider current {r.i('R2') * 1e6:.2f} uA")

    print("\nStep 5: the LED driver, PWM pin high (worst case: fresh battery)")
    r = night_light(1, 4.5, True)
    i_led = r.i("D1")
    p_r5 = r.p("R5")
    p_q = r.v("led_k") * i_led
    print(f"  LED current {i_led * 1000:.2f} mA, LED voltage {r.v('led_a', 'led_k'):.3f} V")
    print(f"  base current {r.i('R4') * 1000:.3f} mA (forced beta {i_led / r.i('R4'):.1f}), V_CE {r.v('led_k') * 1000:.0f} mV")
    print(f"  R5 dissipates {p_r5 * 1000:.1f} mW (0805 rating 125 mW), Q1 {p_q * 1000:.2f} mW (rating about 225 mW)")
    print(f"  pin PB1 sources {r.i('R4') * 1000:.2f} mA (limit about 20 mA)")
    r_off = night_light(1, 4.5, False)
    print(f"  PWM pin low: LED current {r_off.i('D1') * 1e9:.2f} nA (off)")

    print("\nStep 6: requirement checks")
    on_code, off_code = code(night_light(5, 4.2, False).v("light")), code(night_light(15, 4.2, False).v("light"))
    print(f"  R1: on threshold code {on_code}, off threshold code {off_code}")
    node_max = max(abs(night_light(1, 4.5, True).v(n)) for n in ("vbat", "vdd", "light", "bat_sense", "pwm", "base", "led_a", "led_k"))
    print(f"  R6: highest node voltage {node_max:.2f} V (below 5 V: {node_max < 5})")

    print("\nStep 7: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        results = evaluate(task, {"S1": part})
        line = ", ".join(f"{res['label']}: {res['value'] * 1000:.2f} mA" for res in results)
        print(f"  R4 = {part['ohms']:>7,.0f} Ohm: {line} -> {'PASS' if all(x['passed'] for x in results) else 'fail'}")


if __name__ == "__main__":
    main()
