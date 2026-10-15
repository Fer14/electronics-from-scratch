# AC Analysis in Our Simulator

> AC analysis is the DC nodal analysis you already built, with one change: every number becomes complex and every part's conductance depends on frequency.

**Type:** Build
**Prerequisites:** Phase 05 (Circuit Analysis and Our Simulator), Lessons 04 (Modified Nodal Analysis from Scratch) and 08 (Dependent Sources); Phase 09 (Alternating Current), Lessons 04 (Complex Numbers for Circuits), 05 (Phasors) and 06 (Impedance); Phase 10 (Filters and Resonance), Lessons 01 to 07
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| AC analysis | Solving a circuit for steady sine waves at one frequency at a time, using phasors | Asking "what does this circuit do to a 1 kHz tone?" and getting the answer in one step |
| Small-signal / frequency-domain analysis | Other names for AC analysis | Looking at the recipe instead of watching the cake bake |
| Admittance (Y) | The inverse of impedance, Y = 1/Z, in siemens (S); the AC version of conductance | How easily current flows: the width of the pipe instead of its narrowness |
| Complex MNA | Modified nodal analysis where every entry of the matrix is a complex number | The DC matrix from Phase 05, written in "arrow numbers" |
| Stamp | The small fixed pattern of numbers a part adds into the matrix (Phase 05) | A rubber stamp pressed wherever the part sits |
| Frequency sweep | Solving the same circuit at many frequencies to draw its Bode plot | Playing every note on a piano and writing down how loud each one comes out |
| Steady state | The behaviour after all start-up transients have died out | The swing after it has settled into its rhythm |
| gmin | A tiny conductance (10^-12 S) a simulator adds from every node to ground so the matrix is never singular | A hair-thin wire that keeps a floating node from being undefined |

## Learning Objectives

- Explain why a linear circuit driven by a sine can be solved with complex phasors instead of time steps
- Write the complex MNA stamps for resistors, capacitors, inductors, voltage sources and voltage-controlled voltage sources
- Build a small AC solver in numpy that returns node phasors at any frequency, and sweep it to draw Bode plots
- Compare our solver with `sim`'s `Circuit.ac` on four circuits and explain the tiny differences
- Check that an AC phasor predicts the amplitude and phase a transient simulation shows after it settles

## The Problem

Throughout this phase we called `c.ac(freqs, source="V1")` and trusted the answer. Every Bode plot, every cutoff and every lab check in Phase 10 came from that one call. A from-scratch course should not have black boxes. How does the simulator turn a schematic into a frequency response?

There is a slow way: run a transient simulation (Phase 07, Lesson 08) with a sine source at each frequency, wait for the start-up wobble to die out (with a high-Q circuit, hundreds of cycles), and measure the output amplitude and phase. For a 600-point Bode plot that is 600 long simulations. There is a fast way: use phasors. Each frequency then costs one small linear solve, the same work as one DC operating point. This lesson builds the fast way, line by line, and checks it against both `sim` and the slow way.

## The Physics

### Why phasors are allowed

Phase 09 showed that, for a circuit made of resistors, capacitors, inductors, sources and linear dependent sources, a sine input at frequency f produces, once the transients have died out, sines at the *same* frequency everywhere in the circuit. Only amplitudes and phases differ. We can describe each of those sines by one complex number, its **phasor**: the size is the amplitude, the angle is the phase. (This course uses the sine convention: a phasor P means the voltage P_amplitude x sin(2 pi f t + phase), Phase 09, Lesson 05.)

The two things that make phasors work:

1. **Kirchhoff's laws still hold for phasors.** Adding sines of the same frequency gives a sine of that frequency, and adding the sines is the same as adding their phasors (adding arrows). So "currents into a node sum to zero" becomes "current phasors into a node sum to zero".
2. **Each part becomes a complex Ohm's law.** Taking the derivative of a sine multiplies its phasor by j omega (it rotates the arrow by 90° and scales it by omega = 2 pi f). So:
   - Resistor: V = R I.
   - Capacitor: i = C dv/dt becomes I = j omega C V.
   - Inductor: v = L di/dt becomes V = j omega L I, so I = V / (j omega L).

Every part has a complex **admittance** Y = I / V:

| Part | Impedance Z | Admittance Y = 1/Z |
|---|---|---|
| Resistor R | R | 1 / R |
| Capacitor C | 1 / (j omega C) | j omega C |
| Inductor L | j omega L | 1 / (j omega L) = -j / (omega L) |

At DC (omega = 0) the capacitor's admittance is 0 (an open) and the inductor's is infinite (a short). That is why DC analysis treats them as open and short, and why our simple solver below only works for omega > 0 (the real `sim` handles inductors with an extra current unknown instead, which also works at DC).

### Nothing else changes

That is the whole physics. With admittances, the AC circuit at one frequency looks exactly like a DC circuit of conductances, except the numbers are complex. So the **modified nodal analysis** from Phase 05, Lesson 04 works unchanged: one equation per node (KCL), one extra equation per voltage source, a matrix equation A x = z, solved with linear algebra. numpy's `np.linalg.solve` happily solves complex systems.

## The Concept

### The unknowns

For a circuit with N non-ground nodes and M voltage sources (independent or dependent), the unknowns are:

- the N node voltage phasors V_1 ... V_N,
- the M currents through the voltage sources.

The matrix A is (N + M) x (N + M), complex. The right-hand side z holds the source phasors.

### The stamps

**Admittance between nodes a and b** (resistor, capacitor or inductor), with Y from the table:

```
            col a    col b
  row a  [   +Y       -Y   ]
  row b  [   -Y       +Y   ]
```

Read it: "a current Y (V_a - V_b) leaves node a and enters node b". It is the DC resistor stamp with 1/R replaced by Y. If a or b is ground, that row and column are simply skipped.

**Independent voltage source** from plus node p to minus node m, with branch current unknown k and phasor value E:

```
            col p   col m   col k        z
  row p  [                   +1   ]   [  0 ]
  row m  [                   -1   ]   [  0 ]
  row k  [   +1      -1           ]   [  E ]
```

The +1 and -1 in column k put the source's current into the KCL equations of p and m. Row k says V_p - V_m = E. The **AC source** has E = 1 (a 1 V sine of phase 0); every other independent voltage source has E = 0 (it becomes a short circuit at AC, because only one source drives the circuit, as in `sim`).

**Voltage-controlled voltage source** (vcvs) with output p, m, control cp, cm and gain A (Phase 05, Lesson 08):

```
            col p   col m   col cp   col cm   col k      z
  row p  [                                     +1  ]  [ 0 ]
  row m  [                                     -1  ]  [ 0 ]
  row k  [   +1      -1      -A       +A           ]  [ 0 ]
```

Row k says V_p - V_m - A (V_cp - V_cm) = 0.

### Worked example: the RC low-pass at fc

R = 1 k ohm from "in" to "out", C = 100 nF from "out" to ground, source V1 from "in" to ground. fc = 1591.5 Hz, so omega = 2 pi x 1591.5 = 10,000 rad/s and the capacitor's admittance is j omega C = j x 10,000 x 1e-7 = j 0.001 S. The resistor's is 1/1000 = 0.001 S. Unknowns: V_in, V_out, I_V1.

```
          V_in       V_out             I_V1        z
in    [  +0.001     -0.001             +1   ]   [ 0 ]
out   [  -0.001     +0.001 + j0.001     0   ]   [ 0 ]
V1    [  +1          0                  0   ]   [ 1 ]
```

- Row V1: V_in = 1.
- Row out: -0.001 x 1 + (0.001 + 0.001j) V_out = 0, so V_out = 0.001 / (0.001 + 0.001j) = 1 / (1 + j) = 0.5 - 0.5j.

|V_out| = 0.707, phase -45°: the cutoff, exactly as Lesson 02 predicted. Row "in" gives the source current: 0.001 (1 - V_out) + I_V1 = 0, so I_V1 = -0.001 x (0.5 + 0.5j); the minus sign is the MNA convention that I_V1 flows from plus to minus *through* the source.

### The sweep

A Bode plot is just this solve repeated for every frequency in a list. The matrix must be rebuilt each time because the capacitor and inductor admittances change with omega. For small circuits that costs microseconds per point.

### Why `sim` differs by 10^-8 dB

When you run the comparison, our solver and `sim` agree to about 10^-8 dB. The difference is deliberate: `sim` adds a tiny conductance **gmin = 10^-12 S** from every node to ground (Phase 05) so that a node connected only through capacitors, or to nothing, never makes the matrix singular. At the 1 to 10 k ohm levels of our circuits, a 10^12 ohm leak changes the results in the eighth or ninth digit. Our hand-built solver has no gmin, so it will fail with a "singular matrix" error on a floating node, exactly as the DC solver in Phase 05 did.

### AC analysis of nonlinear circuits

Diodes and transistors (Phases 11 and 12) are not linear, so phasors do not strictly apply. Simulators handle them by first finding the DC operating point, then replacing each nonlinear part by its *small-signal* linear model at that point (a small resistance for a diode, a transconductance for a transistor), and finally doing exactly the AC analysis of this lesson. `sim.Circuit.ac` does this: it calls the DC solver first and then asks every part for its linearised AC stamp. The result is valid for small signals around the operating point (Phase 12, Lesson 07).

## Build It

### Step 1: A tiny netlist

```python
class AcNetlist:
    def __init__(self):
        self.parts = []

    def resistor(self, name, a, b, ohms):
        self.parts.append(("R", name, a, b, ohms))

    def capacitor(self, name, a, b, farads):
        self.parts.append(("C", name, a, b, farads))

    def inductor(self, name, a, b, henries):
        self.parts.append(("L", name, a, b, henries))

    def voltage_source(self, name, plus, minus, phasor=1.0):
        self.parts.append(("V", name, plus, minus, phasor))

    def vcvs(self, name, plus, minus, cplus, cminus, gain):
        self.parts.append(("E", name, plus, minus, (cplus, cminus, gain)))
```

Each part is stored as a tuple: kind, name, two nodes, and a value. The method `nodes()` collects every node name except ground ("0") in order of first appearance, and they become the first N unknowns.

### Step 2: Admittances

```python
def admittance_of(kind, value, omega):
    if kind == "R":
        return 1 / value
    if kind == "C":
        return 1j * omega * value
    return 1 / (1j * omega * value)
```

The three lines of the admittance table, in Python. `1j` is j.

### Step 3: Building the matrix with stamps

```python
    def build(self, freq):
        omega = 2 * math.pi * freq
        nodes = self.nodes()
        index = {node: i for i, node in enumerate(nodes)}
        branches = [p for p in self.parts if p[0] in ("V", "E")]
        size = len(nodes) + len(branches)
        matrix = np.zeros((size, size), complex)
        rhs = np.zeros(size, complex)

        def add(row, col, value):
            if row is not None and col is not None:
                matrix[row, col] += value

        def at(node):
            return None if node == GROUND else index[node]

        for kind, name, a, b, value in self.parts:
            if kind in ("R", "C", "L"):
                admittance = admittance_of(kind, value, omega)
                add(at(a), at(a), admittance)
                add(at(b), at(b), admittance)
                add(at(a), at(b), -admittance)
                add(at(b), at(a), -admittance)
        for k, (kind, name, a, b, value) in enumerate(branches):
            row = len(nodes) + k
            add(at(a), row, 1)
            add(at(b), row, -1)
            add(row, at(a), 1)
            add(row, at(b), -1)
            if kind == "V":
                rhs[row] = value
            else:
                cplus, cminus, gain = value
                add(row, at(cplus), -gain)
                add(row, at(cminus), gain)
        return nodes, matrix, rhs
```

`at(node)` returns `None` for ground, and `add` silently ignores any entry with a `None` row or column: that is how "skip the ground row and column" is implemented without special cases. The two loops are the three stamps of the Concept section, entry by entry. `np.zeros(..., complex)` makes the matrix complex from the start.

### Step 4: Solving and sweeping

```python
    def solve(self, freq):
        nodes, matrix, rhs = self.build(freq)
        x = np.linalg.solve(matrix, rhs)
        voltages = {node: x[i] for i, node in enumerate(nodes)}
        voltages[GROUND] = 0j
        return voltages

    def sweep(self, freqs, node):
        return np.array([self.solve(f)[node] for f in freqs])
```

The script first prints the matrix of the worked example:

```
  unknowns: ['in', 'out', 'I(V1)']
  [ +0.0010+0.0000j  -0.0010+0.0000j  +1.0000+0.0000j ]   rhs +0.0
  [ -0.0010+0.0000j  +0.0010+0.0010j  +0.0000+0.0000j ]   rhs +0.0
  [ +1.0000+0.0000j  +0.0000+0.0000j  +0.0000+0.0000j ]   rhs +1.0
  V(out) at fc = +0.5000 -0.5000j, |V| = 0.7071, phase -45.0 deg
```

Compare it with the hand-written matrix above: identical.

### Step 5: Against `sim`, on four circuits

A helper `describe` builds the same netlist twice, once in our `AcNetlist` and once in a `sim.Circuit`, so the comparison is fair. The four circuits are the stars of this phase: the RC low-pass (Lesson 02), the series RLC band-pass (Lessons 05 and 07), the LC notch (Lesson 06) and the buffered two-stage low-pass (Lesson 03). We sweep 601 frequencies from 1 Hz to 1 MHz:

```
  RC low-pass      : max gain difference 8.69e-09 dB, max phase difference 2.86e-08 deg
  RLC band-pass    : max gain difference 8.55e-09 dB, max phase difference 3.11e-08 deg
  LC notch         : max gain difference 8.07e-08 dB, max phase difference 3.08e-07 deg
  buffered 2-stage : max gain difference 1.74e-08 dB, max phase difference 5.73e-08 deg
```

Agreement to a hundred-millionth of a decibel: the size of `sim`'s gmin. The phase difference is measured as the angle of our phasor divided by theirs, which avoids any confusion from angles wrapping around ±180°.

### Step 6: Against the formula

For the RC low-pass, our sweep matches 1 / (1 + j f/fc) to 2.3e-16, which is the rounding limit of 64-bit floating point numbers. No gmin, no difference.

### Step 7: A phasor is a promise about the time domain

The phasor claims: "after settling, the output is |V| sin(2 pi f t + phase)". Let us check that promise with the slow method. We drive the RLC band-pass at 1400 Hz (a bit below its 1592 Hz resonance) in a transient simulation for 60 cycles, keep cycles 50 to 60 (well settled for Q = 10; Lesson 07 says about Q cycles), and extract the amplitude and phase of the 1400 Hz component:

```python
reference = np.exp(1j * 2 * math.pi * f_test * t[last])
measured = 2j * np.mean(v[last] * np.conj(reference))
```

Multiplying a sine by e^(-j omega t) and averaging over whole cycles picks out its phasor (this is one "bin" of a Fourier transform, Lesson 01). Because sin(x) = (e^(jx) - e^(-jx)) / (2j), the average equals P / (2j), so we multiply by 2j to recover P.

```
  AC phasor at 1400 Hz:       |V| = 0.3624, phase  +68.75 deg
  transient, after settling:  |V| = 0.3624, phase  +68.75 deg
```

The output leads the input by 68.75° (below resonance the series circuit is capacitive, Lesson 05). The transient simulation took 30,000 time steps; the AC analysis took one 4 x 4 solve.

### Step 8: The picture

`save_bode` draws all four Bode plots from our own solver into `out.png`: the RC's gentle -20 dB per decade, the two-stage's -40 dB per decade and -180° phase, the RLC's sharp peak with its 180° phase swing, and the LC notch's deep dip at 50 Hz.

## Use It

- **Every SPICE has an `.AC` analysis** that does exactly this: `.AC DEC 100 1 1MEG` sweeps 100 points per decade from 1 Hz to 1 MHz. LTspice, ngspice and the simulators built into PCB tools (Phase 21) all do complex MNA with gmin.
- **Small-signal amplifier design.** After Phase 12 you will run AC analysis on transistor amplifiers to read their gain and bandwidth from Bode plots, built on the linearised models this lesson mentioned.
- **Stability analysis.** Engineers break a feedback loop in simulation and run AC analysis to see the loop gain and phase margin (Phase 13 and Phase 18).
- **Filter design tools** (such as the TI Filter Design Tool or Analog Devices' filter wizard) compute exactly these complex transfer functions to show you a Bode plot before you build anything.
- **Network analysers** measure the same complex response on a real circuit: a real-world `c.ac()`.

## Common Mistakes

- **Running AC analysis at f = 0 with inductors as admittances.** 1 / (j x 0 x L) divides by zero. Use DC analysis for DC, or model inductors with a branch current as `sim` does.
- **Expecting AC analysis to show clipping or distortion.** It is linear. A 1 V AC source gives the same *relative* answer as a 1000 V one. For large signals use transient analysis.
- **Forgetting that AC analysis only uses one source.** All other independent sources are set to zero (voltage sources become shorts, current sources opens). That is superposition (Phase 05).
- **Comparing phases without unwrapping.** A phase of +179° and -181° are the same angle. Compare phasors by dividing them, or unwrap.
- **Leaving a node floating.** A node connected only through capacitors to the rest of the circuit has no DC path; our gmin-free solver can still solve it at AC (capacitors conduct), but a node connected to nothing makes the matrix singular.

## Exercises

1. **Easy.** By hand, write the 3 x 3 complex MNA matrix of an RL low-pass (L = 10 mH from in to out, R = 100 ohm from out to ground) at f = 1591.5 Hz, and solve for V(out).
2. **Easy.** Use `AcNetlist` to compute the gain in dB of the RLC band-pass at 1592 Hz, 1514 Hz and 1673 Hz. Compare with Lesson 07.
3. **Medium.** Add a `current_source(name, a, b)` part to `AcNetlist` that injects a phasor current of 1 from a to b (stamp: z[a] -= 1, z[b] += 1). Use it to compute the impedance of a parallel LC tank (L = 10 mH, C = 1 µF, 1 ohm in series with L) versus frequency: Z = V / 1 A.
4. **Medium.** Add a `vccs` (voltage-controlled current source, Phase 05) stamp to `AcNetlist`. Build a one-transistor-like amplifier: a vccs with gm = 0.01 S from the output node to ground controlled by the input, with a 5 k ohm load in parallel with 1 nF at the output. Plot its gain. What is its low-frequency gain and its -3 dB frequency?
5. **Hard.** Time both methods: measure how long `ours.sweep(freqs, "out")` takes for 601 points, and how long the transient method of Step 7 would take for the same 601 points (time one and multiply). How many times faster is AC analysis? Then explain in your own words what physical assumption makes it valid.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| AC analysis | "The .AC sweep" | Solving the circuit in the frequency domain with complex phasors, one linear solve per frequency |
| Admittance | "1 over Z" | Y = I / V for a part: 1/R, j omega C, or 1/(j omega L), in siemens |
| Complex MNA | "The AC matrix" | Modified nodal analysis with complex admittance stamps and source phasors |
| Stamp | "How a part enters the matrix" | The fixed pattern of +Y and -Y (or +1 and -1) entries each part adds |
| gmin | "Leak to ground" | A 10^-12 S conductance added at every node to keep the matrix solvable |
| Small-signal model | "Linearised device" | A nonlinear device replaced by its linear behaviour around the DC operating point, so AC analysis applies |
| Steady state | "After it settles" | The pure sinusoidal response that remains once transients decay; what a phasor describes |

## Further Reading

- [Ho, Ruehli and Brennan, "The modified nodal approach to network analysis", IEEE Transactions on Circuits and Systems, 1975](https://ieeexplore.ieee.org/document/1084079) — the original MNA paper behind SPICE
- [MIT OpenCourseWare 6.002, lectures on the impedance model and sinusoidal steady state](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — why phasors turn differential equations into algebra
- [ngspice user manual, chapter on the .AC analysis](https://ngspice.sourceforge.io/docs.html) — how a real SPICE sets up and runs a frequency sweep
- Lawrence Pillage, Ronald Rohrer and Chandramouli Visweswariah, *Electronic Circuit and System Simulation Methods* (McGraw-Hill, 1995) — the textbook on how circuit simulators work inside
