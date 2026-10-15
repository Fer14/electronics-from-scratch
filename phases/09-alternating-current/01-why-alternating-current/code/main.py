from sim import Circuit

TOWN_POWER_W = 12_000.0
LINE_RESISTANCE_EACH_WIRE = 0.4
HOUSE_VOLTAGE = 240.0


def loss_by_formula(power_w, voltage_v, line_resistance_total):
    current = power_w / voltage_v
    loss = current**2 * line_resistance_total
    drop = current * line_resistance_total
    return current, loss, drop


def send_power(source_volts, turns_ratio):
    load_resistance = HOUSE_VOLTAGE**2 / TOWN_POWER_W
    load_seen_by_line = load_resistance * turns_ratio**2
    c = Circuit()
    c.voltage_source("V1", "plant", "0", source_volts)
    c.resistor("Rgo", "plant", "town", LINE_RESISTANCE_EACH_WIRE)
    c.resistor("Rload", "town", "back", load_seen_by_line)
    c.resistor("Rreturn", "back", "0", LINE_RESISTANCE_EACH_WIRE)
    r = c.dc()
    line_current = r.i("Rgo")
    line_loss = r.p("Rgo") + r.p("Rreturn")
    delivered = r.p("Rload")
    house_volts = r.v("town", "back") / turns_ratio
    return line_current, line_loss, delivered, house_volts


def main():
    total_line = 2 * LINE_RESISTANCE_EACH_WIRE
    print("=== Step 1: The same 12 kW sent at different voltages (formula) ===")
    print(f"  line resistance (both wires) = {total_line:.1f} ohm")
    print(f"  {'line voltage':>14} {'current':>10} {'line loss':>12} {'loss %':>8} {'voltage drop':>13}")
    for volts in (240.0, 2_400.0, 24_000.0, 240_000.0):
        current, loss, drop = loss_by_formula(TOWN_POWER_W, volts, total_line)
        print(f"  {volts:>12.0f} V {current:>8.2f} A {loss:>10.2f} W {100 * loss / TOWN_POWER_W:>7.3f}% {drop:>11.2f} V")

    print("\n=== Step 2: Simulate the line with a fixed town load ===")
    print(f"  town load = {HOUSE_VOLTAGE:.0f} V^2 / {TOWN_POWER_W:.0f} W = {HOUSE_VOLTAGE**2 / TOWN_POWER_W:.2f} ohm")
    for volts, ratio in ((240.0, 1), (2_400.0, 10), (24_000.0, 100)):
        current, loss, delivered, house = send_power(volts, ratio)
        print(f"  send at {volts:>7.0f} V (step-down {ratio:>3}:1): line current {current:7.3f} A, "
              f"line loss {loss:9.2f} W, delivered {delivered:9.1f} W, house sees {house:6.1f} V")

    print("\n=== Step 3: Mains frequencies around the world ===")
    for place, volts, hertz in (("Europe, most of Asia, Africa", 230, 50),
                                ("North America", 120, 60),
                                ("Japan, east (Tokyo)", 100, 50),
                                ("Japan, west (Osaka)", 100, 60),
                                ("Brazil (varies by city)", 127, 60)):
        period_ms = 1000.0 / hertz
        reversals_per_second = 2 * hertz
        print(f"  {place:<30} {volts:>4} V  {hertz} Hz  period {period_ms:6.2f} ms  "
              f"direction flips {reversals_per_second} times per second")
    print(f"  cycles in one day at 50 Hz: {50 * 60 * 60 * 24:,}")


if __name__ == "__main__":
    main()
