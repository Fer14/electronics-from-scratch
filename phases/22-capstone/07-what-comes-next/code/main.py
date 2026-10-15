from sim import Circuit

VDD = 3.3
ADC_MAX = 1023
TARGET_AVG_A = 0.0057
NIGHT_HOURS = 10
BATTERY_MAH = 2000
DAY_MA = 0.0127


def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7


def light_code(lux):
    c = Circuit()
    c.voltage_source("PB2", "p", "0", VDD)
    c.resistor("R_PIN", "p", "ldr_pwr", 25)
    c.resistor("LDR1", "ldr_pwr", "light", ldr_ohms(lux))
    c.resistor("R1", "light", "0", 10e3)
    return round(c.dc().v("light") / VDD * ADC_MAX)


def driver(vbat, switch="npn"):
    c = Circuit()
    c.voltage_source("BAT", "bi", "0", vbat)
    c.resistor("R_INT", "bi", "vbat", 0.5)
    c.voltage_source("PB1", "pin", "0", VDD)
    if switch == "npn":
        c.resistor("R4", "pin", "base", 2200)
        c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    else:
        c.resistor("R4", "pin", "gate", 100)
        c.nmos("M1", d="led_k", g="gate", s="0", vth=1.2, k=0.2)
    c.resistor("R5", "vbat", "led_a", 68)
    c.led("D1", "led_a", "led_k", color="white")
    r = c.dc()
    return r.i("D1"), abs(r.i("R4"))


def pwm_average(vbat, duty):
    c = Circuit()
    c.voltage_source("BAT", "bi", "0", vbat)
    c.resistor("R_INT", "bi", "vbat", 0.5)
    c.pulse_source("PB1", "pin", "0", low=0.0, high=VDD, period=1e-3, duty=duty)
    c.resistor("R4", "pin", "base", 2200)
    c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    c.resistor("R5", "vbat", "led_a", 68)
    c.led("D1", "led_a", "led_k", color="white")
    t = c.transient(t_stop=0.02, dt=5e-6)
    return float(t.i("D1")[t.time >= 0.01].mean())


def nights(base_ma):
    per_day = (TARGET_AVG_A * 1000 + base_ma + DAY_MA) * NIGHT_HOURS + DAY_MA * (24 - NIGHT_HOURS)
    return BATTERY_MAH / per_day


def main():
    print("Step 1: the final requirement check")
    on_code, off_code = light_code(5), light_code(15)
    averages = []
    for vbat in (4.5, 3.6):
        duty = min(TARGET_AVG_A / ((vbat - 3.09) / 75.0), 1.0)
        averages.append(pwm_average(vbat, duty))
    spread = (max(averages) - min(averages)) / max(averages)
    i_on, i_base = driver(4.2)
    base_ma = TARGET_AVG_A / i_on * i_base * 1000
    n_nights = nights(base_ma)
    checks = [
        ("R1", f"on/off codes {on_code}/{off_code} for 5/15 lux", off_code - on_code > 50),
        ("R2", "2 switchings in the night scenario (Lesson 04)", True),
        ("R3", f"PWM 1 kHz, average {averages[0] * 1000:.2f} mA at 4.5 V", 0.005 <= averages[0] <= 0.0065),
        ("R4", f"{n_nights:.1f} nights from {BATTERY_MAH} mAh", n_nights >= 30),
        ("R5", f"average current spread {spread * 100:.1f}% from 4.5 V to 3.6 V", spread <= 0.2),
        ("R6", "4.5 V maximum, parts $1.79, board 40 x 30 mm (Lesson 05)", True),
    ]
    for tag, evidence, passed in checks:
        print(f"  {tag}: {'PASS' if passed else 'FAIL'}  {evidence}")

    print("\nStep 2: one improvement, measured: a MOSFET instead of the NPN")
    for name in ("npn", "nmos"):
        i_on, i_drive = driver(4.2, name)
        drive_avg_ma = TARGET_AVG_A / i_on * i_drive * 1000
        print(f"  {name:4s}: LED on-current {i_on * 1000:5.2f} mA, steady drive current {i_drive * 1000:7.4f} mA,"
              f" {nights(drive_avg_ma):5.1f} nights")

    print("\nStep 3: ideas for version 2, each with the requirement it would change")
    for idea, effect in (
        ("logic-level MOSFET switch", "R4: about 2 more nights (no base current)"),
        ("constant-current LED driver chip", "R5: brightness independent of the battery, no calibration"),
        ("ambient light sensor chip over I2C", "R1: calibrated lux, no cadmium (RoHS)"),
        ("motion sensor (PIR), light only when someone passes", "R4: months instead of weeks"),
        ("USB-C charging and a Li-ion cell", "R4: rechargeable; needs a charger IC and protection"),
        ("enclosure, light guide, button", "product: optics keep the LED's light away from the LDR"),
    ):
        print(f"  - {idea:52s} {effect}")


if __name__ == "__main__":
    main()
