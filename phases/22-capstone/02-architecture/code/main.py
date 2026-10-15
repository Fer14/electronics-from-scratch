from sim import Circuit

R_INTERNAL = 0.5
R_LED = 68.0
R_BASE = 2_200.0
PIN_OHMS = 25.0
VDD = 3.3
BATTERY_MAH = 2000
NIGHT_HOURS = 10
NIGHT_DUTY = 0.3
TARGET_AVG_A = NIGHT_DUTY * 0.019

SLEEP_CURRENTS_UA = {
    "microcontroller asleep, watchdog running": 4.0,
    "LDO quiescent current": 1.6,
    "battery-sense divider (2 x 470 kOhm)": 4.5 / 940e3 * 1e6,
}

WAKE = {"period_s": 1.0, "awake_s": 0.002, "mcu_active_ma": 1.0, "ldr_divider_ma": 3.3 / 20e3 * 1000}


def led_on_current(vbat):
    c = Circuit()
    c.voltage_source("BAT", "bat_ideal", "0", vbat)
    c.resistor("R_INT", "bat_ideal", "vbat", R_INTERNAL)
    c.voltage_source("PIN", "pin_ideal", "0", VDD)
    c.resistor("R_PIN", "pin_ideal", "pin", PIN_OHMS)
    c.resistor("R_BASE", "pin", "base", R_BASE)
    c.npn("Q1", c="col", b="base", e="0", beta=100)
    c.resistor("R_LED", "vbat", "led_a", R_LED)
    c.led("D1", "led_a", "col", color="white")
    r = c.dc()
    return r.i("D1"), r.i("R_BASE"), r.v("vbat")


def average_currents_ma(night_led_avg_ma, base_avg_ma):
    sleep_ma = sum(SLEEP_CURRENTS_UA.values()) / 1000
    wake_fraction = WAKE["awake_s"] / WAKE["period_s"]
    wake_ma = wake_fraction * (WAKE["mcu_active_ma"] + WAKE["ldr_divider_ma"])
    day = sleep_ma + wake_ma
    night = day + night_led_avg_ma + base_avg_ma
    return sleep_ma, wake_ma, day, night


def nights_from(capacity_mah, day_ma, night_ma):
    per_day = night_ma * NIGHT_HOURS + day_ma * (24 - NIGHT_HOURS)
    return capacity_mah / per_day, per_day


def main():
    print("Step 1: the blocks")
    for line in (
        "  3 x AA (4.5 V) --+--> LDO 3.3 V --> microcontroller (ADC, PWM, sleep timer)",
        "                   |                     |  PB2 powers the LDR divider -> ADC0",
        "                   |                     |  ADC1 <- battery divider 470k / 470k",
        "                   |                     +- PB1 PWM -> 2.2 k -> NPN base",
        "                   +--> 68 Ohm -> white LED -> NPN collector (low-side switch)",
    ):
        print(line)

    print("\nStep 2: sleep and wake currents")
    for name, ua in SLEEP_CURRENTS_UA.items():
        print(f"  {name:42s} {ua:6.2f} uA")
    sleep_ma, wake_ma, day_ma, _ = average_currents_ma(0, 0)
    print(f"  waking {WAKE['awake_s'] * 1000:.0f} ms every {WAKE['period_s']:.0f} s"
          f" (MCU {WAKE['mcu_active_ma']:.1f} mA + LDR divider {WAKE['ldr_divider_ma']:.3f} mA):"
          f" {wake_ma * 1000:.2f} uA on average")
    print(f"  daytime average: {day_ma * 1000:.2f} uA")

    print("\nStep 3: LED current with the transistor fully on, as the battery runs down (simulated)")
    print(f"  {'battery':>8s} {'at terminals':>13s} {'LED on':>8s} {'base':>8s} {'duty for 5.7 mA':>16s}")
    led_at = {}
    for vbat in (4.5, 4.2, 3.9, 3.6):
        i_led, i_base, v_term = led_on_current(vbat)
        led_at[vbat] = (i_led, i_base)
        duty = TARGET_AVG_A / i_led
        print(f"  {vbat:6.1f} V {v_term:11.3f} V {i_led * 1000:6.2f}mA {i_base * 1000:6.2f}mA {duty * 100:14.1f}%")

    print("\nStep 4: battery life of the chosen architecture")
    i_led, i_base = led_at[4.2]
    duty = TARGET_AVG_A / i_led
    _, _, day_ma, night_ma = average_currents_ma(TARGET_AVG_A * 1000, duty * i_base * 1000)
    nights, per_day = nights_from(BATTERY_MAH, day_ma, night_ma)
    print(f"  night average {night_ma:.3f} mA, day average {day_ma * 1000:.1f} uA, {per_day:.1f} mAh per day")
    print(f"  -> {nights:.0f} nights from {BATTERY_MAH} mAh")
    shares = {"LED": TARGET_AVG_A * 1000 * NIGHT_HOURS, "transistor base": duty * i_base * 1000 * NIGHT_HOURS,
              "everything else": day_ma * 24}
    for name, mah in shares.items():
        print(f"     {name:16s} {mah:6.2f} mAh per day ({mah / per_day * 100:5.1f}%)")

    print("\nStep 5: other architectures and batteries, same light")
    analog_divider_ma = 3.3 / 20e3 * 1000
    analog_night_ma = 19.0 + analog_divider_ma
    options = [
        ("3 x AA, our design", 2000, day_ma, night_ma),
        ("3 x AA, analog LDR + transistor, full brightness", 2000, analog_divider_ma, analog_night_ma),
        ("1 x Li-ion 18650 (needs a charger, other R_LED)", 2500, day_ma, night_ma),
        ("1 x CR2032 coin cell (cannot give 19 mA pulses well)", 220, day_ma, night_ma),
    ]
    for name, capacity, d, n in options:
        count, _ = nights_from(capacity, d, n)
        print(f"  {name:52s}: {count:5.1f} nights")
    print(f"  (the analog version's LDR divider alone draws {analog_divider_ma:.3f} mA day and night)")


if __name__ == "__main__":
    main()
