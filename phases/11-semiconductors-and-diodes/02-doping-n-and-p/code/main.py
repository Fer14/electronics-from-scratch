import numpy as np

BOLTZMANN_EV = 8.617e-5
ELECTRON_CHARGE = 1.602e-19
SILICON_GAP_EV = 1.12
SILICON_ATOMS_PER_CM3 = 5.0e22
MEASURED_NI_300 = 1.0e10


def intrinsic_density(kelvin):
    shape = (kelvin / 300.0) ** 1.5 * np.exp(-SILICON_GAP_EV / (2 * BOLTZMANN_EV * kelvin))
    shape_at_300 = np.exp(-SILICON_GAP_EV / (2 * BOLTZMANN_EV * 300.0))
    return MEASURED_NI_300 * shape / shape_at_300


def electron_mobility(total_doping):
    return 68.5 + (1414 - 68.5) / (1 + (total_doping / 9.2e16) ** 0.711)


def hole_mobility(total_doping):
    return 44.9 + (470.5 - 44.9) / (1 + (total_doping / 2.23e17) ** 0.719)


def carrier_densities(donors, acceptors, kelvin=300.0):
    ni = intrinsic_density(kelvin)
    net = donors - acceptors
    if net >= 0:
        electrons = net / 2 + np.sqrt((net / 2) ** 2 + ni**2)
        holes = ni**2 / electrons
    else:
        holes = -net / 2 + np.sqrt((net / 2) ** 2 + ni**2)
        electrons = ni**2 / holes
    return electrons, holes


def resistivity_ohm_cm(donors, acceptors, kelvin=300.0):
    electrons, holes = carrier_densities(donors, acceptors, kelvin)
    total = donors + acceptors
    conductivity = ELECTRON_CHARGE * (electrons * electron_mobility(total) + holes * hole_mobility(total))
    return 1.0 / conductivity


def hole_walk(seats, steps):
    row = list(seats)
    frames = ["".join(row)]
    for _ in range(steps):
        gap = row.index("_")
        if gap + 1 < len(row):
            row[gap], row[gap + 1] = row[gap + 1], row[gap]
        frames.append("".join(row))
    return frames


def show_hole_walk():
    print("A hole is a moving vacancy. Field pushes electrons (e) to the LEFT, one hop at a time:")
    for step, frame in enumerate(hole_walk("ee_eeeee", 5)):
        print(f"  step {step}:  [{frame}]   empty seat at position {frame.index('_')}")
    print("  Each electron moved left by one seat; the empty seat travelled right, like a + charge.")
    print()


def show_doping_table():
    print("n-type silicon (phosphorus donors) at 300 K")
    print(f"  {'donors/cm^3':>12} {'1 per N atoms':>14} {'electrons n':>12} {'holes p':>10} {'n/p':>9} {'rho ohm*cm':>11}")
    for donors in [0.0, 1e14, 1e15, 1e16, 1e17, 1e18, 1e19]:
        electrons, holes = carrier_densities(donors, 0.0)
        ratio = electrons / holes
        dilution = f"{SILICON_ATOMS_PER_CM3 / donors:.1e}" if donors else "pure"
        print(f"  {donors:>12.0e} {dilution:>14} {electrons:>12.2e} {holes:>10.2e} {ratio:>9.1e} {resistivity_ohm_cm(donors, 0.0):>11.4g}")
    print()
    print("p-type silicon (boron acceptors) at 300 K")
    print(f"  {'acceptors/cm^3':>14} {'holes p':>10} {'electrons n':>12} {'rho ohm*cm':>11}")
    for acceptors in [1e14, 1e15, 1e16, 1e17, 1e18]:
        electrons, holes = carrier_densities(0.0, acceptors)
        print(f"  {acceptors:>14.0e} {holes:>10.2e} {electrons:>12.2e} {resistivity_ohm_cm(0.0, acceptors):>11.4g}")
    print()


def show_mass_action():
    electrons, holes = carrier_densities(1e16, 0.0)
    print("Mass-action law check for 1e16 donors/cm^3:")
    print(f"  n x p = {electrons:.3e} x {holes:.3e} = {electrons * holes:.3e}")
    print(f"  n_i^2 = {MEASURED_NI_300**2:.3e}")
    print()


def show_compensation():
    electrons, holes = carrier_densities(1e16, 3e15)
    print("Compensation: 1e16 donors and 3e15 acceptors in the same piece")
    print(f"  net donors = 7e15 per cm^3 -> n = {electrons:.3e}, p = {holes:.3e} per cm^3 (still n-type)")
    print()


def show_temperature_stability():
    print("Temperature: doped (1e16 donors) versus pure silicon")
    print(f"  {'T (C)':>6} {'pure n_i':>11} {'doped n':>11} {'doped rho ohm*cm':>17}")
    for celsius in [-40, 25, 75, 125, 175, 250, 350]:
        kelvin = celsius + 273.15
        electrons, _ = carrier_densities(1e16, 0.0, kelvin)
        print(f"  {celsius:>6} {intrinsic_density(kelvin):>11.2e} {electrons:>11.3e} {resistivity_ohm_cm(1e16, 0.0, kelvin):>17.4f}")
    print("  (mobility kept at its 300 K value; real silicon also slows down when hot)")
    print()


def show_wafer_example():
    rho = resistivity_ohm_cm(1e15, 0.0)
    length_cm = 1.0
    area_cm2 = 0.1 * 0.01
    resistance = rho * length_cm / area_cm2
    print("A bar of n-type silicon (1e15 donors), 10 mm long, 1 mm wide, 0.1 mm thick:")
    print(f"  rho = {rho:.3f} ohm*cm, R = rho * L / A = {rho:.3f} * {length_cm} / {area_cm2} = {resistance:.0f} ohm")


def main():
    show_hole_walk()
    show_doping_table()
    show_mass_action()
    show_compensation()
    show_temperature_stability()
    show_wafer_example()


if __name__ == "__main__":
    main()
