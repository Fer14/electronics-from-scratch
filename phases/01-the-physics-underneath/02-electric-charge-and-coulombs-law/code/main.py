import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19
COULOMB_CONSTANT = 8.988e9
GRAVITATIONAL_CONSTANT = 6.674e-11
ELECTRON_MASS = 9.109e-31
PROTON_MASS = 1.6726e-27
HYDROGEN_RADIUS = 5.29e-11


def electrons_for_charge(charge):
    return charge / ELEMENTARY_CHARGE


def coulomb_force(q1, q2, distance):
    return COULOMB_CONSTANT * q1 * q2 / distance**2


def gravity_force(m1, m2, distance):
    return GRAVITATIONAL_CONSTANT * m1 * m2 / distance**2


def force_vector_on(target_charge, target_position, source_charge, source_position):
    separation = target_position - source_position
    distance = np.linalg.norm(separation)
    direction = separation / distance
    return coulomb_force(target_charge, source_charge, distance) * direction


def net_force(target_charge, target_position, sources):
    total = np.zeros(2)
    for source_charge, source_position in sources:
        total += force_vector_on(target_charge, target_position, source_charge, source_position)
    return total


print("Step 1: how many electrons in a coulomb, and in everyday charges")
print(f"  electrons in 1 C            = {electrons_for_charge(1.0):.3e}")
balloon_charge = -50e-9
print(f"  balloon rubbed on hair, -50 nC -> {electrons_for_charge(-balloon_charge):.2e} extra electrons")
print(f"  that is {electrons_for_charge(-balloon_charge) / 1.5e24 * 1e12:.3f} electrons per trillion in the balloon (~1.5e24 electrons)")

print()
print("Step 2: conservation, rubbing moves charge but never creates it")
transferred = 3.1e11
hair = +transferred * ELEMENTARY_CHARGE
balloon = -transferred * ELEMENTARY_CHARGE
print(f"  hair    after rubbing = {hair * 1e9:+.2f} nC")
print(f"  balloon after rubbing = {balloon * 1e9:+.2f} nC")
print(f"  total                 = {(hair + balloon) * 1e9:+.2f} nC")

print()
print("Step 3: quantization, Millikan-style charges are whole multiples of e")
measured_drops = np.array([3.21e-19, 8.00e-19, 4.82e-19, 1.123e-18, 1.60e-19, 6.39e-19])
multiples = measured_drops / ELEMENTARY_CHARGE
for charge, ratio in zip(measured_drops, multiples):
    print(f"  drop charge {charge:.3e} C  ->  {ratio:5.2f} e  ->  n = {round(ratio)}")

print()
print("Step 4: Coulomb's law with numbers")
force = coulomb_force(1e-6, 1e-6, 0.10)
print(f"  two +1 uC charges 10 cm apart: F = {force:.4f} N  (repel)")
force = coulomb_force(1e-6, -1e-6, 0.10)
print(f"  +1 uC and -1 uC 10 cm apart:   F = {force:.4f} N  (negative = attract)")
force = coulomb_force(1.0, 1.0, 1000.0)
print(f"  two 1 C charges 1 km apart:    F = {force:.3e} N  (about {force / 9.81:.0f} kg of weight)")

print()
print("Step 5: the inverse-square law")
for distance in [0.05, 0.10, 0.20, 0.40]:
    force = coulomb_force(1e-6, 1e-6, distance)
    print(f"  r = {distance * 100:4.0f} cm   F = {force:7.4f} N")

print()
print("Step 6: electric force versus gravity inside a hydrogen atom")
electric = abs(coulomb_force(ELEMENTARY_CHARGE, -ELEMENTARY_CHARGE, HYDROGEN_RADIUS))
gravity = gravity_force(ELECTRON_MASS, PROTON_MASS, HYDROGEN_RADIUS)
print(f"  electric attraction = {electric:.3e} N")
print(f"  gravitational pull  = {gravity:.3e} N")
print(f"  ratio               = {electric / gravity:.2e}")

print()
print("Step 7: superposition, adding force vectors with numpy")
target_charge = 2e-9
target_position = np.array([0.0, 0.0])
sources = [
    (3e-9, np.array([-0.03, 0.0])),
    (-4e-9, np.array([0.0, 0.04])),
    (1e-9, np.array([0.03, 0.0])),
]
for source_charge, source_position in sources:
    vector = np.round(force_vector_on(target_charge, target_position, source_charge, source_position) * 1e6, 3) + 0.0
    x_cm, y_cm = source_position * 100
    print(f"  from {source_charge * 1e9:+.0f} nC at ({x_cm:+.0f} cm, {y_cm:+.0f} cm): F = [{vector[0]:+8.3f}, {vector[1]:+8.3f}] uN")
total = net_force(target_charge, target_position, sources)
angle = np.degrees(np.arctan2(total[1], total[0]))
print(f"  net force          = [{total[0] * 1e6:+8.3f}, {total[1] * 1e6:+8.3f}] uN")
print(f"  size {np.linalg.norm(total) * 1e6:.3f} uN at {angle:.1f} degrees from the +x axis")
