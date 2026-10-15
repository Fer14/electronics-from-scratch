# Finite State Machines

> Any circuit that reacts to a sequence of events can be drawn as circles and arrows, then turned mechanically into flip-flops and gates.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lessons 03 and 06 (Boolean Algebra, Combinational Circuits), Phase 15 (Sequential Logic), Lessons 03-05 (Flip-Flops and the Clock, Registers, Counters)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Finite state machine (FSM) | A circuit with a limited number of states that moves between them at each clock edge according to its inputs | A board game: your square (state) and the dice (input) decide your next square |
| State | One situation the machine can be in, summarising everything it needs to remember about the past | "I have put in 50 cents so far" in a vending machine |
| Transition | A move from one state to another, labelled with the input that causes it | An arrow on the board game |
| State diagram | Circles (states) joined by arrows (transitions) | A subway map |
| State table | The same information as a table: current state and input give next state and output | The timetable version of the subway map |
| Moore machine | An FSM whose outputs depend only on the current state | A traffic light: the colour depends only on which phase it is in |
| Mealy machine | An FSM whose outputs depend on the current state and the current input | A vending machine that releases a drink the moment the last coin drops |
| State encoding | The bit pattern chosen to represent each state | Giving each subway station a number |
| One-hot encoding | One flip-flop per state, exactly one of them 1 | One light per station on a map, only yours lit |
| Next-state logic | The combinational logic that computes the next state | The rule book of the game |
| Output logic | The combinational logic that computes the outputs | The scoreboard |
| Sequence detector | An FSM that signals when a particular pattern of input bits has arrived | A door lock that opens after the right code is typed |

## Learning Objectives

- Describe a problem as a state diagram and a state table.
- Tell Moore and Mealy machines apart and explain the one-cycle difference in their outputs.
- Choose a state encoding (binary or one-hot) and derive next-state and output equations from the table.
- Build a sequence detector from flip-flops and gates and verify it against a software reference.
- Recognise that counters, registers and processors' control units are all finite state machines.

## The Problem

A counter (Lesson 05) always goes to the same next value. Most real controllers are more interesting: what they do next depends on what has happened before and on what is happening now. A washing machine fills, washes, drains, spins, and moves between those phases on timers and sensors. A traffic light changes colour on a timer, but turns red early if a pedestrian presses the button. A serial receiver must find the start bit, then collect 8 data bits, then check the stop bit. The control unit of a processor (Phase 16, Lesson 05) steps through fetch, decode and execute.

All of these are **finite state machines**. The power of the idea is that there is a recipe: describe the behaviour as states and arrows, write the table, encode the states in bits, and the circuit (flip-flops for the state, gates for the logic) follows mechanically. This lesson follows the recipe from start to finish for a sequence detector, and checks the result against a plain Python search.

## The Physics

Physically, an FSM is the synchronous pattern of Lesson 03: a register (the state) and two blocks of combinational logic (next state and outputs), all on one clock. Nothing new is needed. What matters physically is timing: the next-state logic must settle within one clock period (Lesson 07), and the inputs must be synchronised to the clock, because an input that changes right at a clock edge can drive the state flip-flops into an inconsistent combination (one bit seeing the new input, another the old). That last point is why real designs pass every asynchronous input through a synchroniser first.

## The Concept

### The general structure

```
               +------------------------------+
               |                              |
  inputs ----->|  next-state logic            |
         +---->|  next = f(state, inputs)     |
         |     +---------------+--------------+
         |                     |
         |               +-----v-----+
         |               |  state    |<---- clk
         |               | register  |
         |               +-----+-----+
         |                     |
         +---------------------+ state
                               |
               +---------------v--------------+
  inputs ----->|  output logic                |----> outputs
   (Mealy only)|  out = g(state) or g(state,in)|
               +------------------------------+
```

- In a **Moore** machine, the outputs are a function of the state only: `out = g(state)`. They change only after a clock edge.
- In a **Mealy** machine, the outputs are a function of the state and the current inputs: `out = g(state, inputs)`. They can react within the same cycle as an input change.

The counter of Lesson 05 is a Moore machine with 16 states and one input (`en`), where the output is the state itself.

### Step 1: The specification

**Detect the pattern 1, 0, 1 on a serial input `x`.** One bit arrives per clock cycle. After the cycle in which the third bit of a "101" arrives, the output `z` must be 1 for one cycle. Overlapping patterns count: the stream 1 0 1 0 1 contains two (positions 1-3 and 3-5).

### Step 2: The states

A state must summarise **everything about the past that matters for the future**. For this detector, only one thing matters: how much of "101" we have seen at the end of the stream so far.

```
A : nothing useful (the stream so far does not end in 1 or 10)
B : the stream ends in "1"
C : the stream ends in "10"
D : the stream ends in "101"   -> output z = 1
```

### Step 3: The transitions

For each state and each input value, ask: "what does the stream end in now?"

```
from A:  x=0 -> still nothing           -> A
         x=1 -> ends in "1"              -> B
from B:  x=0 -> ends in "10"             -> C
         x=1 -> ends in "11", i.e. "1"   -> B
from C:  x=0 -> ends in "100": nothing   -> A
         x=1 -> ends in "101"            -> D
from D:  x=0 -> ends in "1010": "10"     -> C    (overlap: the last 1 of 101 starts a new pattern)
         x=1 -> ends in "1011": "1"      -> B
```

As a state diagram, the forward arrows form a chain, and the other arrows point back:

```
            x=0           x=1
           +---+         +---+
           |   |         |   |
           v   |         v   |
 reset --> [ A ] --x=1--> [ B ] --x=0--> [ C ] --x=1--> [ D ]
           z=0           z=0           z=0           z=1

 backward arrows:   C --x=0--> A      D --x=0--> C      D --x=1--> B
```

(The machine starts in A after reset.) Because `z` is written inside the circles, this is a **Moore** machine: the output belongs to the state.

### Step 4: The encoding and the state table

Four states need 2 flip-flops, `s1 s0`. Choose a binary encoding: A = 00, B = 01, C = 10, D = 11. Now the diagram becomes a truth table with inputs `s1, s0, x` and outputs `s1+, s0+`:

```
 s1 s0 x | s1+ s0+    from -> to
  0  0 0 |  0   0     A -> A
  0  0 1 |  0   1     A -> B
  0  1 0 |  1   0     B -> C
  0  1 1 |  0   1     B -> B
  1  0 0 |  0   0     C -> A
  1  0 1 |  1   1     C -> D
  1  1 0 |  1   0     D -> C
  1  1 1 |  0   1     D -> B
```

### Step 5: Next-state and output equations

Look at the `s0+` column: 0 1 0 1 0 1 0 1. It equals `x` in every row. (With this encoding, `s0` means "the last bit was 1", which is just `x` delayed by one clock.) So the flip-flop for `s0` takes `x` directly: no gates at all.

The `s1+` column is 1 on rows `010`, `101` and `110`. Use a Karnaugh map (Phase 14, Lesson 03) with `s1` on the rows and `s0 x` on the columns:

```
            s0 x
          00   01   11   10
        +----+----+----+----+
 s1 = 0 |  0 |  0 |  0 |  1 |
        +----+----+----+----+
 s1 = 1 |  0 |  1 |  0 |  1 |
        +----+----+----+----+
```

- The column `s0 x = 10` has 1s in both rows: the group `s0·x'`.
- The single cell `s1 = 1, s0 x = 01` cannot join anything: the term `s1·s0'·x`.

```
s1+ = s0·x' + s1·s0'·x
```

Read it in words: "we will be in C or D next (s1 = 1) if the last bit was 1 and this one is 0 (we have '10'), or if we were in C ('10') and this bit is 1 (we have '101')". The output is 1 only in D:

```
z = s1·s0
```

Total: 2 flip-flops, 2 inverters, 3 AND gates (one for `z`) and 1 OR gate.

### Step 6: Verify

Run the gates on a stream and compare with a direct software search for "101" ending at each position:

```
  x     : 1 1 0 1 0 1 1 0 1 0 0 1 0 1
  state : B B C D C D B C D C A B C D
  z     : 0 0 0 1 0 1 0 0 1 0 0 0 0 1
  string search says: 0 0 0 1 0 1 0 0 1 0 0 0 0 1
```

Four occurrences, including the overlapping pair `1 0 1 0 1` at positions 3-7. The state row reads like a story: each letter is how much of the pattern the machine has seen.

### Moore versus Mealy

A Mealy version of the same detector needs only three states (A, B, C): instead of a state D whose meaning is "just saw 101", it raises `z` **on the arrow** from C with `x = 1`:

```
z = (state is C) · x
```

Its output appears in the **same** cycle as the last 1 arrives, one cycle earlier than the Moore output, and it uses one state less. The price: the output now depends directly on the input, so it can glitch when `x` glitches, and a combinational path runs from the input straight to the output, which matters for timing when FSMs are chained. Many designers prefer Moore machines (or register the Mealy outputs) for that reason.

### Choosing an encoding

The encoding changes the logic, not the behaviour. Two common choices:

- **Binary** (A = 00, B = 01, ...): fewest flip-flops, `ceil(log2(N))` for N states. Logic can be complex.
- **One-hot**: one flip-flop per state, exactly one of them 1 (A = 0001, B = 0010, C = 0100, D = 1000). More flip-flops, but the next-state logic is trivial to write: each state's flip-flop is the OR of all arrows pointing into it. For the detector:

```
A+ = A·x' + C·x'
B+ = A·x + B·x + D·x
C+ = B·x' + D·x'
D+ = C·x
z  = D
```

FPGAs have plenty of flip-flops (one per LUT, Phase 14, Lesson 08), so synthesis tools often choose one-hot for them. Gray codes (neighbouring states differ by one bit) are a third option, useful when state bits are read by another clock domain.

### Always have a reset, and handle unused states

With 2 flip-flops for 4 states, every pattern is a valid state. But a 5-state machine needs 3 flip-flops, leaving 3 unused patterns. A glitch or a power-up could land the machine in one of them. Good practice: make sure every unused state leads back to a valid one (often the reset state), and give the machine a reset input that puts it in its starting state.

## Build It

The script `code/main.py` writes the state machine as a Python dictionary, derives the table from it, builds the gates in `sim.logic`, and checks the gates against both the table and a string search.

### Step 1: The machine as data

```python
STATES = {"A": (0, 0), "B": (0, 1), "C": (1, 0), "D": (1, 1)}
NAMES = {code: name for name, code in STATES.items()}
TRANSITIONS = {
    ("A", 0): "A", ("A", 1): "B",
    ("B", 0): "C", ("B", 1): "B",
    ("C", 0): "A", ("C", 1): "D",
    ("D", 0): "C", ("D", 1): "B",
}
```

This dictionary is the state diagram: `(state, input) -> next state`.

### Step 2: The state table

```python
def table_from_transitions():
    rows = []
    for (s1, s0), x in product(STATES.values(), (0, 1)):
        nxt = STATES[TRANSITIONS[(NAMES[(s1, s0)], x)]]
        rows.append((s1, s0, x, nxt[0], nxt[1]))
    return rows
```

### Step 3: The circuit

```python
def detector():
    lc = LogicCircuit("Moore detector for 101")
    lc.inputs("x")
    lc.not_("nx", "x")
    lc.not_("ns0", "s0")
    lc.and_("p", "s0", "nx")
    lc.and_("r", "s1", "ns0", "x")
    lc.or_("n1", "p", "r")
    lc.dff("x", "s0", name="S0")
    lc.dff("n1", "s1", name="S1")
    lc.and_("z", "s1", "s0")
    lc.outputs("s1", "s0", "z")
    return lc
```

### Step 4: Check the logic against the table

`settle` can force the flip-flop outputs `s1, s0` to any state, together with an input value, and then report what the next-state wires compute. Doing this for all 8 rows checks the gates without running any clock:

```python
for s1, s0, x, n1, n0 in table_from_transitions():
    values = lc.settle({"s1": s1, "s0": s0, "x": x})
    wrong += values["n1"] != n1 or x != n0
```

### Step 5: Run a stream and compare

```python
def reference(bits):
    return [int(k >= 2 and bits[k - 2:k + 1] == [1, 0, 1]) for k in range(len(bits))]
```

The reference looks at the last three bits at every position. The script resets the machine, applies one input bit per `step`, and compares `z` with the reference: `match: True`.

Run it:

```bash
uv run python phases/15-sequential-logic/06-finite-state-machines/code/main.py
```

## Use It

- **Protocol receivers.** A UART receiver is an FSM: idle, start bit, data bits 0-7, stop bit (Phase 17, Lesson 06). USB, Ethernet and I2C controllers are larger FSMs.
- **Control units.** The control unit of the computer in Phase 16, Lesson 05 is an FSM that steps through fetch, decode and execute, with outputs that drive every register's load enable.
- **Debouncers and edge detectors.** A button input goes through a tiny FSM that waits for the signal to be stable for several milliseconds before reporting a press.
- **Traffic lights, elevators, vending machines, washing machines**: classic FSM examples, and in real products they are FSMs in a microcontroller's software or in a small programmable chip.
- **Hardware description languages.** In Verilog or VHDL, FSMs are written as a `case` statement on the state; synthesis tools choose the encoding and derive the logic, exactly the steps of this lesson.

## Try It in the Lab

The lab task "Next-state logic of a 101 detector" has the whole machine wired except the logic for `s1+`. The inverters `nx = x'` and `ns0 = s0'`, the product `u = s1·s0'`, both flip-flops and the output `z = s1·s0` are fixed. Fill three slots: one combining `s0` with `nx`, one combining `u` with `x`, and the one that combines both into `n1`, the input of the `s1` flip-flop. Parts: AND, OR, NOR. The checker feeds a 14-bit stream and compares `z` after every clock edge with the correct detections.

Think about: `s1+ = s0·x' + s1·s0'·x` is a sum of products. Which gate makes a product, and which makes a sum?

## Common Mistakes

- **Forgetting overlap.** After detecting 101, the last 1 may start the next pattern. From D, input 0 goes to C, not A.
- **States that remember too little.** If two different histories lead to the same state but need different futures, the machine is wrong. Test with tricky streams like 1 1 0 1 and 1 0 0 1.
- **Mixing Moore and Mealy timing.** A Moore output appears one cycle after the input that completes the pattern; a Mealy output appears in the same cycle. Check which one the specification asks for.
- **No reset.** Without a reset, the machine starts in a random state and may report a detection that never happened.
- **Unsynchronised inputs.** An input that changes at the clock edge can send some state bits to the new state and others to the old, landing in a state that has no arrow for it. Synchronise inputs first (Lesson 07).

## Exercises

1. Draw the state diagram of a Moore detector for the pattern 1, 1 (two 1s in a row), with overlap. How many states does it need? Write its state table with a binary encoding.
2. Draw the Mealy version of the 101 detector with three states. Write its state table, including the output column, and derive the equations.
3. A traffic light cycles green (4 clock ticks), yellow (1 tick), red (3 ticks). Model it as an FSM with a counter, or as an FSM with one state per tick. How many states does the second version need? Which version needs fewer flip-flops?
4. Rewrite the 101 detector with the encoding A = 00, B = 01, C = 11, D = 10. Derive `s1+`, `s0+` and `z`. Is the logic simpler or more complex than in this lesson?
5. In the script, change `TRANSITIONS` to detect 110 instead, update the circuit with your own equations, and check it against a modified `reference`. (Hint: after detecting 110, the next input starts from scratch.)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Finite state machine | "FSM", "state machine" | A state register plus next-state and output logic, stepping on each clock edge |
| State diagram | "Bubbles and arrows" | States as circles, transitions as arrows labelled with the inputs that cause them |
| State table | "The transition table" | Current state and input listed against next state and output; a truth table for the logic |
| Moore machine | "Outputs on states" | Outputs depend only on the state; they change only after clock edges |
| Mealy machine | "Outputs on arrows" | Outputs depend on state and inputs; faster by one cycle, but can glitch with the inputs |
| State encoding | "State assignment" | The bit patterns given to the states: binary, one-hot, Gray |
| One-hot | "One flip-flop per state" | Exactly one state bit is 1; next-state logic is the OR of incoming arrows |
| Sequence detector | "Pattern matcher" | An FSM whose output marks the arrival of a given bit pattern |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 3, section on finite state machines (design examples, Moore and Mealy, state encodings).
- M. Morris Mano and Michael D. Ciletti, *Digital Design*, Chapter 5, sections on state diagrams, state reduction and assignment, and design procedure.
- John F. Wakerly, *Digital Design: Principles and Practices*, chapters on state machine design.
- Edward F. Moore, "Gedanken-experiments on Sequential Machines" (1956), and George H. Mealy, "A Method for Synthesizing Sequential Circuits" (1955), the two papers the machine types are named after.
