# Kirchhoff's Current Law

> Charge cannot pile up in a wire, so whatever flows into a node must flow out of it. Every circuit solver on Earth starts from this one sentence.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), especially Lesson 08 (Current as Moving Charge); Phase 03 (Resistance and Ohm's Law), especially Lesson 03 (Ohm's Law); Phase 04 Lesson 01 (Nodes, Branches and Loops)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Kirchhoff's current law (KCL) | At any node, the total current flowing in equals the total current flowing out | At a road junction, the cars per minute arriving equal the cars per minute leaving, because none park there |
| Conservation of charge | Electric charge is never created or destroyed, only moved | Money moved between bank accounts: the total never changes |
| Junction | A node where three or more branches meet; the interesting kind of node | A crossroads, as opposed to a bend in a road |
| Reference direction | An arrow you draw on a branch to say "I will call current positive if it flows this way" | Deciding that "north" is positive before you measure how fast a car is going |
| Negative current | A current that turned out to flow against the arrow you drew | Driving at -30 km/h north: you are really going 30 km/h south |
| Unknown node voltage | The voltage at a node that you do not know yet and want to find | The water level in a tank you cannot see into |
| Bisection | Finding an answer by guessing, checking whether you are too high or too low, and halving the range each time | The "guess my number between 1 and 100" game |
| Incidence matrix | A table with one row per node and one column per branch saying which branch leaves or enters which node | A spreadsheet of which roads leave which towns |

## Learning Objectives

- State Kirchhoff's current law in words and as an equation, and explain why it follows from conservation of charge.
- Use reference arrows and signs consistently, and interpret a negative answer.
- Find an unknown current at a junction from the others.
- Combine KCL with Ohm's law to find an unknown node voltage, both by guessing and by algebra.
- Check that a solved circuit satisfies KCL at every node.

## The Problem

You have a 9 V battery feeding a node. From that node, two resistors go back to the battery. You know the battery delivers 15 mA, and you measure 8 mA in one of the resistors. What is in the other? Your intuition probably says 7 mA. It is right, and the rule behind that intuition is Kirchhoff's current law.

It sounds too obvious to be a "law". But it is the single most-used equation in electronics. In Lesson 01 you learned to count nodes. Kirchhoff's current law gives you one equation per node. Together with Ohm's law (one relation per resistor) it is enough to solve circuits that series-and-parallel tricks cannot touch. In Phase 05 you will write a simulator that is nothing more than KCL written at every node, solved by a computer.

And there is a practical side. When a fuse blows or a wire gets hot, someone has to figure out where the current went. "Current in = current out" lets you trace it, node by node, with a multimeter.

## The Physics

Recall from Phase 01 (Lesson 08) that current is moving charge: one ampere (A) means one coulomb (C) of charge passing a point every second. Written as a sentence: current equals charge moved divided by time taken.

```
I = Q / t        I in amperes, Q in coulombs, t in seconds
```

Now look at one node, say a junction of three wires. Suppose 5 mA (5 thousandths of an ampere) flows in through one wire and only 3 mA flows out through the other two. Every second, 0.005 C arrives and 0.003 C leaves. So 0.002 C of extra charge would collect at the junction every second.

What happens to a place where charge collects? From Phase 01 (Lesson 04 and Lesson 06) you know that like charges repel and that piling charge on an object raises its voltage. How much voltage per coulomb depends on how much charge the object can "hold" for each volt, a quantity called capacitance (you will study it in Phase 07). For now the only fact you need: a little blob of metal like a circuit node can hold about 10 picofarads, meaning it only takes 10 × 10⁻¹² coulombs to raise its voltage by 1 V. That is a tiny amount of charge.

So imagine a mismatch of just 1 mA flowing into such a node:

```
after 1 nanosecond:   charge = 0.001 A × 1e-9 s = 1e-12 C  → voltage up by 1e-12 / 10e-12 = 0.1 V
after 1 microsecond:  charge = 1e-9 C                        → voltage up by 100 V
after 1 millisecond:  charge = 1e-6 C                        → voltage up by 100 000 V
```

That never happens, and the reason is a feedback loop. As soon as the node's voltage starts to rise, the current flowing in (from the higher-voltage side) gets smaller, and the currents flowing out (towards lower voltages) get bigger, both by Ohm's law. The voltage settles, within nanoseconds, at the exact value where in and out balance. After that, nothing piles up.

So in a circuit that has settled down (engineers say **steady state**, or **DC** when nothing changes in time), the current arriving at any node exactly equals the current leaving. That is Kirchhoff's current law. Gustav Kirchhoff wrote it down in 1845, when he was a student.

What the "cars at a junction" analogy gets right: none are created, none vanish, so in equals out. What it gets wrong: cars can park and a car park can fill up, but a wire junction cannot store any noticeable charge. Later (Phase 07) you will meet the capacitor, a part *designed* to store charge, and there the current in and out of each of its plates differ for a while. Even then, KCL still holds at every node if you include the capacitor's current as one of the branch currents.

## The Concept

### The law in words and symbols

In words: **the sum of the currents flowing into a node equals the sum of the currents flowing out of it.**

As an equation, for currents I₁, I₂, ... arriving and I₃, I₄, ... leaving:

```
I1 + I2 + ... = I3 + I4 + ...        (in = out)
```

Many books write the same thing another way. Count every current *leaving* the node as positive and every current *arriving* as negative. Then the total is zero:

```
sum of currents leaving the node = 0        (signed sum)
```

Read it out loud: "add up all the currents leaving the node, with arriving ones counted as negative, and you get zero". Both forms say the same thing. The signed form is the one computers use.

### Worked example: one unknown wire

A junction has five wires. You measured four of them:

```
            wire 1: 120 mA in
                 |
 wire 2: 45 mA ──●── wire 3: 80 mA out
     in          |
            wire 4: 30 mA out
                 |
            wire 5: ?
```

In = 120 + 45 = 165 mA. Out (so far) = 80 + 30 = 110 mA. The missing 165 - 110 = **55 mA** must leave through wire 5.

Check with the signed form, counting leaving as positive: -120 - 45 + 80 + 30 + 55 = 0. Yes.

### Reference directions and negative answers

Often you do not know which way a current flows before you solve the circuit. That is fine. You draw an arrow on each branch, any way you like, and call it the **reference direction**. Write KCL using those arrows. If a current comes out negative, it simply flows opposite to the arrow.

Example: suppose in the junction above you had drawn wire 5's arrow pointing *in*. Then KCL says in = out:

```
120 + 45 + I5 = 80 + 30   →   I5 = 110 - 165 = -55 mA
```

The minus sign tells you: 55 mA, flowing against your arrow, so out of the junction. Same physical answer. Never "fix" a minus sign by quietly flipping it; keep it and read it.

### KCL plus Ohm's law: finding a voltage

KCL alone counts currents. To get voltages you combine it with Ohm's law from Phase 03: the current through a resistor equals the voltage across it divided by its resistance, I = V / R. Here is the circuit used in the code:

```
   vcc ──[ R1 = 1 kΩ ]── a ──┬──────────┐
    |                        |          |
  [B1 9 V]               [R2 2 kΩ]  [R3 6 kΩ]
    |                        |          |
   gnd ──────────────────────┴──────────┘
```

(kΩ means kilo-ohms, thousands of ohms.) Ground is the battery's minus side, so v(gnd) = 0 V and v(vcc) = 9 V. The unknown is the voltage at node a, call it v(a).

Write each current through each resistor using Ohm's law, with the voltage across it being the difference of its two node voltages:

```
current arriving through R1  = (9 - v(a)) / 1000
current leaving through R2   = (v(a) - 0) / 2000
current leaving through R3   = (v(a) - 0) / 6000
```

KCL at node a, in = out:

```
(9 - v(a)) / 1000 = v(a) / 2000 + v(a) / 6000
```

### Solving it by guessing (bisection)

Before algebra, let us do it the way an engineer with only a calculator might. Guess v(a), compute "in minus out", and see which way you are off.

```
guess v(a) = 3 V:  in = 6/1000 = 6.000 mA,  out = 1.5 + 0.5 = 2.000 mA,  in - out = +4.000 mA
guess v(a) = 8 V:  in = 1/1000 = 1.000 mA,  out = 4 + 1.333 = 5.333 mA,  in - out = -4.333 mA
```

At 3 V more comes in than goes out: charge would pile up and push the voltage up, so the true answer is higher. At 8 V more goes out: the true answer is lower. The answer is between 3 V and 8 V. Try the middle, 5.5 V:

```
guess v(a) = 5.5 V: in = 3.5 mA, out = 2.75 + 0.917 = 3.667 mA, in - out = -0.167 mA → too high
```

So it is between 3 and 5.5. Keep halving. This is **bisection**, and notice it mirrors the physics: the circuit itself "searches" for the voltage where KCL holds. After 40 halvings the program lands on 5.400000 V.

### Solving it by algebra

Multiply both sides by 6000 to clear the fractions:

```
6 × (9 - v(a)) = 3 × v(a) + 1 × v(a)
54 - 6 v(a) = 4 v(a)
54 = 10 v(a)
v(a) = 5.4 V
```

Now every current follows from Ohm's law:

```
I(R1) = (9 - 5.4) / 1000 = 3.6 mA   (vcc to a)
I(R2) = 5.4 / 2000      = 2.7 mA   (a to gnd)
I(R3) = 5.4 / 6000      = 0.9 mA   (a to gnd)
```

Check KCL at node a: 3.6 = 2.7 + 0.9. Yes. At gnd: 2.7 + 0.9 = 3.6 mA arrive from R2 and R3, and 3.6 mA leave through the battery back up to vcc. At vcc: 3.6 mA arrive from the battery, 3.6 mA leave through R1. Every node balances.

Notice the bigger resistor (6 kΩ) takes the smaller current, three times smaller, because it is three times bigger and has the same 5.4 V across it. You will turn that into a rule in Lesson 06 (The Current Divider).

### How many KCL equations are useful?

A circuit with N nodes gives N KCL equations, but only N - 1 of them are independent. In our example, if vcc and a balance, gnd must balance too: every branch current leaves one node and enters another, so adding up all N equations gives 0 = 0. One equation is always redundant. That is why, in Phase 05, nodal analysis writes KCL at every node *except ground*.

### The incidence matrix

There is a tidy way to write "every current leaving minus entering" for all nodes at once. Make a table with one row per node and one column per branch. Put +1 where the branch's arrow leaves the node, -1 where it enters, and 0 otherwise:

```
          R1    R2    R3    B1
  vcc     +1     0     0    -1
    a     -1    +1    +1     0
  gnd      0    -1    -1    +1
```

(The battery's arrow points from gnd up through it to vcc, the way its current flows.) Multiply this table by the list of branch currents (3.6, 2.7, 0.9, 3.6 mA) row by row, and each row gives the signed KCL sum for one node. All three are zero. Notice every column has exactly one +1 and one -1: every branch leaves one node and enters another. That is the whole reason one equation is redundant, since adding the rows gives all zeros.

## Build It

Run the program:

```
uv run python phases/04-kirchhoffs-laws/02-kirchhoffs-current-law/code/main.py
```

### Step 1: The junction with an unknown wire

```python
known = {"wire 1 (in)": 0.120, "wire 2 (in)": 0.045, "wire 3 (out)": -0.080, "wire 4 (out)": -0.030}
arriving = sum(amps for amps in known.values() if amps > 0)
leaving = -sum(amps for amps in known.values() if amps < 0)
unknown = arriving - leaving
```

Arriving currents are stored as positive and leaving ones as negative. The program prints that wire 5 carries 55 mA out.

### Step 2: What a broken KCL would mean

```python
mismatch = 0.001
node_capacitance = 10e-12
for t in seconds:
    piled_charge = mismatch * t
    voltage = piled_charge / node_capacitance
```

Charge is current times time, and the voltage rise is that charge divided by the node's tiny capacitance. The output (0.1 V after a nanosecond, 100 000 V after a millisecond) shows why the node voltage must settle where in = out.

### Step 3: Find v(a) by bisection and by algebra

```python
def imbalance_at_a(v_a):
    arriving = (supply - v_a) / r_feed
    leaving = v_a / r_left + v_a / r_right
    return arriving - leaving


low, high = 0.0, supply
for step in range(40):
    middle = (low + high) / 2
    if imbalance_at_a(middle) > 0:
        low = middle
    else:
        high = middle
```

If the imbalance is positive (more in than out), the true voltage is higher, so we raise the lower bound. Otherwise we lower the upper bound. Forty halvings shrink a 9 V range to about 9 / 2⁴⁰, far smaller than any voltmeter can see.

The algebraic answer is the same equation rearranged: move all v(a) terms to one side.

```python
v_a_algebra = (supply / r_feed) / (1 / r_feed + 1 / r_left + 1 / r_right)
```

Check it by hand: 0.009 / (0.001 + 0.0005 + 0.0001667) = 0.009 / 0.0016667 = 5.4 V.

### Step 4: Check KCL everywhere

```python
def leaving_current_at(node, branches, branch_currents):
    total = 0.0
    for (name, node_from, node_to, _), current in zip(branches, branch_currents):
        if node_from == node:
            total += current
        if node_to == node:
            total -= current
    return total
```

Each branch has a reference direction from `node_from` to `node_to`. Its current counts as leaving `node_from` and arriving at `node_to`. The program prints a signed sum of zero for vcc, a and gnd.

### Step 5: The incidence matrix

```python
incidence = np.zeros((len(nodes), len(branches)))
for column, (name, node_from, node_to, _) in enumerate(branches):
    incidence[nodes.index(node_from), column] = 1
    incidence[nodes.index(node_to), column] = -1
```

`incidence @ currents` performs every node's signed sum in one multiplication and prints `[0. 0. 0.]`. Phase 05 builds the whole simulator out of this matrix.

## Use It

- **Tracing a fault.** An electrician measuring 16 A on the main wire of a circuit, and 10 A and 2 A on the two known loads, knows 4 A is going somewhere else. KCL tells them to look for a third branch: a forgotten heater, or a fault to earth.
- **Residual current devices (RCDs, also called GFCIs in North America)** in your home's fuse box are KCL in hardware. They compare the current going out on the live wire with the current returning on the neutral. If they differ by more than about 30 mA, some current is leaking through another path (possibly a person) and the device trips in a few tens of milliseconds.
- **Current-sense resistors.** Boards often put a small resistor (for example 0.1 Ω) in the main supply line and measure the voltage across it. By KCL, that current equals the sum of everything the board draws. Battery "fuel gauge" chips like the Texas Instruments BQ27441 do exactly this.
- **USB power budgets.** A USB 2.0 port supplies up to 500 mA. If a hub feeds four devices, KCL says the sum of their currents must stay under that, or the port's protection shuts it down.

## Try It in the Lab

Open the lab task for this lesson. A 9 V battery pushes current through a 100 Ω sense resistor R0 into node a. A 1 kΩ resistor R1 already goes from a to ground. Your job is to drop one resistor into the empty slot, also from a to ground, so that the current through R0 is between 14 and 16 mA, without your resistor dissipating more than 1/4 W.

Things to think about: how much current flows with no second branch at all? Since the sense resistor drops some voltage, node a is not at 9 V; roughly where is it once 15 mA flows? KCL at node a tells you how much your branch must carry. Does a bigger resistor in the slot increase or decrease the total current?

## Common Mistakes

- **Mixing up signs.** Choose one convention per equation (in = out, or signed sum with leaving positive) and stick to it. Most errors come from switching halfway through.
- **"Fixing" a negative answer.** A negative current is information: the real flow is opposite your arrow. Do not drop the minus sign, and do not redraw the arrow and recompute; just read it.
- **Thinking current gets "used up" in a resistor.** The same current that enters a resistor leaves it. What a resistor uses up is energy (voltage drops across it), not charge. KCL applied to a node inside a series chain shows this: one wire in, one wire out, so the currents are equal.
- **Writing KCL at every node and expecting N independent equations.** One is always redundant. If you try to solve with all N you will find the system has no unique answer.
- **Applying KCL while things are changing fast.** KCL holds at every instant for nodes made of wire. But if you draw your "node" boundary around a capacitor plate, charge does build up inside it. Keep nodes as pure wire junctions and KCL always holds.

## Exercises

1. Four wires meet at a node. Wire A brings 2.5 A in, wire B takes 1.2 A out, wire C takes 0.4 A out. What does wire D carry, and in which direction?
2. You draw all three arrows at a three-wire junction pointing *into* the node. Two of the currents are measured as +40 mA and +25 mA. What is the third, with sign? Explain what the sign means.
3. In the circuit of this lesson (9 V, R1 = 1 kΩ, R2 = 2 kΩ, R3 = 6 kΩ), change R3 to 2 kΩ. Find v(a) with the KCL equation by hand, then all three currents. Check your answer by editing `r_right` in `code/main.py`.
4. A 12 V battery feeds node a through R1 = 200 Ω. From a, R2 = 300 Ω goes to ground, and a small gadget that always draws exactly 20 mA (whatever its voltage) also goes from a to ground. Write KCL at a and solve for v(a).
5. (Harder) Add a second unknown node: 9 V battery, R1 = 1 kΩ from vcc to a, R2 = 1 kΩ from a to gnd, R3 = 1 kΩ from a to b, R4 = 1 kΩ from b to gnd. Write KCL at a and at b (two equations, two unknowns). Solve by substitution, then check that the battery current equals the sum of the currents in R2 and R4 arriving at ground.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| KCL | "Current splits at junctions" | At every node, the sum of currents in equals the sum out; it follows from charge being conserved and not piling up |
| Reference direction | "The direction current flows" | The direction you *chose* to call positive before solving; the real flow may turn out opposite |
| Negative current | "An error" | Current flowing against your chosen arrow, a perfectly valid answer |
| Node voltage | "The voltage of a point" | The voltage difference between that node and the ground node |
| Steady state (DC) | "When it is switched on" | When nothing in the circuit changes any more in time, after any start-up effects have died away |
| Incidence matrix | "A complicated matrix" | A node-by-branch table of +1, -1 and 0 that turns all KCL equations into one multiplication |

## Further Reading

- *All About Circuits*, Volume I (DC), chapter "Divider Circuits and Kirchhoff's Laws": short, clear, with many worked examples.
- Khan Academy, Electrical Engineering, "Kirchhoff's current law" video and article: a gentle visual introduction.
- MIT OpenCourseWare 6.002 *Circuits and Electronics*, lectures 1 and 2: shows how KCL comes from Maxwell's equations under the "lumped" assumption.
- Richard Feynman, *The Feynman Lectures on Physics*, Vol. II, chapter 13 ("Magnetostatics"), section on conservation of charge and current: the physics behind "charge cannot pile up".
