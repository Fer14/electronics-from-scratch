import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.109e-31
PROTON_MASS = 1.6726e-27
NEUTRON_MASS = 1.6749e-27
AVOGADRO = 6.022e23

PARTICLES = {
    "proton": (PROTON_MASS, +1),
    "neutron": (NEUTRON_MASS, 0),
    "electron": (ELECTRON_MASS, -1),
}

SHELLS = {
    "hydrogen": (1, [1]),
    "helium": (2, [2]),
    "carbon": (6, [2, 4]),
    "neon": (10, [2, 8]),
    "sodium": (11, [2, 8, 1]),
    "silicon": (14, [2, 8, 4]),
    "copper": (29, [2, 8, 18, 1]),
    "silver": (47, [2, 8, 18, 18, 1]),
}

COPPER_DENSITY_KG_PER_M3 = 8960.0
COPPER_MOLAR_MASS_KG_PER_MOL = 0.06355
COPPER_PROTONS = 29


def atoms_per_cubic_meter(density, molar_mass):
    return density / molar_mass * AVOGADRO


def wire_volume(length_m, area_mm2):
    return length_m * area_mm2 * 1e-6


def charge_to_mass_ratio(charge, mass):
    return charge / mass


print("Step 1: the three particles")
for name, (mass, charge_units) in PARTICLES.items():
    charge = charge_units * ELEMENTARY_CHARGE
    print(f"  {name:8s} mass = {mass:.4e} kg   charge = {charge:+.4e} C   ({charge_units:+d} e)")
print(f"  proton mass / electron mass = {PROTON_MASS / ELECTRON_MASS:.1f}")

print()
print("Step 2: shells and valence electrons")
for element, (protons, shells) in SHELLS.items():
    assert sum(shells) == protons
    print(f"  {element:9s} {protons:2d} protons  shells {str(shells):20s} valence electrons = {shells[-1]}")

print()
print("Step 3: sizes, an atom as a stadium")
atom_diameter = 2.6e-10
nucleus_diameter = 1.0e-14
scale = 100.0 / atom_diameter
print(f"  atom diameter          = {atom_diameter:.1e} m")
print(f"  nucleus diameter       = {nucleus_diameter:.1e} m")
print(f"  ratio atom / nucleus   = {atom_diameter / nucleus_diameter:,.0f}")
print(f"  if the atom were a 100 m stadium, the nucleus would be {nucleus_diameter * scale * 1000:.1f} mm wide")

print()
print("Step 4: counting atoms in a copper wire")
atoms_m3 = atoms_per_cubic_meter(COPPER_DENSITY_KG_PER_M3, COPPER_MOLAR_MASS_KG_PER_MOL)
print(f"  moles per m^3            = {COPPER_DENSITY_KG_PER_M3 / COPPER_MOLAR_MASS_KG_PER_MOL:,.0f} mol")
print(f"  atoms per m^3            = {atoms_m3:.3e}")
volume = wire_volume(1.0, 1.5)
atoms_in_wire = atoms_m3 * volume
print(f"  1 m of 1.5 mm^2 wire     = {volume:.2e} m^3 = {volume * 1e6:.1f} cm^3")
print(f"  mass of that wire        = {volume * COPPER_DENSITY_KG_PER_M3 * 1000:.2f} g")
print(f"  copper atoms in it       = {atoms_in_wire:.3e}")
print(f"  free (valence) electrons = {atoms_in_wire:.3e}  (one per atom)")

print()
print("Step 5: the charge hiding in that wire")
all_electrons = atoms_in_wire * COPPER_PROTONS
negative_charge = -all_electrons * ELEMENTARY_CHARGE
positive_charge = atoms_in_wire * COPPER_PROTONS * ELEMENTARY_CHARGE
free_charge = -atoms_in_wire * ELEMENTARY_CHARGE
print(f"  total electrons          = {all_electrons:.3e}")
print(f"  charge of all electrons  = {negative_charge:.3e} C")
print(f"  charge of all protons    = {positive_charge:+.3e} C")
print(f"  net charge               = {positive_charge + negative_charge:+.1f} C")
print(f"  charge of free electrons = {free_charge:.3e} C")

print()
print("Step 6: Thomson's measurement, charge-to-mass ratio")
electron_ratio = charge_to_mass_ratio(ELEMENTARY_CHARGE, ELECTRON_MASS)
hydrogen_ion_ratio = charge_to_mass_ratio(ELEMENTARY_CHARGE, PROTON_MASS)
print(f"  electron e/m             = {electron_ratio:.3e} C/kg")
print(f"  hydrogen ion e/m         = {hydrogen_ion_ratio:.3e} C/kg")
print(f"  electron is {electron_ratio / hydrogen_ion_ratio:.0f} times more 'responsive'")

print()
print("Step 7: why electrons are the movers")
force = 1e-15
accelerations = np.array([force / ELECTRON_MASS, force / PROTON_MASS])
print(f"  same push of {force:.0e} N:")
print(f"  electron acceleration    = {accelerations[0]:.3e} m/s^2")
print(f"  proton acceleration      = {accelerations[1]:.3e} m/s^2")
print(f"  ratio                    = {accelerations[0] / accelerations[1]:.0f}")
time = 1e-9
distances = 0.5 * accelerations * time**2
print(f"  distance covered in 1 ns from rest: electron {distances[0] * 1000:.3f} mm, proton {distances[1] * 1e6:.3f} um")
