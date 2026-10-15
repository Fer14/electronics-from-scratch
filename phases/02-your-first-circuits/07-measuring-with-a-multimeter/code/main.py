import math

COUNTS = 2000
VOLT_RANGES = [0.2, 2.0, 20.0, 200.0, 600.0]
AMP_RANGES = [0.002, 0.02, 0.2]
OHM_RANGES = [200.0, 2000.0, 20000.0, 200000.0, 2000000.0]
VOLTMETER_INPUT_OHMS = 10e6
AMMETER_SHUNT_OHMS = 1.0
MA_JACK_FUSE_AMPS = 0.2
OHMMETER_TEST_AMPS = 1e-4
CONTINUITY_THRESHOLD_OHMS = 30.0

BATTERY_VOLTS = 9.0
R1_OHMS = 1000.0
R2_OHMS = 2000.0


def parallel(first, second):
    return first * second / (first + second)


def display(value, ranges, unit, fixed_range=None):
    candidates = [fixed_range] if fixed_range else ranges
    for full_scale in candidates:
        if abs(value) < full_scale * (COUNTS - 0.5) / COUNTS:
            step = full_scale / COUNTS
            decimals = max(0, -int(math.floor(math.log10(step))))
            return f"{round(value / step) * step:.{decimals}f} {unit}  (range {full_scale:g} {unit})"
    return f"OL  (range {candidates[-1]:g} {unit})"


def true_values():
    current = BATTERY_VOLTS / (R1_OHMS + R2_OHMS)
    return current, current * R1_OHMS, current * R2_OHMS


def voltmeter_across(resistor_ohms, other_ohms):
    loaded = parallel(resistor_ohms, VOLTMETER_INPUT_OHMS)
    return BATTERY_VOLTS * loaded / (loaded + other_ohms)


def voltmeter_in_series():
    total = R1_OHMS + R2_OHMS + VOLTMETER_INPUT_OHMS
    loop_current = BATTERY_VOLTS / total
    return loop_current * VOLTMETER_INPUT_OHMS, loop_current


def ammeter_in_series():
    return BATTERY_VOLTS / (R1_OHMS + R2_OHMS + AMMETER_SHUNT_OHMS)


def ammeter_across_battery(battery_internal_ohms):
    return BATTERY_VOLTS / (battery_internal_ohms + AMMETER_SHUNT_OHMS)


def ohmmeter(resistance, voltage_already_there=0.0, thevenin_ohms=None):
    seen_ohms = resistance if thevenin_ohms is None else thevenin_ohms
    measured_volts = voltage_already_there + OHMMETER_TEST_AMPS * seen_ohms
    return measured_volts / OHMMETER_TEST_AMPS


def continuity(resistance):
    return "BEEP" if resistance < CONTINUITY_THRESHOLD_OHMS else "silent"


def main():
    current, v_r1, v_r2 = true_values()
    print(f"Circuit: {BATTERY_VOLTS:.0f} V battery, R1 = {R1_OHMS:.0f} ohm and R2 = {R2_OHMS:.0f} ohm in one loop")
    print(f"  true current {current * 1e3:.4f} mA, true V(R1) {v_r1:.4f} V, true V(R2) {v_r2:.4f} V")
    print()

    print("1. Voltage: probes ACROSS a part (in parallel), meter input 10 Mohm")
    across_r2 = voltmeter_across(R2_OHMS, R1_OHMS)
    across_r1 = voltmeter_across(R1_OHMS, R2_OHMS)
    print(f"  across R2: exact {across_r2:.5f} V  display {display(across_r2, VOLT_RANGES, 'V')}")
    print(f"  across R1: exact {across_r1:.5f} V  display {display(across_r1, VOLT_RANGES, 'V')}")
    print(f"  across R2 on the 2 V range : {display(across_r2, VOLT_RANGES, 'V', fixed_range=2.0)}")
    print(f"  across R2 on the 200 V range: {display(across_r2, VOLT_RANGES, 'V', fixed_range=200.0)}")
    print(f"  probes swapped on R2       : {display(-across_r2, VOLT_RANGES, 'V')}")
    print()

    print("2. Mistake: voltmeter put IN SERIES (loop broken, meter in the gap)")
    reading, loop_current = voltmeter_in_series()
    print(f"  meter shows {display(reading, VOLT_RANGES, 'V')}, loop current drops to {loop_current * 1e6:.3f} uA")
    print()

    print("3. Current: break the loop and put the meter IN SERIES (mA jack, 1 ohm inside)")
    in_series = ammeter_in_series()
    print(f"  exact {in_series * 1e3:.4f} mA  display {display(in_series * 1e3, [a * 1e3 for a in AMP_RANGES], 'mA')}")
    print(f"  error caused by the meter: {(current - in_series) / current * 100:.3f} %")
    print()

    print("4. Mistake: ammeter put ACROSS the battery (in parallel)")
    for internal in [1.5, 0.5]:
        fault = ammeter_across_battery(internal)
        verdict = "fuse BLOWS" if fault > MA_JACK_FUSE_AMPS else "fuse survives"
        print(f"  battery inside resistance {internal:.1f} ohm -> {fault:.2f} A through a {MA_JACK_FUSE_AMPS:.1f} A fuse: {verdict}")
    print()

    print("5. Resistance: power OFF, part out of circuit, meter pushes 0.1 mA and reads the voltage")
    for value in [R1_OHMS, R2_OHMS]:
        reading = ohmmeter(value)
        print(f"  {value:6.0f} ohm part -> {display(reading, OHM_RANGES, 'ohm')}")
    print(f"  {R2_OHMS:6.0f} ohm on the 2000 ohm range: {display(R2_OHMS, OHM_RANGES, 'ohm', fixed_range=2000.0)}")
    powered = ohmmeter(R2_OHMS, voltage_already_there=v_r2, thevenin_ohms=parallel(R1_OHMS, R2_OHMS))
    print(f"  R2 measured with the battery still ON: {display(powered, OHM_RANGES, 'ohm')}  (nonsense)")
    print()

    print("6. Continuity (beeps below 30 ohm)")
    for name, value in [("jumper wire", 0.05), ("R1", R1_OHMS), ("broken wire", 1e12)]:
        print(f"  {name:12s}: {continuity(value)}")


if __name__ == "__main__":
    main()
