# Complex Numbers for Circuits

> A complex number is an arrow written as two ordinary numbers. Multiplying by j turns the arrow a quarter turn, and that one trick turns every AC calculus problem into school arithmetic.

**Type:** Learn
**Prerequisites:** Phase 09, Lesson 02 (Sine Waves, Frequency and Phase). From maths: adding, multiplying, squares and square roots. Nothing else: this lesson starts from zero.
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Number line | All ordinary numbers laid out on a line, negatives to the left, positives to the right | A ruler that continues past zero to the left |
| Real number | Any number on that line: 3, -2.5, 0.7071, pi | A position along a straight road |
| Imaginary unit (j) | A new number whose square is -1; it means "a quarter turn" | A quarter turn of a steering wheel |
| Imaginary number | A real number times j, like 4j; it sits on a second line at right angles to the first | A position on a road that crosses the first one at a right angle |
| Complex number | A real part plus an imaginary part, like 3 + 4j; a point (or an arrow) on a flat plane | A street address: "3 blocks east, 4 blocks north" |
| Complex plane | The flat sheet where complex numbers live: real axis across, imaginary axis up | A city map with east-west and north-south streets |
| Real part / imaginary part | The across and up coordinates of a complex number | The "east" and "north" numbers of an address |
| Rectangular form | Writing a complex number as across + up: a + bj | Giving directions as "3 east, 4 north" |
| Magnitude (modulus, size) | The length of the arrow | The straight-line distance "as the crow flies" |
| Angle (argument, phase) | The direction of the arrow, measured anticlockwise from the real axis | A compass bearing |
| Polar form | Writing a complex number as size and angle: 5 at 53.13 degrees | Giving directions as "walk 5 blocks at bearing 53 degrees" |
| Conjugate | The mirror image of a complex number across the real axis: a + bj becomes a - bj | Your reflection in a lake |
| Euler's formula | e^(j theta) = cos(theta) + j sin(theta): an arrow of length 1 at angle theta | A clock hand of length 1 pointing at angle theta |
| e | The number 2.71828..., the natural base of growth | The number your savings approach with "continuous" compound interest |

## Learning Objectives

- Explain what j means as "a quarter turn" and why j x j = -1.
- Draw any complex number on the complex plane and move between rectangular form (a + bj) and polar form (size at angle).
- Add, subtract, multiply and divide complex numbers by hand, and check the results in Python.
- Explain why multiplying complex numbers multiplies their sizes and adds their angles.
- State Euler's formula, check it numerically, and use e^(j theta) to rotate an arrow.
- Read a complex voltage from the simulator as "an amplitude and a phase".

## The Problem

At the end of Lesson 02 the simulator told us that an RC circuit at 1 kHz makes the output 0.7071 times the input and 45 degrees late. To find that, we simulated ten whole cycles, thousands of time steps, then measured peaks and zero crossings. For one frequency. A filter designer wants the answer at hundreds of frequencies, for circuits with dozens of parts.

There is a faster way, and it rests on one observation from Lesson 02: in a circuit of resistors, capacitors and inductors driven by a sine wave, every voltage and current is a sine wave of the same frequency. Each one is fully described by **two numbers**: its amplitude and its phase. If we had a kind of number that carries a size and an angle together, and whose arithmetic does the right thing to them, we could analyse AC circuits with plain algebra, exactly like the DC circuits of Phase 05.

Such numbers exist. They were invented for an apparently useless puzzle about square roots of negative numbers, and they turned out to be the natural language of rotation. In 1893 the engineer Charles Proteus Steinmetz showed how to use them for AC circuits, and since then every electrical engineer has used them. This lesson builds them from nothing.

## The Physics

There is no new physics in this lesson, but there is new geometry, and it matches the physics of Lesson 02 perfectly. A sine wave is the shadow of a spinning arrow. An arrow on a flat sheet is described by two numbers (how far across, how far up; or how long, which direction). AC circuits shift and scale sine waves, which in the arrow picture means **stretching and turning arrows**. So what we need is a number system for arrows, in which:

- adding numbers adds arrows tip to tail (two voltages in series add up);
- multiplying numbers stretches and turns arrows (a circuit makes a wave smaller and shifts its phase).

Complex numbers are exactly that system. Keep the picture of an arrow in your head through the whole lesson.

## The Concept

### Step 1: Multiplying by -1 is a half turn

Draw the ordinary number line. Take the number 3 and multiply it by -1: you get -3, the same distance from zero on the other side. Multiply by -1 again: back to 3.

```
     -3          0           3
  ----*----------+-----------*---->
      ^__________ half turn ___|
```

Think of the number as an arrow from 0 to 3. Multiplying by -1 **turns the arrow round by half a turn** (180 degrees). Doing it twice is a full turn, which is why (-1) x (-1) = +1. That is a perfectly good way to understand the strange school rule "minus times minus is plus".

### Step 2: A number that is a quarter turn

Now a puzzle. Is there a number that, applied **twice**, gives a half turn? That is, a number x with x x x = -1? On the number line, no: any real number squared is positive or zero. But in the arrow picture the answer is obvious: a **quarter turn**. Two quarter turns make a half turn.

So we invent a new number, call it j, and define it to mean "turn a quarter turn anticlockwise". Then:

```
j x j = -1          (read: "j times j equals minus one")
```

Mathematicians write this number i. Electrical engineers write **j**, because i is already taken for current. You may see "the square root of -1" as its definition. That is true, but "a quarter turn" tells you what it does.

Where does the arrow 1 go when you multiply it by j? A quarter turn up, off the number line, onto a new line at right angles to it. That vertical line holds the **imaginary numbers**: j, 2j, -0.5j, and so on. "Imaginary" is a bad historical name (Descartes meant it as an insult in 1637). They are no less real than negative numbers, which also once seemed absurd ("how can I have minus three cows?").

### Step 3: Powers of j go round a circle

Start at 1 and keep multiplying by j:

| Power | Value | Where the arrow points |
|---|---|---|
| j^0 | 1 | right (0 degrees) |
| j^1 | j | up (90 degrees) |
| j^2 | -1 | left (180 degrees) |
| j^3 | -j | down (270 degrees) |
| j^4 | 1 | right again (360 degrees) |
| j^5 | j | up... |

j^3 = j^2 x j = (-1) x j = -j. j^4 = j^2 x j^2 = (-1) x (-1) = 1. The pattern repeats every four steps, like a hand going round a clock face in quarter turns. One useful consequence: 1 / j = -j, because j x (-j) = -(j x j) = -(-1) = 1.

### Step 4: The complex plane

Combine the two lines. The horizontal line is the **real axis** (ordinary numbers), the vertical line is the **imaginary axis** (multiples of j). Every point on the sheet is a **complex number**, written

```
z = a + bj
```

Read it: "z equals a plus b j". a is the **real part** (how far across), b is the **imaginary part** (how far up). Both a and b are ordinary real numbers. Example: z1 = 3 + 4j is the point 3 across and 4 up, or the arrow from the origin to that point.

```
   imaginary
      ^
    4 +           * z1 = 3 + 4j
      |         /
    3 +       /
      |     /   size 5
    2 +   /
      | /  ) 53.13 degrees
    0 +-------+---+---+----> real
      0   1   2   3
   -2 +       * z2 = 1 - 2j   (1 across, 2 down)
```

This is the **rectangular form**, a + bj: like giving directions "3 blocks east and 4 blocks north".

### Step 5: Adding and subtracting: tip to tail

To add complex numbers, add the real parts together and the imaginary parts together:

```
(a + bj) + (c + dj) = (a + c) + (b + d)j
```

Worked: z1 = 3 + 4j and z2 = 1 - 2j.

- z1 + z2 = (3 + 1) + (4 + (-2))j = 4 + 2j.
- z1 - z2 = (3 - 1) + (4 - (-2))j = 2 + 6j.

Geometrically, addition puts the arrows tip to tail: walk along z1 (3 east, 4 north), then along z2 (1 east, 2 south), and you end at 4 east, 2 north. That is exactly how two series voltages will add in Lesson 05.

### Step 6: Multiplying: expand and use j x j = -1

Multiply like ordinary brackets (every term with every term), then replace j x j by -1:

```
(a + bj)(c + dj) = ac + adj + bcj + bd j^2
                 = (ac - bd) + (ad + bc)j
```

Worked: z1 x z2 = (3 + 4j)(1 - 2j).

- 3 x 1 = 3
- 3 x (-2j) = -6j
- 4j x 1 = 4j
- 4j x (-2j) = -8 j^2 = -8 x (-1) = +8

Add: 3 + 8 + (-6 + 4)j = 11 - 2j.

Multiplying by a plain real number just stretches: 2 x (3 + 4j) = 6 + 8j, same direction, twice as long. Multiplying by j turns a quarter: j x (3 + 4j) = 3j + 4j^2 = -4 + 3j. Check it on paper: the arrow (3, 4) turned 90 degrees anticlockwise is (-4, 3). Yes.

### Step 7: Size and angle (polar form)

The **magnitude** (size) of z = a + bj is the length of its arrow. The arrow, its across part and its up part form a right triangle, so by Pythagoras:

```
|z| = square root of (a^2 + b^2)
```

Read it: "the size of z is the square root of a squared plus b squared". For z1 = 3 + 4j: |z1| = sqrt(9 + 16) = sqrt(25) = 5. For z2 = 1 - 2j: |z2| = sqrt(1 + 4) = sqrt(5) = 2.2361.

The **angle** (also called the argument, or in circuits the phase) is the direction of the arrow, measured anticlockwise from the positive real axis. In a right triangle, tan(angle) = up / across, so angle = arctan(b / a), with one catch: arctan alone cannot tell 3 + 4j from -3 - 4j (both have b / a = 4/3). Computers use a two-argument version, **atan2(b, a)**, that looks at the signs of a and b separately and always picks the right quarter of the plane.

- z1: atan2(4, 3) = 53.130 degrees.
- z2: atan2(-2, 1) = -63.435 degrees (below the axis, so negative).

So z1 in **polar form** is "5 at 53.13 degrees", often written 5∠53.13°. Going back from polar to rectangular uses cosine and sine (Lesson 02: the across and up parts of a spinning arrow):

```
a = size x cos(angle)       b = size x sin(angle)
```

Check: 5 x cos(53.13°) = 5 x 0.6 = 3, and 5 x sin(53.13°) = 5 x 0.8 = 4. Back to 3 + 4j.

### Step 8: Why multiplication is "stretch and turn"

Look again at z1 x z2 = 11 - 2j. Its size is sqrt(121 + 4) = sqrt(125) = 11.180. And |z1| x |z2| = 5 x 2.2361 = 11.180. The same! Its angle is atan2(-2, 11) = -10.305 degrees, and 53.130 + (-63.435) = -10.305 degrees. The same again!

This is the most important fact of the lesson:

**When you multiply two complex numbers, their sizes multiply and their angles add.**

It follows from the cosine and sine addition rules of trigonometry, but you have already seen the special cases: multiplying by 2 (size 2, angle 0) stretches without turning; multiplying by j (size 1, angle 90°) turns without stretching; multiplying by -1 (size 1, angle 180°) is the half turn of Step 1.

And this is exactly what a circuit does to a sine wave: it scales the amplitude and shifts the phase. Multiplying by one complex number does both at once.

### Step 9: The conjugate and division

The **conjugate** of z = a + bj, written conj(z) or z*, flips the sign of the imaginary part: a - bj. It is the mirror image across the real axis: same size, opposite angle. Multiply a number by its own conjugate:

```
(a + bj)(a - bj) = a^2 - abj + abj - b^2 j^2 = a^2 + b^2
```

A plain real number, the size squared. For z1: (3 + 4j)(3 - 4j) = 9 + 16 = 25 = 5^2.

That gives us division. To compute z / w, multiply top and bottom by conj(w), which makes the bottom real:

```
z / w = (z x conj(w)) / (w x conj(w)) = (z x conj(w)) / |w|^2
```

Worked: z1 / z2 = (3 + 4j) / (1 - 2j).

1. conj(z2) = 1 + 2j.
2. Top: (3 + 4j)(1 + 2j) = 3 + 6j + 4j + 8j^2 = 3 - 8 + 10j = -5 + 10j.
3. Bottom: |z2|^2 = 1 + 4 = 5.
4. Result: (-5 + 10j) / 5 = -1 + 2j.

Check in polar: size 5 / 2.2361 = 2.2361 (and sqrt(1 + 4) = 2.2361), angle 53.130 - (-63.435) = 116.565 degrees (and atan2(2, -1) = 116.565 degrees). **Dividing divides the sizes and subtracts the angles.** A special case you will use constantly: 1 / j = -j, size 1, angle -90 degrees.

### Step 10: Euler's formula: the arrow as a single expression

An arrow of length 1 at angle theta (radians) has rectangular form cos(theta) + j sin(theta). In 1748, Leonhard Euler found that this same number can be written as a power of e = 2.71828...:

```
e^(j theta) = cos(theta) + j sin(theta)
```

Read it: "e to the j theta equals cos theta plus j sine theta". You do not need to prove it to use it, but you can check it. The number e^x can be computed by adding up a never-ending list of terms, 1 + x + x^2/2 + x^3/6 + x^4/24 + ..., each term being the previous one times x divided by the next counting number. Put x = j theta into that recipe, using complex multiplication, and the sum lands on cos(theta) + j sin(theta). The script does this with 30 terms and agrees with cos and sin to every printed digit.

Why is this so useful? Because the rule "sizes multiply, angles add" becomes the ordinary rule for powers:

```
e^(j alpha) x e^(j beta) = e^(j (alpha + beta))
```

Turning by alpha and then by beta is turning by alpha + beta, and the exponent does the bookkeeping for you. Any complex number can be written as size x e^(j angle); the polar form 5∠53.13° is just shorthand for 5 x e^(j x 0.9273) (53.13 degrees = 0.9273 radians).

A famous special case: theta = pi (half a turn): e^(j pi) = cos(pi) + j sin(pi) = -1 + 0j = -1. The half turn of Step 1.

### Step 11: The spinning arrow, at last

Let the angle grow with time: theta = omega x t. Then

```
e^(j omega t) = cos(omega t) + j sin(omega t)
```

is an arrow of length 1 spinning anticlockwise at omega radians per second. Its imaginary part (its height) is sin(omega t), the sine wave of Lesson 02. Multiply by a fixed complex number A e^(j phi):

```
A e^(j phi) x e^(j omega t) = A e^(j (omega t + phi))
```

an arrow of length A spinning at omega, starting at angle phi. Its height is A sin(omega t + phi): our general sine wave. So **a sine wave of known frequency is completely described by one complex number, A e^(j phi)**: its size is the amplitude, its angle the phase. That complex number is called a **phasor**, and it is the subject of Lesson 05.

### Step 12: Solving an equation that "had no solution"

Historically, complex numbers appeared in solving equations. Take x^2 - 4x + 13 = 0. The school formula x = (-b ± sqrt(b^2 - 4ac)) / (2a) with a = 1, b = -4, c = 13 gives b^2 - 4ac = 16 - 52 = -36. With only real numbers, you are stuck. With j, sqrt(-36) = 6j (because (6j)^2 = 36 j^2 = -36), so

```
x = (4 ± 6j) / 2 = 2 + 3j   or   2 - 3j
```

Check 2 + 3j: x^2 = (2 + 3j)^2 = 4 + 12j + 9j^2 = -5 + 12j; -4x = -8 - 12j; add 13: -5 - 8 + 13 + (12 - 12)j = 0. It works. In Phase 10, equations like this one describe resonant circuits, and the complex solutions tell you that the circuit rings like a bell.

## Build It

The script first implements complex numbers from scratch as pairs of ordinary numbers (real part, imaginary part), using only the rules above, then compares with Python's built-in complex type.

### Step 1: The rules as functions

```python
def add(z, w):
    return (z[0] + w[0], z[1] + w[1])


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
```

`multiply` is the formula (ac - bd) + (ad + bc)j from Step 6, nothing more. `divide` is "multiply by the conjugate, divide by the size squared" from Step 9. A pair like `(3.0, 4.0)` stands for 3 + 4j.

### Step 2: Powers of j

Starting from `(1.0, 0.0)` and multiplying by `j = (0.0, 1.0)` eight times prints 1, j, -1, -j, 1, j, -1, -j with angles 0, 90, 180, 270, 0, ... degrees.

### Step 3: Arithmetic and polar form

The script prints exactly the worked examples: z1 + z2 = 4 + 2j, z1 - z2 = 2 + 6j, z1 x z2 = 11 - 2j, z1 x conj(z1) = 25, z1 / z2 = -1 + 2j, then sizes and angles, showing that 5 x 2.2361 = 11.1803 and 53.130 + (-63.435) = -10.305 degrees.

### Step 4: Euler's formula by adding a series

```python
def exp_j_by_series(theta, terms=30):
    total = (0.0, 0.0)
    term = (1.0, 0.0)
    for n in range(terms):
        total = add(total, term)
        term = multiply(term, (0.0, theta / (n + 1)))
    return total
```

Each new term is the previous one times (j theta) / (n + 1), which builds 1, j theta, (j theta)^2 / 2, (j theta)^3 / 6, ... For theta = 1 rad the sum is 0.5403 + 0.8415j, equal to cos(1) + j sin(1). For theta = pi it is -1.

### Step 5: Rotation

Multiplying the arrow 1 by `from_polar(1.0, 30.0)` twelve times turns it 30 degrees each time: after 3 steps it points at 90 degrees (it is j), after 6 at 180 (-1), after 12 back at 0.

### Step 6: The quadratic

The script finds x = 2 + 3j and 2 - 3j and plugs each back in to get 0 + 0j.

### Step 7: Python's built-in complex numbers

```python
p1, p2 = 3 + 4j, 1 - 2j
print(f"  (3+4j) * (1-2j) = {p1 * p2}")
print(f"  (3+4j) / (1-2j) = {p1 / p2}")
print(f"  abs(3+4j) = {abs(p1)},  cmath.phase(3+4j) = {math.degrees(cmath.phase(p1)):.3f} deg")
print(f"  cmath.exp(1j * pi) = {cmath.exp(1j * math.pi):.4f}")
print(f"  cmath.rect(5, 0.9273) = {cmath.rect(5, 0.9273):.4f}")
```

Python writes the imaginary unit as `j` too: `4j` is a number, and `1j` is j itself. `abs` gives the size, `cmath.phase` the angle in radians, `cmath.rect(size, angle)` builds from polar form. The results agree with our hand-made functions: (11-2j), (-1+2j), 5.0, 53.130 degrees, (-1.0000+0.0000j) and (3.0000+4.0000j). (The `-1` from `exp(1j * pi)` shows a tiny leftover imaginary part, around 1e-16, from rounding.)

### Step 8: The simulator speaks complex

```python
circuit = Circuit()
circuit.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
circuit.resistor("R1", "in", "out", 1000.0)
circuit.capacitor("C1", "out", "0", 159.15e-9)
result = circuit.ac([1000.0], source="V1")
v_out = complex(result.v("out")[0])
```

`ac()` is our simulator's AC analysis. It treats the source as the complex number 1 (size 1, angle 0) and returns the voltage of each node as a complex number, without simulating any time steps. For the RC circuit of Lesson 02 it returns 0.5 - 0.5j V: size sqrt(0.25 + 0.25) = 0.7071, angle atan2(-0.5, 0.5) = -45 degrees. Exactly the 0.7071 V and 45 degree lag we measured with ten cycles of time simulation, in one line. Lessons 05 and 06 show where that 0.5 - 0.5j comes from.

## Use It

- **AC circuit analysis.** Every AC tool, from the hand calculations of Lesson 06 to SPICE's ".ac" analysis and the network analysers in RF labs, works with complex voltages and currents.
- **Datasheets.** Impedances of antennas, cables and speaker drivers are given as R + jX (real and imaginary parts) or as size and phase; RF engineers plot them on a special complex-plane chart called the Smith chart.
- **Signal processing.** The Fourier transform (Phase 19) turns a recorded signal into complex numbers, one per frequency, each with an amplitude and a phase.
- **Control systems and filters.** The "poles" of a filter (Phase 10) are complex solutions of equations like the quadratic in Step 12; their position on the complex plane tells you how the circuit rings.
- **Python and numpy.** `numpy` arrays can hold complex numbers (`dtype=complex`), and `np.abs`, `np.angle`, `np.conj` work element by element. Our simulator's `ac()` returns such arrays.

## Common Mistakes

- **Forgetting that j x j = -1 when multiplying.** (3 + 4j)(1 - 2j) is 11 - 2j, not -5 - 2j. The -8 j^2 becomes +8.
- **Using arctan(b / a) instead of atan2(b, a).** -3 - 4j has angle -126.87 degrees, not 53.13 degrees. Always use `math.atan2(b, a)` or `cmath.phase`.
- **Dividing parts separately.** (3 + 4j) / (1 - 2j) is not 3/1 + (4/-2)j. Multiply by the conjugate.
- **Mixing degrees and radians.** `cmath.rect` and `cmath.exp` use radians. 53.13 degrees is 0.9273 rad.
- **Thinking "imaginary" means "not physical".** The imaginary part of a voltage phasor is as physical as the real part: it tells you about the part of the wave that is a quarter cycle out of step.
- **Writing `j` alone in Python.** Python needs a number in front: `1j`, not `j`.

## Exercises

1. **Quarter turns.** Compute j^6, j^11 and 1 / j^3. Then draw 2 + j, multiply it by j, and draw the result. By how many degrees did it turn?
2. **Rectangular arithmetic.** With a = 2 - 3j and b = -1 + 4j, compute a + b, a - b, a x b and a / b by hand. Check with Python.
3. **Polar.** Convert -4 + 4j and 0.5 - 0.866j into polar form (size and angle in degrees). Convert 10∠-30° and 2∠135° into rectangular form.
4. **Stretch and turn.** Use polar form to compute (2∠40°) x (3∠-70°) and (2∠40°) / (3∠-70°). Convert both results to rectangular form and verify by multiplying and dividing in rectangular form.
5. **Equation and simulator.** Solve x^2 + 2x + 5 = 0 with complex numbers and check both roots in Python. Then change the capacitor in Step 8 to 318.3 nF: predict V(out) with the formula 1 / (1 + j x omega x R x C) (Lesson 06 explains it), using omega x R x C = 2, and compare with the simulator.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| j | "The square root of minus one" | The number with j x j = -1; geometrically, a rotation by 90 degrees |
| Complex number | "A number with an imaginary part" | a + bj with real a and b; a point or arrow in the plane |
| Real part, imaginary part | "The normal bit and the j bit" | The horizontal and vertical coordinates of the arrow |
| Magnitude | "The size", "the modulus", "abs" | Length of the arrow, sqrt(a^2 + b^2) |
| Angle | "The phase", "the argument" | Direction of the arrow, atan2(b, a), measured anticlockwise from the real axis |
| Polar form | "Size and angle" | r∠theta = r e^(j theta) = r cos(theta) + j r sin(theta) |
| Conjugate | "Flip the sign of j" | a - bj; same size, opposite angle; z x conj(z) = abs(z)^2 |
| Euler's formula | "e to the j theta" | e^(j theta) = cos(theta) + j sin(theta), the unit arrow at angle theta |

## Further Reading

- [BetterExplained: A Visual, Intuitive Guide to Imaginary Numbers](https://betterexplained.com/articles/a-visual-intuitive-guide-to-imaginary-numbers/) — the "rotation" view of j, with lovely pictures.
- [Khan Academy: Complex numbers (Precalculus)](https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:complex) — short practice-driven videos on rectangular and polar forms, multiplication and division.
- [All About Circuits, Vol. II (AC), Chapter 2: Complex Numbers](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-2/introduction-to-complex-numbers/) — complex numbers explained specifically for AC circuits.
- [Feynman Lectures on Physics, Vol. I, Chapter 22: Algebra](https://www.feynmanlectures.caltech.edu/I_22.html) — Feynman builds numbers up to complex exponentials and calls Euler's formula "our jewel".
