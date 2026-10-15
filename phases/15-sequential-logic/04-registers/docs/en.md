# Registers

> A register is a row of flip-flops sharing one clock, with a small multiplexer in front of each one that decides whether to keep the old value or take a new one.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 08 (Multiplexers and Decoders), Phase 15 (Sequential Logic), Lesson 03 (Flip-Flops and the Clock)
**Time:** ~65 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Register | A group of flip-flops that store one multi-bit value together | A row of pigeonholes holding one word, one letter per hole |
| Word | The multi-bit value a register holds (4, 8, 32, 64 bits) | A whole number written on a row of digit cards |
| Load enable | An input that decides whether the register takes new data at the next clock edge | A "write" button on a notepad |
| Hold | Keeping the old value at a clock edge | Not pressing the button |
| Parallel | All bits moved at once, one wire per bit | A row of people stepping forward together |
| Serial | Bits moved one after another on a single wire | People going through a turnstile one at a time |
| Shift register | A chain of flip-flops where each one takes its neighbour's value at every edge | A bucket brigade: every tick, each bucket moves one person down the line |
| Serial in, parallel out (SIPO) | Bits enter one at a time and are read all together | Filling an egg box one egg at a time, then lifting the whole box |
| Parallel in, serial out (PISO) | A word is loaded at once and sent out bit by bit | Emptying the egg box one egg at a time |
| Register file | A set of numbered registers with a way to choose which one is read or written | A wall of numbered lockers |
| Clock gating | Stopping the clock to a register to save power, instead of using an enable | Turning off the conveyor belt instead of ignoring what arrives |

## Learning Objectives

- Build an n-bit register from D flip-flops sharing a clock.
- Add a load enable with a 2-to-1 multiplexer in front of each flip-flop: `d = load·din + load'·q`.
- Explain why the enable is a mux and not a gate on the clock.
- Build a shift register and use it to convert serial data to parallel and back.
- Explain how a register file chooses which register to read and to write, using muxes and a decoder.

## The Problem

A single flip-flop stores one bit. A computer works with numbers: 8 bits for a byte, 32 or 64 for an integer. So we need to store a whole word together, and we need control over **when** it is stored. A processor's accumulator register must keep its value for many clock cycles while other parts of the machine work, and take a new value only when an instruction says so. A plain D flip-flop cannot do that: it takes whatever is on `d` at **every** clock edge.

We also need to move words between places that have only one wire between them, like a microcontroller sending a byte to a computer over a USB-serial cable: the word must be turned into a stream of bits and back. Both jobs are done by registers: flip-flops plus a little combinational logic in front of them.

## The Physics

A register is physically nothing more than its flip-flops, a shared clock wire and some gates. Two physical facts shape how it is built:

- **The clock must be clean.** Every flip-flop must see one sharp edge per cycle at almost the same time. Putting an AND gate in the clock path to "turn the clock off" when the register should hold adds delay (skew) and can create glitches, extra edges that corrupt the stored value. That is why the standard way to hold a value is to leave the clock alone and recirculate the data through a multiplexer.
- **Every flip-flop switches power.** Each clock edge charges the clock inputs of all flip-flops. In large chips, designers do gate the clock to save power, but only with special glitch-free clock-gating cells placed by tools that check the timing.

## The Concept

### A row of flip-flops

An n-bit register is n D flip-flops with the same clock. Bit `i` of the input `din` goes to flip-flop `i`, and its output is bit `i` of `q`. At every rising edge all bits are captured at once.

```
 din3   din2   din1   din0
   |      |      |      |
 [DFF]  [DFF]  [DFF]  [DFF]
   |      |      |      |
  q3     q2     q1     q0
   ^      ^      ^      ^
  clk ---+------+------+------ (shared)
```

### Adding a load enable

We want two behaviours at each edge:

- `load = 1`: take the new value, `q+ = din`.
- `load = 0`: keep the old value, `q+ = q`.

Say it as one sentence: "the next value is din when load is 1, and q when load is 0". That is exactly the next-state equation from Lesson 02 and the 2-to-1 multiplexer from Phase 14, Lesson 08:

```
d_i = load·din_i + load'·q_i
```

So each bit gets a mux in front of its flip-flop, with the flip-flop's own output fed back to the mux's "keep" input:

```
              +------+
  din_i ----->|1     |
              | MUX  |---- d_i ---->[DFF]---+----> q_i
        +---->|0     |                       |
        |     +--+---+                       |
        |        |                           |
        |      load                          |
        +------------------------------------+
```

With `load = 0` the flip-flop still receives a clock edge, but it simply reloads its own value: holding is "loading what you already have". All bits share one `load` wire and one inverter for `load'`. Per bit the cost is 2 AND gates, 1 OR gate and 1 flip-flop.

Worked trace for a 4-bit register (the simulator's output):

```
 edge  din  load | q
   1     9    1  |  9     loads 9 (1001)
   2     3    0  |  9     ignores 3, holds 9
   3    12    0  |  9     holds
   4    12    1  | 12     loads 12 (1100)
   5     5    0  | 12     holds
   6     0    1  |  0     loads 0
   7    15    1  | 15     loads 15
   8     6    0  | 15     holds
```

Our simulator's `dff` and `register` accept an `enable` argument that does the same thing internally, and the script shows both versions agree on every edge.

### Reset

Flip-flops start up random (Lesson 01). Registers usually add a **reset**: one more input that, when 1, forces the next value to 0 (synchronous reset: `d_i = reset'·(load·din_i + load'·q_i)`) or that clears the flip-flops immediately through dedicated pins (asynchronous reset). The simulator's `dff` accepts a `reset` wire: when it is 1 at a clock edge the flip-flop returns to its initial value.

### Shift registers

Connect the flip-flops in a chain instead: each one's `d` is its neighbour's `q`. At every edge, every bit moves one place, and a new bit enters at one end:

```
 serial_in -->[DFF]--q3-->[DFF]--q2-->[DFF]--q1-->[DFF]--q0--> serial_out
```

Send the 4-bit word 1011 into it, one bit per edge, least significant bit first (bits 1, 1, 0, 1):

```
 edge 1: serial_in = 1 -> q3 q2 q1 q0 = 1000
 edge 2: serial_in = 1 -> q3 q2 q1 q0 = 1100
 edge 3: serial_in = 0 -> q3 q2 q1 q0 = 0110
 edge 4: serial_in = 1 -> q3 q2 q1 q0 = 1011    the whole word, in parallel
 edge 5: serial_in = 0 -> q3 q2 q1 q0 = 0101    keeps shifting out at q0
```

After 4 edges, the word that arrived on **one** wire is available on **four** wires at once. This is **serial-in, parallel-out** (SIPO). Run it backwards, loading a word in parallel (with a mux in front of each flip-flop choosing "load" or "shift") and then shifting it out, and you have **parallel-in, serial-out** (PISO).

Why bother? Wires are expensive: pins on a chip, conductors in a cable, traces on a board. A UART (Phase 17, Lesson 06) sends a byte over one wire as a start bit, 8 data bits (LSB first) and a stop bit. At 9600 bits per second those 10 bits take `10 / 9600 = 1.04 ms`. SPI, I2C, USB, Ethernet and PCI Express all serialise data the same way, just faster.

Shifting also does arithmetic: moving every bit one place toward the MSB multiplies an unsigned number by 2 (`0011` = 3 becomes `0110` = 6), and moving toward the LSB divides by 2, dropping the remainder. Processors have shift instructions for exactly this.

### Register files: many registers, chosen by number

A processor has several registers (8, 16, 32 of them), numbered. An instruction like "add register 2 to register 5 and put the result in register 2" needs to:

- **Read** two registers chosen by number: a multiplexer per output port, with the register number on its select lines (Phase 14, Lesson 08). With 4 registers of 8 bits, a read port is eight 4-to-1 muxes sharing a 2-bit select.
- **Write** one register chosen by number: a decoder turns the register number into one-hot signals, and each one, ANDed with a global "write" signal, becomes the **load enable** of one register.

```
                 write_reg (2 bits)
                       |
                 [ 2-to-4 decoder ]---en3--+  en2  en1  en0
                       ^                    \   |    |    |
                     write                  [R3] [R2] [R1] [R0]   <- din on all of them
                                              |    |    |    |
                read_reg (2 bits) ----> [ 4-to-1 mux, 8 bits wide ] ---> read data
```

All registers see the same `din` wires, but only the one whose enable is on actually loads. Phase 16 builds the registers of our computer exactly like this.

### Why an enable instead of gating the clock

A tempting shortcut is to hold a register by feeding it `clk AND load` instead of `clk`. Two things go wrong:

1. If `load` changes while `clk` is high, the AND output makes an extra edge: the register loads at the wrong time.
2. The AND gate delays this register's clock compared with every other flip-flop's clock (skew). Data launched by other flip-flops on the true clock edge might arrive before this delayed edge and be captured one cycle too early (a hold violation, Lesson 07).

The mux-based enable keeps every flip-flop on the same clean clock and moves the decision into the data path, where glitches do not matter as long as they settle before the edge. Chip tools insert true clock gating only through special cells (a latch plus an AND) that are guaranteed glitch-free.

## Build It

The script `code/main.py` builds the registers of this lesson in `sim.logic`.

### Step 1: A register with load enable, gate by gate

```python
BITS = 4

def load_register():
    lc = LogicCircuit("4-bit register with load enable")
    din = [f"din{i}" for i in range(BITS)]
    q = [f"q{i}" for i in range(BITS)]
    lc.inputs(*din, "load")
    lc.not_("nload", "load")
    for i in range(BITS):
        lc.and_(f"p{i}", din[i], "load")
        lc.and_(f"r{i}", q[i], "nload")
        lc.or_(f"dn{i}", f"p{i}", f"r{i}")
        lc.dff(f"dn{i}", q[i], name=f"F{i}")
    lc.outputs(*q)
    return lc
```

`lc.dff(d, q)` adds an edge-triggered flip-flop (Lesson 03); `q[i]` is both the output and the "keep" input of the mux.

### Step 2: The same with the built-in enable

```python
def builtin_register():
    lc = LogicCircuit("4-bit register, built-in enable")
    din = [f"din{i}" for i in range(BITS)]
    q = [f"q{i}" for i in range(BITS)]
    lc.inputs(*din, "load")
    lc.register("R", din, q, enable="load")
    lc.outputs(*q)
    return lc
```

`register` creates one `dff` per bit, all with the same `enable` wire.

### Step 3: Drive both with numbers

```python
def bits_of(value, width=BITS):
    return [(value >> i) & 1 for i in range(width)]

def value_of(out, names):
    return sum(out[name] << i for i, name in enumerate(names))

def drive_load(lc, value, load):
    inputs = {f"din{i}": bit for i, bit in enumerate(bits_of(value))}
    inputs["load"] = load
    return value_of(lc.step(inputs), [f"q{i}" for i in range(BITS)])
```

Each `step` is one clock edge. The script prints the 8-edge trace shown above for both registers, and they agree on every edge.

### Step 4: A shift register

```python
def shift_register():
    lc = LogicCircuit("4-bit shift register")
    lc.inputs("serial_in")
    lc.dff("serial_in", "q3")
    lc.dff("q3", "q2")
    lc.dff("q2", "q1")
    lc.dff("q1", "q0")
    lc.outputs("q3", "q2", "q1", "q0")
    return lc
```

Because every flip-flop in `sim.logic` copies its `d` at the same instant on `step`, `q2` receives the **old** `q3`, not the new one, exactly as real edge-triggered flip-flops behave. (If they copied one after another, a bit would race through the whole chain in one edge.)

Run it:

```bash
uv run python phases/15-sequential-logic/04-registers/code/main.py
```

## Use It

- **74HC574 / 74HC374**: 8-bit registers (octal D flip-flops) with tri-state outputs, the classic way to latch a byte from a bus.
- **74HC595**: an 8-bit serial-in, parallel-out shift register with an output latch. Microcontrollers use it to drive 8 LEDs (or many more, chained) from just 3 pins.
- **74HC165**: an 8-bit parallel-in, serial-out shift register, used to read 8 buttons through 3 pins.
- **Processor register files**: an x86-64 processor has 16 general-purpose 64-bit registers in its instruction set (and hundreds of physical ones behind the scenes); RISC-V has 32.
- **SPI** (Phase 17, Lesson 06) is literally two shift registers, one in each chip, connected in a ring and clocked together: as one byte shifts out, another shifts in.

## Try It in the Lab

The lab task "Give a register bit a load enable" has one D flip-flop and the inverter `nload = load'` already in place. Three slots sit in front of the flip-flop: one combining `din` with `load`, one combining `q` with `nload`, and one combining the two into the flip-flop's input `dn`. Parts: AND, OR, NAND, NOR. The checker applies 8 clock edges with different `load` and `din` values and compares `q` after each edge.

Think about: write down `dn` as a function of `load`, `din` and `q`. Which gate opens a "door" for one signal under the control of another, and which gate combines two doors of which only one is open?

## Common Mistakes

- **Gating the clock with logic.** Using `clk AND load` as the clock gives glitches and skew. Use a mux enable in the data path.
- **Forgetting the feedback.** A "load enable" that outputs `load·din` alone clears the register to 0 whenever `load = 0`. The mux needs `q` on its keep input.
- **Shift direction and bit order.** Decide which end is the MSB and which bit is sent first. A UART sends LSB first; SPI usually sends MSB first. Mixing them reverses every byte.
- **Assuming flip-flops update one after another.** In a shift register all flip-flops sample at the same edge. That is why a shift register shifts by exactly one place per edge.
- **No reset.** A register's power-up value is random. If the design depends on it starting at zero, add a reset.

## Exercises

1. How many flip-flops and gates does an 8-bit register with load enable need, built as in this lesson?
2. A 4-bit shift register (as in the script) starts at 0000. The input bits 0, 1, 1, 0, 1 arrive on five edges. What is q3 q2 q1 q0 after each edge?
3. Add a synchronous clear to the 1-bit load-enable register: when `clear = 1` at an edge, `q` becomes 0 regardless of `load`. Write the new equation for `d`.
4. A 74HC595 chain drives 24 LEDs. How many clock edges are needed to update all of them, and how long does that take at a 1 MHz shift clock?
5. Design a 4-bit register that can **load**, **hold** or **shift right** depending on a 2-bit mode input (00 hold, 01 load, 10 shift). Which multiplexer goes in front of each flip-flop, and what is connected to each of its inputs?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Register | "A reg" | n flip-flops on one clock storing an n-bit word |
| Load enable | "Write enable", "en" | A mux in front of each flip-flop: `d = load·din + load'·q` |
| Shift register | "Shifter" | Flip-flops chained so each takes its neighbour's value at every edge |
| SIPO / PISO | "Serial to parallel" | Shift registers that convert between one wire and many |
| Register file | "Regfile" | Numbered registers with read muxes and a write decoder driving load enables |
| Reset | "Clear" | Forces a register to a known value, synchronously or asynchronously |
| Clock gating | "Turning off the clock" | Stopping a register's clock to save power; done only with special glitch-free cells |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 5, sections on registers, shift registers and register files.
- Texas Instruments datasheets *SN74HC595* (8-bit shift register with output latches) and *SN74HC574* (octal edge-triggered D-type flip-flops).
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 3 (Memory), where a register is built from a flip-flop and a multiplexer.
- Ben Eater, "8-bit register" videos (YouTube), building registers with load enables from 74LS173 chips.
