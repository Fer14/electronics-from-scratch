import cmath
import math

from sim import Circuit


def add(z, w):
    return (z[0] + w[0], z[1] + w[1])


def subtract(z, w):
    return (z[0] - w[0], z[1] - w[1])


def multiply(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def conjugate(z):
    return (z[0], -z[1])


def magnitude(z):
    return math.sqrt(z[0] ** 2 + z[1] ** 2)


def divide(z, w):
    top = multiply(z, conjugate(w))
    bottom = w[0] ** 2 + w[1] ** 2
    return (top[0] / bottom, top[1] / bottom)


def angle_deg(z):
    return math.degrees(math.atan2(z[1], z[0]))


def from_polar(size, degrees):
    radians = math.radians(degrees)
    return (size * math.cos(radians), size * math.sin(radians))


def tidy(value):
    return 0.0 if abs(value) < 1e-12 else value


def show(z):
    real, imag = tidy(z[0]), tidy(z[1])
    sign = "+" if imag >= 0 else "-"
    return f"{real:.4g} {sign} {abs(imag):.4g}j"


def exp_j_by_series(theta, terms=30):
    total = (0.0, 0.0)
    term = (1.0, 0.0)
    for n in range(terms):
        total = add(total, term)
        term = multiply(term, (0.0, theta / (n + 1)))
    return total


def main():
    j = (0.0, 1.0)

    print("=== Step 1: Powers of j go round in a circle ===")
    power = (1.0, 0.0)
    for n in range(8):
        print(f"  j^{n} = {show(power):>10}   angle {angle_deg((tidy(power[0]), tidy(power[1]))) % 360:5.1f} deg")
        power = multiply(power, j)

    print("\n=== Step 2: Arithmetic in rectangular form ===")
    z1, z2 = (3.0, 4.0), (1.0, -2.0)
    print(f"  z1 = {show(z1)},  z2 = {show(z2)}")
    print(f"  z1 + z2      = {show(add(z1, z2))}")
    print(f"  z1 - z2      = {show(subtract(z1, z2))}")
    print(f"  z1 x z2      = {show(multiply(z1, z2))}")
    print(f"  conj(z1)     = {show(conjugate(z1))}")
    print(f"  z1 x conj(z1) = {show(multiply(z1, conjugate(z1)))}  (= |z1|^2)")
    print(f"  z1 / z2      = {show(divide(z1, z2))}")

    print("\n=== Step 3: Polar form: size and angle ===")
    for name, z in (("z1", z1), ("z2", z2), ("z1 x z2", multiply(z1, z2)), ("z1 / z2", divide(z1, z2))):
        print(f"  {name:<8} = {show(z):>14}   size {magnitude(z):8.4f}   angle {angle_deg(z):8.3f} deg")
    print(f"  sizes multiply: {magnitude(z1):.4f} x {magnitude(z2):.4f} = {magnitude(z1) * magnitude(z2):.4f}")
    print(f"  angles add:     {angle_deg(z1):.3f} + ({angle_deg(z2):.3f}) = {angle_deg(z1) + angle_deg(z2):.3f} deg")
    print(f"  back from polar: 5 at 53.130 deg = {show(from_polar(5.0, 53.130))}")

    print("\n=== Step 4: Euler's formula, checked by adding up a series ===")
    for theta in (1.0, math.pi / 2, math.pi):
        series = exp_j_by_series(theta)
        print(f"  theta = {theta:.4f} rad: series e^(j theta) = {show(series):>18}   "
              f"cos + j sin = {show((math.cos(theta), math.sin(theta))):>18}")

    print("\n=== Step 5: Multiplying by e^(j 30 deg) rotates by 30 deg ===")
    arrow = (1.0, 0.0)
    step = from_polar(1.0, 30.0)
    for n in range(1, 13):
        arrow = multiply(arrow, step)
        if n % 3 == 0:
            print(f"  after {n:2d} turns of 30 deg: {show(arrow):>16}   angle {angle_deg((tidy(arrow[0]), tidy(arrow[1]))) % 360:6.1f} deg")

    print("\n=== Step 6: Solving x^2 - 4x + 13 = 0 ===")
    a, b, c = 1.0, -4.0, 13.0
    disc = b * b - 4 * a * c
    root_of_disc = (0.0, math.sqrt(-disc))
    x1 = ((-b + root_of_disc[0]) / (2 * a), root_of_disc[1] / (2 * a))
    x2 = conjugate(x1)
    for x in (x1, x2):
        value = add(add(multiply(x, x), multiply((b, 0.0), x)), (c, 0.0))
        print(f"  x = {show(x)}  ->  x^2 - 4x + 13 = {show(value)}")

    print("\n=== Step 7: Python already knows complex numbers ===")
    p1, p2 = 3 + 4j, 1 - 2j
    print(f"  (3+4j) * (1-2j) = {p1 * p2}")
    print(f"  (3+4j) / (1-2j) = {p1 / p2}")
    print(f"  abs(3+4j) = {abs(p1)},  cmath.phase(3+4j) = {math.degrees(cmath.phase(p1)):.3f} deg")
    print(f"  cmath.exp(1j * pi) = {cmath.exp(1j * math.pi):.4f}")
    print(f"  cmath.rect(5, 0.9273) = {cmath.rect(5, 0.9273):.4f}")

    print("\n=== Step 8: The simulator answers with complex numbers ===")
    circuit = Circuit()
    circuit.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.resistor("R1", "in", "out", 1000.0)
    circuit.capacitor("C1", "out", "0", 159.15e-9)
    result = circuit.ac([1000.0], source="V1")
    v_out = complex(result.v("out")[0])
    as_pair = (v_out.real, v_out.imag)
    print(f"  V(out) at 1 kHz = {show(as_pair)} V")
    print(f"  size {magnitude(as_pair):.4f} V, angle {angle_deg(as_pair):.2f} deg  (Lesson 02 measured 0.7071 V and a 45 deg lag)")


if __name__ == "__main__":
    main()
