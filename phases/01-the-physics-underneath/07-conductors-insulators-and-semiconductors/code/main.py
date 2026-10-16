import numpy as np

ELECTRON_CHARGE = 1.602176634e-19
BOLTZMANN_EV = 8.617e-5
COPPER_FREE_ELECTRONS = 8.5e28
SILICON_ATOMS = 5.0e28
EFFECTIVE_STATES = 2.0e25

MATERIALS = [
    ("silver", 1.59e-8, "conductor"),
    ("copper", 1.68e-8, "conductor"),
    ("gold", 2.44e-8, "conductor"),
    ("aluminium", 2.65e-8, "conductor"),
    ("iron", 9.7e-8, "conductor"),
    ("nichrome", 1.10e-6, "conductor"),
    ("graphite", 1.0e-5, "conductor"),
    ("sea water", 0.2, "in between"),
    ("germanium", 0.46, "semiconductor"),
    ("silicon", 2.3e3, "semiconductor"),
    ("pure water", 1.8e5, "insulator"),
    ("wood (dry)", 1.0e11, "insulator"),
    ("glass", 1.0e12, "insulator"),
    ("rubber", 1.0e13, "insulator"),
    ("quartz", 7.5e17, "insulator"),
    ("PTFE (Teflon)", 1.0e23, "insulator"),
]

BAND_GAPS_EV = [
    ("germanium", 0.66),
    ("silicon", 1.12),
    ("gallium arsenide", 1.42),
    ("diamond", 5.5),
    ("glass (silica)", 9.0),
]


def resistance_of_rod(resistivity, length_m, area_m2):
    return resistivity * length_m / area_m2


def kicked_across_fraction(gap_ev, temperature_k):
    return np.exp(-gap_ev / (2 * BOLTZMANN_EV * temperature_k))


def carriers_per_m3(gap_ev, temperature_k):
    return EFFECTIVE_STATES * kicked_across_fraction(gap_ev, temperature_k)


def resistivity_from_carriers(carriers, mobility):
    return 1.0 / (carriers * ELECTRON_CHARGE * mobility)


def print_resistivity_ladder():
    print("=== Resistivity ladder (ohm metres, room temperature) ===")
    resistivities = np.array([r for _, r, _ in MATERIALS])
    exponents = np.log10(resistivities)
    lowest = np.floor(exponents.min())
    for (name, rho, group), exponent in zip(MATERIALS, exponents):
        bar = "#" * int(round(exponent - lowest + 1))
        print(f"{name:15s} {rho:9.2e}  10^{exponent:6.1f}  {group:13s} {bar}")
    span = exponents.max() - exponents.min()
    print(f"Span from best conductor to best insulator: {span:.1f} orders of magnitude")
    print()


def print_rod_resistances():
    print("=== Resistance of a rod 1 m long, 1 mm^2 cross-section (preview of Phase 03) ===")
    length = 1.0
    area = 1e-6
    for name, rho, _ in MATERIALS:
        ohms = resistance_of_rod(rho, length, area)
        print(f"{name:15s} R = {ohms:9.2e} ohm")
    print()


def print_copper_mobility():
    print("=== How freely do copper's electrons move? ===")
    copper_rho = 1.68e-8
    conductivity = 1.0 / copper_rho
    mobility = conductivity / (COPPER_FREE_ELECTRONS * ELECTRON_CHARGE)
    print(f"Copper conductivity        = {conductivity:.3e} siemens per metre")
    print(f"Free electrons per m^3     = {COPPER_FREE_ELECTRONS:.2e}")
    print(f"Mobility = sigma / (n e)   = {mobility:.2e} m^2 per volt-second")
    print(f"Free electrons per atom    = {COPPER_FREE_ELECTRONS / 8.49e28:.2f}")
    print()


def print_band_gap_table(temperature_k):
    print(f"=== Band gaps and carriers at {temperature_k:.0f} K ===")
    print(f"kT = {BOLTZMANN_EV * temperature_k:.4f} eV")
    for name, gap in BAND_GAPS_EV:
        fraction = kicked_across_fraction(gap, temperature_k)
        carriers = carriers_per_m3(gap, temperature_k)
        print(f"{name:17s} gap = {gap:4.2f} eV  factor = {fraction:9.2e}  carriers = {carriers:9.2e} per m^3")
    ratio = COPPER_FREE_ELECTRONS / carriers_per_m3(1.12, temperature_k)
    print(f"Copper has {ratio:.1e} times more free electrons than pure silicon")
    print()


def print_temperature_effect():
    print("=== Heating changes conductors and semiconductors in opposite directions ===")
    temperatures = np.array([250.0, 300.0, 350.0, 400.0])
    copper_tempco = 0.0039
    for t in temperatures:
        copper_rho = 1.68e-8 * (1 + copper_tempco * (t - 293.0))
        silicon_carriers = carriers_per_m3(1.12, t)
        print(f"T = {t:5.0f} K  copper rho = {copper_rho:.3e} ohm m  silicon carriers = {silicon_carriers:.2e} per m^3")
    ratio = carriers_per_m3(1.12, 310.0) / carriers_per_m3(1.12, 300.0)
    print(f"Warming silicon from 300 K to 310 K multiplies its carriers by {ratio:.2f}")
    print()


def print_doping():
    print("=== Doping: one impurity atom per million silicon atoms ===")
    electron_mobility_silicon = 0.135
    hole_mobility_silicon = 0.048
    intrinsic = 1.0e16
    pure_rho = 1.0 / (intrinsic * ELECTRON_CHARGE * (electron_mobility_silicon + hole_mobility_silicon))
    donors = SILICON_ATOMS * 1e-6
    doped_rho = resistivity_from_carriers(donors, electron_mobility_silicon)
    print(f"Pure silicon carriers      = {intrinsic:.1e} electrons + {intrinsic:.1e} holes per m^3")
    print(f"Pure silicon resistivity   = {pure_rho:.2e} ohm m")
    print(f"Donor atoms added          = {donors:.1e} per m^3")
    print(f"Doped silicon resistivity  = {doped_rho:.2e} ohm m")
    print(f"Improvement factor         = {pure_rho / doped_rho:.1e}")
    print()


def main():
    print_resistivity_ladder()
    print_rod_resistances()
    print_copper_mobility()
    print_band_gap_table(300.0)
    print_temperature_effect()
    print_doping()


if __name__ == "__main__":
    main()
