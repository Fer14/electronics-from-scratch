import numpy as np

WATER_DENSITY = 1000.0
WATER_VISCOSITY = 1.0e-3
G = 9.81
ELEMENTARY_CHARGE = 1.602176634e-19
COPPER_ELECTRON_DENSITY = 8.5e28
SOUND_SPEED_IN_WATER = 1480.0
SIGNAL_SPEED_IN_CABLE = 2.0e8


def pressure_from_height(height_m):
    return WATER_DENSITY * G * height_m


def pipe_resistance(length_m, radius_m):
    return 8 * WATER_VISCOSITY * length_m / (np.pi * radius_m**4)


def flow(pressure_pa, resistance):
    return pressure_pa / resistance


def current(volts, ohms):
    return volts / ohms


def drift_speed(amps, area_m2):
    return amps / (COPPER_ELECTRON_DENSITY * ELEMENTARY_CHARGE * area_m2)


def print_side_by_side(pressure_pa, pipe_r, volts, ohms):
    water_flow = flow(pressure_pa, pipe_r)
    electric_current = current(volts, ohms)
    print("Side by side: one pump and one pipe, one battery and one resistor")
    print(f"  push      : pressure difference = {pressure_pa:10.1f} Pa      | voltage    = {volts:6.2f} V")
    print(f"  opposition: pipe resistance     = {pipe_r:10.3e} Pa*s/m^3 | resistance = {ohms:6.0f} ohm")
    print(f"  flow      : water flow          = {water_flow * 1e6:10.3f} mL/s    | current    = {electric_current * 1e3:6.2f} mA")
    print(f"  power     : pressure x flow     = {pressure_pa * water_flow:10.4f} W       | V x I      = {volts * electric_current:6.4f} W")
    print()


def doubling_experiments(pressure_pa, pipe_r, volts, ohms):
    print("What happens when we double the push or double the opposition")
    cases = [("baseline", 1, 1), ("double the push", 2, 1), ("double the opposition", 1, 2)]
    for name, push_factor, opposition_factor in cases:
        q = flow(push_factor * pressure_pa, opposition_factor * pipe_r)
        i = current(push_factor * volts, opposition_factor * ohms)
        print(f"  {name:22s}: water {q * 1e6:7.3f} mL/s   electric {i * 1e3:6.2f} mA")
    print()


def series_and_parallel_pipes(pressure_pa, pipe_r):
    print("Two identical pipes, one after the other (series) or side by side (parallel)")
    one = flow(pressure_pa, pipe_r)
    series = flow(pressure_pa, 2 * pipe_r)
    parallel = 2 * flow(pressure_pa, pipe_r)
    print(f"  one pipe       : {one * 1e6:7.3f} mL/s")
    print(f"  two in series  : {series * 1e6:7.3f} mL/s  (half: the water must squeeze through both)")
    print(f"  two in parallel: {parallel * 1e6:7.3f} mL/s  (double: two paths, the pump works harder)")
    print()


def where_shape_matters():
    print("Where the analogy breaks 1: thickness matters differently")
    print("  radius factor | pipe resistance factor (1/r^4) | wire resistance factor (1/r^2)")
    for factor in [0.5, 1.0, 2.0]:
        print(f"  {factor:13.1f} | {1 / factor**4:30.4f} | {1 / factor**2:30.4f}")
    print()


def where_speed_matters(hose_length_m, water_speed_m_s, amps, wire_area_m2, wire_length_m):
    print("Where the analogy breaks 2 (and also where it shines): how fast things travel")
    water_trip = hose_length_m / water_speed_m_s
    pressure_trip = hose_length_m / SOUND_SPEED_IN_WATER
    v_drift = drift_speed(amps, wire_area_m2)
    electron_trip = wire_length_m / v_drift
    signal_trip = wire_length_m / SIGNAL_SPEED_IN_CABLE
    print(f"  a {hose_length_m:.0f} m hose, water moving at {water_speed_m_s:.1f} m/s")
    print(f"    one drop travelling the whole hose : {water_trip:10.1f} s")
    print(f"    the push arriving (full hose)      : {pressure_trip * 1e3:10.1f} ms")
    print(f"  a {wire_length_m:.0f} m copper wire of {wire_area_m2 * 1e6:.1f} mm^2 carrying {amps:.1f} A")
    print(f"    electron drift speed               : {v_drift * 1e3:10.4f} mm/s")
    print(f"    one electron travelling the wire   : {electron_trip / 3600:10.2f} hours")
    print(f"    the push (signal) arriving         : {signal_trip * 1e9:10.1f} ns")
    print()


def where_ends_matter():
    print("Where the analogy breaks 3: cut the loop open")
    print("  cut water pipe with the pump running : water sprays out, the pump keeps flowing")
    print("  cut wire with the battery connected  : current stops everywhere at once, nothing leaks out")
    print()


def main():
    tank_height = 1.0
    pressure = pressure_from_height(tank_height)
    pipe_r = pipe_resistance(length_m=1.0, radius_m=1.0e-3)
    volts = 9.0
    ohms = 450.0
    print(f"A water tank {tank_height:.1f} m high pushes with {pressure:.0f} Pa (pressure = density x g x height)")
    print()
    print_side_by_side(pressure, pipe_r, volts, ohms)
    doubling_experiments(pressure, pipe_r, volts, ohms)
    series_and_parallel_pipes(pressure, pipe_r)
    where_shape_matters()
    where_speed_matters(hose_length_m=20.0, water_speed_m_s=1.0, amps=1.0, wire_area_m2=1.0e-6, wire_length_m=1.0)
    where_ends_matter()


if __name__ == "__main__":
    main()
