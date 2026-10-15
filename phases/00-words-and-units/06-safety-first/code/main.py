import numpy as np

BODY_RESISTANCE = {
    "dry": 100_000.0,
    "sweaty": 10_000.0,
    "wet": 1_000.0,
    "broken skin": 500.0,
}

CONDITION_NOTES = {
    "dry": "dry skin, fingertip touch",
    "sweaty": "sweaty hands, firm grip",
    "wet": "wet hands, full grip",
    "broken skin": "cut skin, only the inside",
}

AC_EFFECTS = [
    (0.001, "not felt"),
    (0.005, "a tingle"),
    (0.010, "painful, but you can let go"),
    (0.030, "muscles lock, cannot let go"),
    (0.100, "breathing stops, heart at risk"),
    (np.inf, "heart may fibrillate: deadly"),
]

DC_EFFECTS = [
    (0.002, "not felt"),
    (0.025, "felt, jolt on touch and release"),
    (0.150, "painful, muscle jerks, skin burns"),
    (np.inf, "heart may fibrillate: deadly"),
]

VOLTAGES = [1.5, 9.0, 12.0, 24.0, 50.0, 120.0, 230.0]

COURSE_LIMIT_VOLTS = 12.0

BATTERIES = [
    ("CR2032 coin cell", 3.0, 15.0),
    ("9 V PP3 battery", 9.0, 1.7),
    ("AA alkaline cell", 1.5, 0.15),
    ("18650 Li-ion cell", 3.7, 0.04),
    ("car battery", 12.6, 0.008),
]

CAPACITORS = [
    ("breadboard electrolytic", 100e-6, 12.0),
    ("disposable camera flash", 120e-6, 330.0),
    ("microwave oven", 1e-6, 2100.0),
]


def effect_of(current, effects):
    for limit, description in effects:
        if current < limit:
            return description
    return effects[-1][1]


def body_current(volts, ohms):
    return volts / ohms


def show_body_table():
    print("=== 1. Current through a body, I = V / R (preview of Phase 03) ===")
    for name, ohms in BODY_RESISTANCE.items():
        print(f"  {name:<12} = {CONDITION_NOTES[name]:<26} R ~ {ohms:>9,.0f} Ω")
    print()
    print("  volts " + "".join(f"{name:>14}" for name in BODY_RESISTANCE))
    for volts in VOLTAGES:
        cells = "".join(f"{body_current(volts, ohms) * 1000:>11.3g} mA" for ohms in BODY_RESISTANCE.values())
        marker = "   <- course limit" if volts == COURSE_LIMIT_VOLTS else ""
        print(f"  {volts:>5g}{cells}{marker}")
    print()


def show_effects():
    print("=== 2. What those currents would do, hand to hand (rough; people differ a lot) ===")
    cases = [
        (12.0, "dry"),
        (12.0, "wet"),
        (50.0, "wet"),
        (230.0, "dry"),
        (230.0, "sweaty"),
        (230.0, "wet"),
    ]
    print(f"  {'case':<14} {'current':>10}   {'if DC (battery)':<34} if AC (mains)")
    for volts, condition in cases:
        current = body_current(volts, BODY_RESISTANCE[condition])
        label = f"{volts:g} V, {condition}"
        print(
            f"  {label:<14} {current * 1000:>7.3g} mA   {effect_of(current, DC_EFFECTS):<34} "
            f"{effect_of(current, AC_EFFECTS)}"
        )
    broken_down_ohms = np.array([1000.0, 2000.0])
    mains_currents = 230.0 / broken_down_ohms * 1000
    print(
        f"  but above ~50 V skin breaks down: at 230 V even dry skin falls to ~1-2 kΩ "
        f"-> {mains_currents[1]:.0f}-{mains_currents[0]:.0f} mA, deadly"
    )
    print()


def show_voltage_needed():
    print("=== 3. Voltage needed to push 10 mA ('cannot let go') ===")
    for condition, ohms in BODY_RESISTANCE.items():
        volts = 0.010 * ohms
        print(f"  {condition:<12} R = {ohms:>9,.0f} Ω  ->  V = 0.010 A x {ohms:,.0f} Ω = {volts:g} V")
    print()


def show_battery_shorts():
    print("=== 4. Short-circuiting a battery: current and heat inside it ===")
    for name, volts, internal_ohms in BATTERIES:
        current = volts / internal_ohms
        heat_watts = current**2 * internal_ohms
        print(f"  {name:<20} {volts:>5g} V, r = {internal_ohms:>6g} Ω  ->  I = {current:8.1f} A, heat = {heat_watts:8.1f} W")
    print()


def show_capacitors():
    print("=== 5. Charge left in capacitors after unplugging (touched with sweaty hands, 10 kΩ) ===")
    body_ohms = BODY_RESISTANCE["sweaty"]
    for name, farads, volts in CAPACITORS:
        energy = 0.5 * farads * volts**2
        first_current = volts / body_ohms
        time_constant = body_ohms * farads
        print(
            f"  {name:<24} {farads * 1e6:>6g} µF at {volts:>6g} V: energy = {energy:7.3g} J, "
            f"first touch {first_current * 1000:7.3g} mA, gone after ~5RC = {5 * time_constant:.3g} s"
        )
    print()


def show_resistor_heat():
    print("=== 6. A small resistor on the wrong supply gets hot ===")
    rating_watts = 0.25
    for volts in [5.0, 9.0, 12.0]:
        for ohms in [100.0, 1000.0]:
            power = volts**2 / ohms
            status = "OK" if power <= rating_watts / 2 else ("warm, over half rating" if power <= rating_watts else "OVERLOADED, will smoke")
            print(f"  {volts:>4g} V across {ohms:>6g} Ω -> P = {volts:g}^2 / {ohms:g} = {power:6.3f} W  ({status})")
    print()


def main():
    show_body_table()
    show_effects()
    show_voltage_needed()
    show_battery_shorts()
    show_capacitors()
    show_resistor_heat()


if __name__ == "__main__":
    main()
