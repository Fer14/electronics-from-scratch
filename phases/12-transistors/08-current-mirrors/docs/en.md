# Current Mirrors

> Two identical transistors with the same base-emitter voltage carry the same current. Force a current through one, and the other copies it into whatever load you connect, as long as the load leaves it some room.

**Type:** Build
**Prerequisites:** 12-02 (The BJT), 12-04 (The MOSFET), 12-07 (Small-Signal Thinking); Phase 06 (Sources, Batteries and Measurement), lesson 01-ideal-and-real-sources
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Current source | A circuit that delivers a set current regardless of the voltage across its load (Phase 06) | A metering pump that delivers the same litres per minute whatever the pipe |
| Current mirror | Two matched transistors sharing a control voltage, so one copies the other's current | A photocopier for current |
| Reference current (I_REF) | The current forced into the input side of the mirror | The original you put on the copier glass |
| Diode-connected transistor | A transistor with its base tied to its collector (or gate to drain), so it behaves like a diode | A tap whose handle is linked to its own outlet: it opens just enough for what flows |
| Matched transistors | Transistors made side by side so their I_S (or k, V_th) are equal | Twins |
| Compliance (voltage) | The range of output voltage over which the mirror still delivers its current | The range of pipe pressures the pump can handle |
| Output resistance | How much the output current changes with output voltage: ΔV / ΔI, ideally infinite | How "stiff" the pump is |
| Early effect / channel-length modulation | The slight increase of output current with output voltage in real BJTs / MOSFETs | A pump that leaks a bit faster at higher pressure |
| Emitter area ratio | Making one transistor N times larger so it carries N times the current | A copier set to N× enlargement |
| Active load | A current mirror used in place of a collector resistor in an amplifier | A spring that pulls with constant force instead of a rubber band |

## Learning Objectives

- Explain why two matched BJTs with the same V_BE carry the same collector current.
- Design a basic BJT mirror: choose R_REF for a given output current and estimate the β error, β/(β+2).
- Find the compliance limit where the output transistor saturates.
- Scale a mirror with area ratios, and build the MOSFET version.
- Explain output resistance and why real mirrors are not perfect current sources.

## The Problem

Many circuits need a *current*, not a voltage: charging a capacitor linearly to make a ramp (Phase 13), biasing a sensor such as a thermistor or a photodiode, biasing every transistor inside an op-amp, driving LEDs evenly. A resistor from the supply is a poor current source: its current changes with the voltage at its far end.

In lesson 02 we saw that a BJT's collector is a current source: in the active region the curves are flat. But that current depends exponentially on V_BE and directly on I_S, both of which vary with temperature and from part to part. We need a way to set that current precisely without knowing I_S. The answer is elegant: let a second, identical transistor measure the right V_BE for us.

## The Physics

### The key fact: same V_BE, same current

From lesson 02, in the active region I_C = I_S e^(V_BE / V_T). Two transistors made side by side on the same chip (or the same die in a dual-transistor package) have the same I_S and the same temperature. If they also have the **same V_BE**, they carry the **same collector current**, whatever I_S and T happen to be. We don't need to know the exponential; we only need two copies of it.

### The diode-connected transistor

How do we find the V_BE that corresponds to the current we want? Tie a transistor's base to its collector and push a current into that node:

```
      I_REF
        |
        +----+
        |    |
        c    |
   b ---+----+    base and collector connected
        |Q1
        e
        |
      ground
```

Now V_CB = 0, so the transistor is still in its active region (BC not forward biased), and all the current entering the node must go into the collector or the base. The transistor automatically settles at whatever V_BE makes I_C + I_B = I_REF. It behaves like a diode, which is why it's called **diode-connected**. Its V_BE is "the answer" for that current.

### The mirror

Connect a second transistor's base-emitter in parallel with Q1's:

```
        +V_CC ----+-------------------+
                  |                   |
               [R_REF]             [R_LOAD]
                  |                   |
                  +----+              +---- out
                  |    |              |
                  c    |              c
             b ---+----+------------- b
                  |Q1                 |Q2
                  e                   e
                  |                   |
        ground ---+-------------------+
```

Q2 has exactly Q1's V_BE, so its collector current equals Q1's: Q2 **mirrors** I_REF into the load. And because Q2's collector is a current source, that current hardly depends on the load.

What the analogy gets wrong: a photocopier makes a copy that then lives its own life. The mirror's copy depends on the original *continuously*: change I_REF and the output follows instantly.

## The Concept

### Setting I_REF

Q1's collector-base node sits one V_BE (about 0.65 V) above ground, so

```
I_REF = (V_CC − V_BE) / R_REF
```

For V_CC = 5 V and R_REF = 4.7 kΩ: I_REF = (5 − 0.65) / 4700 = 0.926 mA. The simulator: V_BE = 0.6523 V, I_REF = **0.9251 mA**.

### The β error

I_REF feeds three currents: Q1's collector and *two* base currents (Q1's and Q2's). With both collectors equal to I_C:

```
I_REF = I_C + 2 I_C / β    →    I_OUT = I_C = I_REF × β / (β + 2)
```

Read: "the output equals the reference times beta over beta plus two". For β = 100: 100/102 = 0.9804. The simulator: **I_OUT = 0.9069 mA**, ratio 0.9804 exactly. Versus β:

| β | I_OUT / I_REF (simulator) | β / (β + 2) |
|---|---|---|
| 20 | 0.9091 | 0.9091 |
| 50 | 0.9615 | 0.9615 |
| 100 | 0.9804 | 0.9804 |
| 300 | 0.9934 | 0.9934 |

A 2 % error at β = 100, smaller than resistor tolerance. (Improved mirrors add a third transistor to supply the base currents and cut the error to about 2/β².)

### Load independence and compliance

With R_REF = 4.7 kΩ, vary the load:

| R_load | I_OUT | V_CE(Q2) |
|---|---|---|
| 100 Ω | 0.9069 mA | 4.909 V |
| 1 kΩ | 0.9069 mA | 4.093 V |
| 2.2 kΩ | 0.9069 mA | 3.005 V |
| 4.3 kΩ | 0.9069 mA | 1.100 V |
| 4.7 kΩ | 0.9069 mA | 0.738 V |
| 5.6 kΩ | 0.8727 mA | 0.113 V |
| 10 kΩ | 0.4956 mA | 0.044 V |

From 100 Ω to 4.7 kΩ, a 47-fold change in load, the current does not move in the fourth digit. That is a current source. But it can only push its current as long as the load leaves Q2 enough V_CE to stay active (about 0.2-0.3 V). The largest load is

```
R_max ≈ (V_CC − V_CE,min) / I_OUT = (5 − 0.2) / 0.907 mA ≈ 5.3 kΩ
```

Beyond it (5.6 kΩ, 10 kΩ) Q2 saturates and the circuit becomes "a resistor from 5 V": I = (5 − 0.05)/10 kΩ = 0.495 mA. The range of output voltages over which the mirror works is its **compliance**: here from about 0.2 V to 5 V at the collector.

### Output resistance: why "perfect" is too perfect

Our simulator's BJT has no Early effect, so its mirror's output current is *exactly* constant in the active region: an infinite output resistance. Real BJTs have an output resistance r_o = V_A / I_C, where V_A (the Early voltage) is typically 50-150 V. A 2N3904 with V_A ≈ 100 V at 1 mA has r_o ≈ 100 kΩ: the output current rises about 1 % per volt of output voltage. Cascode and Wilson mirrors (with extra transistors) raise the output resistance to tens of megohms.

The MOSFET model in our simulator does include the equivalent effect (channel-length modulation, parameter λ, "lambda"), so we can see it there.

### The supply sensitivity

The mirror copies I_REF faithfully, but I_REF itself comes from a resistor:

```
supply 4.5 V: I_OUT = 0.8033 mA
supply 5.0 V: I_OUT = 0.9069 mA
supply 5.5 V: I_OUT = 1.0106 mA
```

A 10 % supply change gives an 11 % current change. For a supply-independent reference, I_REF is generated from a bandgap reference or from a zener (lesson 11-08) and an op-amp (Phase 13).

### Scaling: mirrors that multiply

Make Q2 with N times the emitter area. Its I_S is N times larger, so at the same V_BE it carries N times the current:

```
area x1: I_OUT / I_REF = 0.980
area x2: I_OUT / I_REF = 1.942
area x4: I_OUT / I_REF = 3.810
```

(The β error grows because Q2's base current grows with it: N/(1 + (N+1)/β).) On chips, area ratios are made by placing N identical transistors in parallel, which matches far better than drawing one bigger one. One reference can feed many outputs, each a chosen multiple of it: that's how an op-amp biases all its stages from a single resistor.

### The MOSFET mirror

The same idea with MOSFETs: the diode-connected M1 (gate tied to drain) settles at the V_GS that carries I_REF, and M2 with the same V_GS copies it:

```
I_REF = (V_DD − V_GS) / R_REF,     with I_REF = (k/2)(V_GS − V_th)²
```

With V_DD = 5 V, R_REF = 10 kΩ, V_th = 0.7 V and k = 2 mA/V², solving both equations together (V_GS ≈ 1.31 V) gives the simulator's **I_REF = 369.24 µA**. And MOSFETs have no gate current, so there is no β error: with λ = 0, I_OUT = 369.24 µA for every load.

With λ = 0.05 V⁻¹ (a realistic short-channel value), the copy depends on V_DS:

```
lambda 0.05 (I_REF 370.97 uA)   R_L 100: 434.85 uA   R_L 2000: 420.94 uA   R_L 5000: 400.70 uA
```

Each transistor's current is multiplied by (1 + λ V_DS). M1 sits at V_DS = V_GS ≈ 1.3 V, while M2 sits at 4.96 V with a 100 Ω load, so M2 carries (1 + 0.05 × 4.96)/(1 + 0.05 × 1.31) ≈ 1.17 times more. As the load grows and M2's V_DS falls toward M1's, the copy improves. This finite output resistance is what cascode mirrors are designed to fix.

## Build It

### Step 1: The BJT mirror

```python
def bjt_mirror(reference_ohms, load_ohms, beta=100.0, output_area=1.0, supply=SUPPLY):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", supply)
    circuit.resistor("RREF", "vcc", "x", reference_ohms)
    circuit.npn("Q1", c="x", b="x", e="0", beta=beta)
    circuit.npn("Q2", c="out", b="x", e="0", beta=beta, Is=1e-14 * output_area)
    circuit.resistor("RL", "vcc", "out", load_ohms)
    return circuit.dc()
```

Q1's collector and base are both node `x`: that is the diode connection. Q2 shares `x` as its base. `Is=1e-14 * output_area` models an N-times-larger transistor.

### Step 2: The experiments

`show_basic`, `show_load_independence`, `show_beta_effect`, `show_ratio` and `show_supply_change` each change one thing and print the result.

### Step 3: The MOSFET mirror

```python
circuit.nmos("M1", d="x", g="x", s="0", vth=0.7, k=2e-3, lam=lam)
circuit.nmos("M2", d="out", g="x", s="0", vth=0.7, k=2e-3, lam=lam)
```

`lam` is λ, the channel-length modulation parameter.

```
uv run python phases/12-transistors/08-current-mirrors/code/main.py
```

## Use It

- **Inside every op-amp**: the classic 741 and the LM358 bias all their stages with mirrors, and use a mirror as the "active load" of the input stage, which gives a gain of thousands from one stage.
- **Matched pairs**: for discrete mirrors use a dual transistor such as the BCM847 or DMMT3904 (two transistors on one die, matched V_BE within a few millivolts and at the same temperature). Two separate 2N3904s whose temperatures differ by just 1 °C mismatch by about 2 mV in V_BE, which is about 8 % in current (2 mV / 25.85 mV = 0.077, and e^0.077 = 1.08).
- **LED drivers**: multi-channel constant-current LED drivers mirror one reference into many outputs so that every LED string gets the same current.
- **Ramp and timing circuits**: charging a capacitor with a mirror current gives a linear ramp (V = I t / C), used in oscillators and PWM generators (Phase 18).
- **Digital-to-analogue converters**: binary-weighted mirrors (×1, ×2, ×4, ×8) summed into a resistor make a current-steering DAC (Phase 17).

## Try It in the Lab

Two matched NPNs on 5 V: Q1 diode-connected, Q2 feeding a 2.2 kΩ sensor. You choose the reference resistor. Goals: the sensor current between 0.85 and 1.1 mA, and Q2 still out of saturation.

Think about: Q1's V_BE, the reference current that results, the 2 % β loss, and the compliance limit. Why does the smallest resistor fail *both* goals, not just the current one?

## Common Mistakes

- **Using unmatched transistors.** A mirror depends on equal I_S and equal temperature. 18 mV of V_BE mismatch is a factor of 2 in current.
- **Forgetting compliance.** A mirror is a current source only while the output transistor stays active.
- **Ignoring the base current error.** At low β or with many outputs on one reference, the base currents add up.
- **Expecting supply independence.** The mirror only copies; I_REF still depends on V_CC through R_REF.
- **Thinking the copy is exact in real parts.** The Early effect / λ makes the output depend on its voltage; use cascode or Wilson mirrors for precision.
- **Swapping roles.** The diode-connected transistor is the input side; the output is the transistor whose collector goes to the load.

## Exercises

1. Design a BJT mirror on 12 V for an output of 2 mA (β = 100). What R_REF? What is the largest load resistance it can drive?
2. With β = 50 and four output transistors all mirroring one Q1 (each the same size), what is each output's current relative to I_REF? (Hint: count base currents.)
3. Two discrete transistors at 25 °C and 30 °C share the same V_BE. Using −2 mV/°C for V_BE at fixed current and 60 mV per decade, estimate the current ratio.
4. A MOSFET mirror has λ = 0.02 V⁻¹. The input transistor sits at V_DS = 1.2 V and the output at 6 V. By what percentage does the output exceed the reference?
5. In the script, add a third NPN "Q3" (base to `x`, emitter to ground) with its own 1 kΩ load. Check that it also copies I_REF, and see how the β error changes.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Current mirror | "Mirror" | Diode-connected input transistor whose V_BE (or V_GS) drives matched output transistors |
| Diode-connected | "Transistor as a diode" | Base tied to collector (gate to drain); sets the V_BE for a given current |
| I_REF | "Reference current" | Current forced into the input side, usually (V_CC − V_BE)/R_REF |
| β error | "Base current error" | I_OUT/I_REF = β/(β+2) for the basic BJT mirror |
| Compliance | "Headroom" | Output voltage range over which the output transistor stays active |
| Output resistance | "r_out" | ΔV_out/ΔI_out; ≈ r_o = V_A / I for a basic mirror |
| Area ratio | "Scaled mirror" | Output transistor N times larger (or N in parallel) gives N × I_REF |
| Active load | "Mirror load" | A mirror used instead of a resistor to give an amplifier stage very high gain |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 2.3.7 "Current mirrors" and 3.2.2 (JFET current sources).
- *All About Circuits*, Volume III, chapter 4, "Current mirrors". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/current-mirrors/
- P. Gray, P. Hurst, S. Lewis and R. Meyer, *Analysis and Design of Analog Integrated Circuits*, chapter 4 "Current mirrors, active loads and references".
- Nexperia BCM847 matched dual transistor datasheet: V_BE matching and thermal coupling. https://www.nexperia.com/
