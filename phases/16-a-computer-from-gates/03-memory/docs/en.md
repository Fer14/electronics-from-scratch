# Memory

> Memory is a grid of registers, a decoder that picks one row to write, and a multiplexer that picks one row to read.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 08 (Multiplexers and Decoders), Phase 15 (Sequential Logic), Lessons 01 and 04 (Memory from Feedback, Registers), Phase 16 (A Computer from Gates), Lesson 01 (What a Computer Is)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| RAM | Random-access memory: any address can be read or written in the same time | A wall of lockers you can open in any order |
| Word | The group of bits stored at one address (8 bits on the T8) | The contents of one locker |
| Address | The number that selects a word | The locker number |
| Capacity | How many words a memory holds | How many lockers there are |
| Write enable (WE) | The signal that says "store the data at this address now" | Turning the key to lock the locker shut with the new contents |
| Row select (word line) | The one-hot decoder output that activates one word | The light above the locker you are allowed to open |
| SRAM | Static RAM: each bit is a pair of cross-coupled inverters, kept as long as there is power | A light switch that stays where you put it |
| DRAM | Dynamic RAM: each bit is a tiny capacitor that leaks and must be refreshed | A bucket with a small leak that someone keeps topping up |
| Refresh | Re-reading and re-writing DRAM rows before their charge leaks away | Topping up the leaky buckets on a schedule |
| ROM | Read-only memory: contents fixed at manufacture or programming | A printed book |
| Flash | Non-volatile memory that stores charge on an insulated gate and keeps it without power | Writing in ink |
| Volatile | Loses its contents when power is removed | Writing in condensation on a window |
| Memory map | Which address ranges hold program, data and devices | A floor plan of the building |

## Learning Objectives

- Build a 16-byte RAM from 128 flip-flops, a 4-to-16 decoder and eight 16-to-1 read multiplexers in `sim.logic`.
- Explain how the write enable and the decoded address combine into one load enable per word.
- Verify the gate-level RAM against a Python list with random reads and writes.
- Compute how address width, flip-flop count and read logic grow with capacity.
- Explain physically how SRAM, DRAM, ROM and flash store bits, and why big memories use them instead of flip-flops.
- Use the T8's 256-byte memory model with the same read/write behaviour.

## The Problem

The T8 needs 256 bytes of memory for its program and data. One byte is a register (Phase 15, Lesson 04). So 256 bytes are 256 registers. But the processor talks to memory through a narrow doorway: an 8-bit address goes in, and one byte comes out or goes in. Somehow the memory must, for any address, connect exactly the right register to the data wires, quickly, and never disturb the other 255.

You already have the two tools: a **decoder** turns an address into one-hot select lines, and a **multiplexer** picks one of many values (Phase 14, Lesson 08). This lesson builds a complete 16-byte RAM from them at gate level, measures its cost, and then looks at why real memories use much smaller cells than a flip-flop, which is the only reason your phone can have billions of bytes.

## The Physics

### Static RAM: a bistable loop

The most direct memory cell is the bistable pair of inverters from Phase 15, Lesson 01, plus two **access transistors** that connect its two nodes to a pair of **bit lines** when the cell's **word line** is high. That is the **6T SRAM cell**: six transistors per bit (four for the inverters, two for access). To read, the bit lines are precharged and the selected cell pulls one of them slightly down; a sense amplifier (a comparator, Phase 13, Lesson 02) detects the difference. To write, strong drivers force the bit lines to the new value, overpowering the small cell. An SRAM keeps its data as long as it is powered, with no refresh: hence "static". Processor caches and register files are SRAM. A D flip-flop, in comparison, needs about 20-25 transistors.

### Dynamic RAM: a leaky capacitor

A **DRAM** cell is a single transistor and a tiny capacitor (about 10-30 fF). A charged capacitor is a 1, an empty one a 0 (Phase 07, Lesson 01: `Q = C V`). One transistor per bit makes DRAM about 6 times denser than SRAM, which is why main memory is DRAM. But the capacitor leaks through the transistor and the silicon, and the charge is so small that reading it disturbs it. So every row must be read and rewritten (**refreshed**) about every 64 ms, and every read is followed by a rewrite. That bookkeeping is done by the memory controller.

### Non-volatile memory: trapped charge

**Flash** memory stores charge on a "floating gate" (or a charge-trap layer) completely surrounded by insulator inside a MOSFET. The trapped charge shifts the transistor's threshold voltage (Phase 12, Lesson 04), so reading is just testing whether the transistor turns on. Writing pushes electrons through the insulator by quantum tunnelling with a high voltage. The charge stays for years without power. Microcontrollers keep their programs in flash (Phase 17), and SSDs are made of it. **ROM** in its oldest form has the bits fixed by the presence or absence of a transistor in the chip's mask: a lookup table (Phase 14, Lesson 08) frozen in silicon.

## The Concept

### The organisation of a RAM

Take 16 registers of 8 bits each: `word0` to `word15`. A 4-bit address `addr3..addr0` chooses one of them (2^4 = 16).

```
               addr (4 bits)
                   |
           [ 4-to-16 decoder ]
             sel0 ... sel15  (one-hot)
              |          |
    we --AND--+   ...    +--AND-- we        write enables: wen_w = sel_w · we
              |          |
           [word0]  ... [word15]           16 registers, each with load enable
              |          |                 all see the same din (8 bits)
              +--- [ read multiplexer ] ---+
                         |
                     dout (8 bits)
```

**Writing.** Every register's data input is connected to the same 8 data-in wires `din`. Each register has a load enable (Phase 15, Lesson 04). The decoder output `sel_w` says "this is the addressed word"; ANDed with the global write enable `we`, it becomes the load enable of word `w`:

```
wen_w = sel_w · we
```

At a clock edge with `we = 1`, exactly one register loads `din`; the other 15 reload their own values and keep them.

**Reading.** For each of the 8 data bits, a 16-to-1 multiplexer picks bit `i` of the addressed word. Since we already have the one-hot `sel` lines from the decoder, the mux is just an AND per word and one wide OR (Phase 14, Lesson 08):

```
dout_i = sel0·m0_i + sel1·m1_i + ... + sel15·m15_i
```

where `m_w_i` is bit `i` of word `w`.

### The decoder

Each select line is the minterm of its address (Phase 14, Lesson 08). Word 5 is address `0101`:

```
sel5 = addr3' · addr2 · addr1' · addr0
```

Four inverters (one per address bit, shared) and sixteen 4-input AND gates.

### A write and a read, step by step

Follow one write of the value 200 (`1100 1000`) to address 7 (`0111`), then one read of the same address.

**The write.** The inputs are `addr = 0111`, `din = 1100 1000`, `we = 1`.

```
decoder:   sel7 = addr3'·addr2·addr1·addr0 = 1·1·1·1 = 1
           every other sel_w has at least one literal at 0, so sel_w = 0
enables:   wen7 = sel7·we = 1;  wen_w = 0 for w != 7
clock edge: word7 loads 1100 1000; the other 15 words reload their own values
```

**The read.** Later, with `addr = 0111` and `we = 0`:

```
decoder:   sel7 = 1, all others 0
bit 3:     dout3 = sel0·m0_3 + ... + sel7·m7_3 + ... = 0 + ... + 1·1 + ... = 1
bit 0:     dout0 = ... + sel7·m7_0 + ... = 1·0 = 0
all bits:  dout = 1100 1000 = 200
```

Only the term of word 7 can be non-zero in each OR, because only `sel7` is 1. What the other words hold does not matter at all, which is exactly the "random access" promise: any address, same circuit, same delay.

A useful way to check your understanding: what happens if `we = 1` but the address changes **between** two clock edges? Nothing is written until the edge, so only the address present at the edge counts. That is why, in the T8 (Lesson 04), the address is placed in MAR one cycle before memory is read or written.

### Counting the cost

The simulator reports, for 16 bytes:

```
  flip-flops: 128 (16 words x 8 bits)
  gates: 172 (4 NOT, 160 AND, 8 OR)
  read path depth: 4 gate delays
```

Check the AND count by hand: 16 decoder ANDs + 16 write-enable ANDs + 16 x 8 = 128 read ANDs = 160. The 8 ORs are the 16-input ORs of the read muxes. (The load-enable multiplexers live inside the simulator's registers, as in Phase 15, Lesson 04.)

Now scale up. Capacity doubles with every extra address bit, and so do the flip-flops and the read gates:

```
 capacity     address bits   flip-flops   transistors as DFFs   as 6T SRAM cells
 16 bytes          4               128              2,816                 768
 256 bytes         8             2,048             45,056              12,288
 64 KiB           16           524,288         11,534,336           3,145,728
```

(At roughly 22 transistors per flip-flop.) A 64 KiB memory made of flip-flops would need over 11 million transistors, more than a whole 1990s processor. With 6T SRAM cells it is a quarter of that, and with 1T DRAM cells about 0.5 million. That is the economic reason memories are built from special cells arranged in square arrays, not from flip-flops and gates.

Real arrays also split the address in two: the high bits select a **row** (a word line, through a decoder), and the low bits select a **column** inside that row (through a multiplexer). A 1 Mbit array is 1024 rows of 1024 cells, so each decoder handles only 10 bits. Our design is a single "column" per word, which is fine for 16 bytes.

### Timing: reading and writing

- **Reading** is combinational: set the address and, after the decoder and mux delays (4 gate delays here, nanoseconds in a real SRAM, tens of nanoseconds in DRAM), the data appears on `dout`. The T8's control unit simply waits one clock cycle.
- **Writing** happens at a clock edge with `we = 1`. Address and data must be stable before the edge (setup time, Phase 15, Lesson 07). Changing the address while `we = 1` is a classic way to corrupt the wrong word.

### Testing the RAM

The simulator writes 42 to address 3, 200 to address 7, 90 to address 15, 1 to address 0, then reads them back, plus address 8 (never written, still 0). Then it overwrites address 3 and checks that address 7 did not change: a write must disturb **only** its own word. Finally it does 200 random reads and writes and compares every read with a Python list: 0 mismatches. A Python list is the perfect reference model for a memory: `cells[address] = value` and `cells[address]`.

### Memory in the T8

The T8 needs 256 bytes. We could build it exactly like the 16-byte RAM (2,048 flip-flops), and nothing about the design would change except the decoder width. But simulating 2,048 flip-flops gate by gate on every access would make the later lessons slow without teaching anything new. From here on the T8 uses a small Python class, `Memory`, with exactly the interface and behaviour of the gate-level RAM: `read(address)` returns the byte, `write(address, value)` stores the low 8 bits. Engineers do the same: a processor simulation uses a behavioural memory model that has been checked against the real memory design once.

### The memory map

All 256 addresses form one space. The T8 has no rules about where things go, but programs (Lesson 06) follow a convention:

```
0x00 - 0x7F   program code (the PC starts at 0x00)
0x80 - 0xFF   data (variables, tables)
```

Real computers put more into their memory map: ROM for the start-up code, RAM, and the registers of input/output devices (Phase 17: GPIO, timers and UART registers live at fixed addresses, so writing to a "memory" address switches a pin).

## Build It

The script `code/main.py` builds the RAM in `sim.logic`, tests it and introduces the T8's memory model.

### Step 1: Decoder and write enables

```python
def build_ram():
    lc = LogicCircuit("16 x 8 RAM")
    addr = [f"addr{k}" for k in range(ADDR_BITS)]
    din = [f"din{i}" for i in range(BITS)]
    lc.inputs(*addr, *din, "we")
    for k in range(ADDR_BITS):
        lc.not_(f"naddr{k}", addr[k])
    for w in range(WORDS):
        literals = [addr[k] if (w >> k) & 1 else f"naddr{k}" for k in range(ADDR_BITS)]
        lc.and_(f"sel{w}", *literals)
        lc.and_(f"wen{w}", f"sel{w}", "we")
        lc.register(f"word{w}", din, [f"m{w}_{i}" for i in range(BITS)], enable=f"wen{w}")
```

For word `w`, `literals` picks each address bit plain or inverted according to the bits of `w`: that is the minterm. `register` creates the 8 flip-flops of the word with `wen{w}` as their load enable.

### Step 2: Read multiplexers

```python
    for i in range(BITS):
        for w in range(WORDS):
            lc.and_(f"rd{w}_{i}", f"m{w}_{i}", f"sel{w}")
        lc.or_(f"dout{i}", *[f"rd{w}_{i}" for w in range(WORDS)])
    lc.outputs(*[f"dout{i}" for i in range(BITS)])
    return lc
```

### Step 3: Read and write

```python
def access(ram, address, data=0, write=0):
    inputs = {f"addr{k}": (address >> k) & 1 for k in range(ADDR_BITS)}
    inputs.update({f"din{i}": (data >> i) & 1 for i in range(BITS)})
    inputs["we"] = write
    if write:
        ram.step(inputs)
    out = ram.evaluate(inputs)
    return sum(out[f"dout{i}"] << i for i in range(BITS))
```

A write is one clock edge (`step`) with `we = 1`; a read just evaluates the combinational read path.

### Step 4: The behavioural memory of the T8

```python
class Memory:
    def __init__(self, size=256):
        self.cells = [0] * size

    def read(self, address):
        return self.cells[address & 0xFF]

    def write(self, address, value):
        self.cells[address & 0xFF] = value & 0xFF
```

`& 0xFF` keeps addresses and values to 8 bits, exactly what 8 wires can carry.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/03-memory/code/main.py
```

## Use It

- **SRAM chips** such as the 62256 (32 KiB x 8, 15 address pins, 8 data pins, active-low CE', OE' and WE') were the RAM of countless 8-bit computers and are still used on breadboard computers.
- **Processor caches** are SRAM arrays on the processor die: tens of KiB per core at level 1, megabytes at level 3, with access times from about 1 ns to 10 ns (Phase 20, Lesson 07).
- **DDR DRAM modules** in a PC hold gigabytes in 1T1C cells, organised in banks of rows and columns; opening a row takes around 15 ns and every row is refreshed about every 64 ms.
- **Microcontroller memory** (Phase 17): a typical small microcontroller has 32-256 KiB of flash for the program and 2-64 KiB of SRAM for variables, plus device registers in the same address map.
- **FPGA block RAM** is SRAM inside the FPGA, typically in 18 or 36 Kbit blocks, configurable in width and depth.

## Try It in the Lab

The lab task "Address decoder for a 4-byte memory" has two address bits `a1 a0` and their inverters already wired. Four slots, one per select line `y0..y3`, each receive the right pair of literals. Fill them so exactly the line whose number equals the address is 1. Parts: AND, OR, NOR, NAND.

Think about: what is the minterm of address 2 (`a1 = 1, a0 = 0`)? Which gate is 1 only when both of its inputs are 1?

## Common Mistakes

- **Forgetting to gate the write enable with the select line.** If every register gets `we` directly, a write stores the data in all 16 words at once.
- **Changing the address during a write.** The address and data must be stable around the clock edge, or the wrong word may be written.
- **Reading before the data is ready.** A read takes the decoder and multiplexer delay; DRAMs also need the row to be opened first. Memory datasheets give an access time for this.
- **Assuming memory starts at zero.** Real SRAM and DRAM power up with random contents. Programs must initialise their variables.
- **Mixing up capacity and address width.** n address bits give 2^n words: 8 bits give 256, 10 bits give 1024, 16 bits give 65,536.

## Exercises

1. A memory has 12 address bits and 16-bit words. How many words, how many bytes, and how many bits does it store?
2. For the 16-byte RAM, write the decoder minterm for address 11. Which 4 literals does it AND together?
3. Our RAM uses 160 AND gates. How many would a 32-byte version need, built the same way? How many flip-flops?
4. A DRAM cell has 25 fF and stores 1.0 V. How many electrons is that? (Use `Q = C V` and the electron charge 1.602e-19 C.) If it leaks 1 fA, how long until it has lost 10 % of its charge?
5. A 1 Mbit memory is organised as a square array. How many rows and columns? How many address bits go to the row decoder and how many to the column multiplexer? Compare with one decoder for all 2^20 cells.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| RAM | "Memory" | Addressable read/write storage with equal access time for any address |
| Word line / row select | "The decoder output" | One-hot line that enables one word (row) for reading or writing |
| Write enable | "WE" | Global signal ANDed with the row select to make one word's load enable |
| Read multiplexer | "Column mux", "sense path" | Picks the addressed word's bits onto the data-out wires |
| SRAM | "Static RAM" | Cross-coupled inverters plus access transistors (6T); fast, no refresh, volatile |
| DRAM | "Dynamic RAM" | One transistor and one capacitor per bit (1T1C); dense, needs refresh |
| Flash | "Non-volatile memory" | Charge trapped on an insulated gate shifts the threshold; keeps data without power |
| Memory map | "Address map" | Which address ranges hold code, data and device registers |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 5 (memory arrays: SRAM, DRAM, ROM, register files).
- Bruce Jacob, Spencer Ng and David Wang, *Memory Systems: Cache, DRAM, Disk* (2008), for how real memory arrays and DRAM refresh work.
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 3 (Memory), building RAM from registers step by step.
- Ben Eater, "Building RAM" videos for the 8-bit breadboard computer (YouTube), using 74LS189 16 x 4 RAM chips.
