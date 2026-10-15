import numpy as np

BOLTZMANN_EV = 8.617e-5
ELECTRON_CHARGE = 1.602e-19

MATERIALS = {
    "germanium": {"gap_ev": 0.66, "nc_300": 1.04e19, "nv_300": 6.0e18, "mu_n": 3900, "mu_p": 1900},
    "silicon": {"gap_ev": 1.12, "nc_300": 2.8e19, "nv_300": 1.04e19, "mu_n": 1350, "mu_p": 480},
    "gallium arsenide": {"gap_ev": 1.42, "nc_300": 4.7e17, "nv_300": 7.0e18, "mu_n": 8500, "mu_p": 400},
}

COPPER_FREE_ELECTRONS_PER_CM3 = 8.5e22
SILICON_ATOMS_PER_CM3 = 5.0e22
COPPER_RESISTIVITY_OHM_M = 1.7e-8


def thermal_energy_ev(kelvin):
    return BOLTZMANN_EV * kelvin


def intrinsic_density(material, kelvin):
    scale = (kelvin / 300.0) ** 1.5
    nc = material["nc_300"] * scale
    nv = material["nv_300"] * scale
    return np.sqrt(nc * nv) * np.exp(-material["gap_ev"] / (2 * thermal_energy_ev(kelvin)))


def resistivity_ohm_m(electrons_per_cm3, holes_per_cm3, mu_n, mu_p):
    conductivity_per_ohm_cm = ELECTRON_CHARGE * (electrons_per_cm3 * mu_n + holes_per_cm3 * mu_p)
    return 1.0 / conductivity_per_ohm_cm / 100.0


def boltzmann_chance(gap_ev, kelvin):
    return np.exp(-gap_ev / (2 * thermal_energy_ev(kelvin)))


def show_thermal_energy():
    print("Thermal energy kT (the typical 'kick' an electron gets from heat)")
    for kelvin, label in [(77, "liquid nitrogen"), (300, "room temperature"), (400, "hot chip, 127 C")]:
        print(f"  {label:<18} T = {kelvin:>3} K   kT = {thermal_energy_ev(kelvin) * 1000:6.2f} meV")
    print()


def show_gap_chances():
    print("How unlikely is a jump across the gap at 300 K?  chance ~ exp(-Eg / 2kT)")
    for name, material in MATERIALS.items():
        print(f"  {name:<17} Eg = {material['gap_ev']:.2f} eV   exp(-Eg/2kT) = {boltzmann_chance(material['gap_ev'], 300):.2e}")
    print(f"  {'glass (SiO2)':<17} Eg = 9.00 eV   exp(-Eg/2kT) = {boltzmann_chance(9.0, 300):.2e}")
    print()


def show_intrinsic_densities():
    print("Free electrons per cubic centimetre in pure (intrinsic) material at 300 K")
    for name, material in MATERIALS.items():
        density = intrinsic_density(material, 300)
        fraction = density / SILICON_ATOMS_PER_CM3
        print(f"  {name:<17} n_i = {density:.2e} per cm^3   (about 1 in {1 / fraction:.1e} atoms)")
    print(f"  {'copper':<17} n   = {COPPER_FREE_ELECTRONS_PER_CM3:.2e} per cm^3   (about 1 per atom)")
    print()


def show_resistivities():
    print("Resistivity at 300 K")
    for name, material in MATERIALS.items():
        density = intrinsic_density(material, 300)
        rho = resistivity_ohm_m(density, density, material["mu_n"], material["mu_p"])
        print(f"  pure {name:<17} rho = {rho:10.3e} ohm*m   ({rho / COPPER_RESISTIVITY_OHM_M:.1e} times copper)")
    print(f"  {'copper':<22} rho = {COPPER_RESISTIVITY_OHM_M:10.3e} ohm*m")
    print()


def show_temperature_sweep():
    silicon = MATERIALS["silicon"]
    print("Pure silicon gets BETTER at conducting when it gets hotter (copper does the opposite)")
    print(f"  {'T (C)':>6} {'n_i (per cm^3)':>16} {'rho (ohm*m)':>13}")
    for celsius in [-40, 0, 25, 50, 75, 100, 125, 150]:
        kelvin = celsius + 273.15
        density = intrinsic_density(silicon, kelvin)
        rho = resistivity_ohm_m(density, density, silicon["mu_n"], silicon["mu_p"])
        print(f"  {celsius:>6} {density:>16.2e} {rho:>13.1f}")
    room = intrinsic_density(silicon, 300.0)
    warmer = intrinsic_density(silicon, 310.0)
    print(f"  +10 K near room temperature multiplies n_i by {warmer / room:.2f}")
    print()


def main():
    show_thermal_energy()
    show_gap_chances()
    show_intrinsic_densities()
    show_resistivities()
    show_temperature_sweep()


if __name__ == "__main__":
    main()
