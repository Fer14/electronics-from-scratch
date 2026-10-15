# UART, I2C and SPI

> Chips talk to each other by wiggling a few wires in an agreed rhythm. UART agrees on the speed, SPI shares a clock, and I2C lets many chips share two wires by only ever pulling down.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lessons 01-05; Phase 15 (Sequential Logic), Lesson 04 (Registers); Phase 14 (Digital Logic), Lesson 02 (Binary Numbers); Phase 07 (Capacitors), Lesson 04 (The Time Constant)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Serial communication | Sending data one bit after another down a single wire. | Spelling a word out letter by letter on the phone. |
| Parallel communication | Sending several bits at once on several wires. | Holding up eight flags at the same time. |
| Protocol | The agreed rules: voltage levels, timing, order of bits, who speaks when. | The rules of a radio conversation: "over", "over and out". |
| Baud rate | Bits per second on a UART line (for a two-level signal, baud = bits per second). | How fast the person spells. |
| UART | "Universal asynchronous receiver-transmitter": serial with no shared clock; both sides agree on a speed in advance. | Two people who have agreed to speak at exactly one letter per second. |
| Start bit / stop bit | Framing bits around each byte: a 0 to say "a byte begins", a 1 to say "it ended". | "Begin message" and "end message". |
| Synchronous | Sent together with a clock signal that says when to read each bit. | A conductor's baton telling the orchestra exactly when to play. |
| SPI | "Serial peripheral interface": a clock, a data line in each direction and a chip-select per device. | A conductor who points at one player at a time. |
| I2C | "Inter-integrated circuit": two shared wires (clock SCL and data SDA) for many devices, each with an address. | A party line where everyone shares one phone line and starts by saying the name of who they want. |
| Master / controller, slave / target | The device that starts transfers and drives the clock / the device that answers. Modern documents say controller and target. | The teacher who asks / the pupil who answers. |
| Open-drain | An output that can only pull the line low or let go; a resistor pulls it high. | Everyone holding a rope that a spring lifts: anyone can pull it down, nobody can push it up. |
| ACK / NACK | Acknowledge: the receiver pulls the data line low for one bit to say "got it". NACK: it does not. | Nodding (or not) after each sentence. |
| Bus capacitance | The capacitance of all the wires and pins on a shared line. | The weight of the rope the spring has to lift. |
| Rise time | How long a line takes to go from 30% to 70% of the supply (the I2C definition). | How long the spring takes to lift the rope. |

## Learning Objectives

- Draw a UART frame (start, eight data bits LSB first, stop) for any byte and compute bit and character times for a baud rate
- Decode a UART line by sampling in the middle of each bit, and show why the two clocks must agree to within a few percent
- Trace an SPI transfer as two shift registers swapping their contents, one bit per clock
- Explain how I2C's open-drain lines let many devices share wires, how addressing and ACK work
- Size an I2C pull-up resistor from the bus capacitance and the rise-time limit, checked with our simulator

## The Problem

A microcontroller rarely works alone. It reads a temperature sensor, writes to a small display, stores data on a memory chip, and reports to a computer. Giving each connection 8 or 16 wires would need hundreds of pins. Instead, chips send bits in series over two, three or four wires.

But sending bits in series raises questions that a single wire cannot answer by itself. When does a bit start and end? Which device on a shared wire is meant? Who speaks when? What if two speak at once? And the electrical question: how fast can a wire with real capacitance change from 0 to 1? Three protocols answer these questions in three different ways, and every embedded engineer uses all three.

## The Physics

### A wire is a capacitor

Every wire and every pin connected to a line forms a small capacitor with ground: roughly 10 pF per pin and some tens of pF per metre of cable. To change the line's voltage, the driver must move charge into or out of that capacitance. A push-pull output (Lesson 02) does this through tens of ohms, so it is fast. A pull-up resistor of kilohms does it much more slowly: the line rises with the time constant `RC` (Phase 07, Lesson 04). That single fact sets the speed limit of I2C.

### Pulling down is safe, pushing up is not

If two push-pull outputs connected to the same wire disagree, one connects the wire to VDD and the other to ground through only tens of ohms. The current is `3.3 V / 80 ohm = 41 mA`: a short circuit that can damage both. An **open-drain** output has only the lower transistor. It can pull the line to ground or release it. If several devices pull at once, nothing bad happens: the line is simply low. This is called **wired-AND**: the line is 1 only if *every* device releases it.

```
   VDD
    |
  [ R pull-up ]
    |
    +----------+----------+------- SDA line
    |          |          |
  [N]        [N]        [N]      each device has only a pull-down transistor
    |          |          |
   gnd        gnd        gnd
```

## The Concept

### UART: agree on the speed

The idle line sits at 1. To send a byte, the transmitter pulls the line to 0 for one bit time (the **start bit**), then sends the 8 data bits **least significant bit first**, then a 1 for one bit time (the **stop bit**). This is called **8N1**: 8 data bits, no parity bit, 1 stop bit.

Example: the letter 'H' is ASCII 72 = 0x48 = binary `01001000`. LSB first, the data bits are `0 0 0 1 0 0 1 0`:

```
idle  start  b0 b1 b2 b3 b4 b5 b6 b7  stop  idle
 1      0     0  0  0  1  0  0  1  0    1     1
```

At 9600 baud, one bit lasts:

```
bit time = 1 / 9600 s = 104.17 us,   one frame = 10 bits = 1.042 ms
```

So 9600 baud carries at most 960 characters per second: 10 bits on the wire for every 8 bits of data.

**Receiving:** the receiver watches for the falling edge of the start bit. It then waits 1.5 bit times, which puts it in the middle of bit 0, and samples. Then it samples every bit time after that: at 2.5, 3.5, ..., 8.5 bit times for bits 1 to 7, and at 9.5 for the stop bit. If the stop sample is not 1, it reports a **framing error**. Sampling in the middle gives the most margin on both sides.

**Why the clocks must agree:** each side times bits with its own clock. If the transmitter is 2% fast, its bits are 2% short, so by the stop bit (9.5 bits in) the receiver's sample has drifted 9.5 x 2% = 0.19 of a bit. Still inside. The sample falls off the edge of the stop bit when the drift reaches half a bit:

```
drift at the last sample = 9.5 x mismatch < 0.5 bit
mismatch < 0.5 / 9.5 = 5.3%
```

That is the total budget for both clocks together, and in practice designers keep each side under about 2%, because the edges are not perfectly sharp and the start edge is only detected to within a fraction of a bit. A microcontroller's internal RC oscillator, accurate to maybe 1-10%, is often not good enough; that is one reason boards carry crystals.

Our simulation shows a nasty detail: at 6% mismatch, the received bytes are wrong but **no framing error is reported**, because the last data sample lands on the stop bit and the stop sample lands on the idle line, which is also 1. Garbage that looks valid.

### SPI: share the clock

SPI uses four wires:

```
  controller                  target
  SCLK  ------------------->  SCLK    clock, driven by the controller
  MOSI  ------------------->  MOSI    controller out, target in   (also "COPI")
  MISO  <-------------------  MISO    controller in, target out   (also "CIPO")
  CS    ------------------->  CS      chip select, active low: "I'm talking to you"
```

Inside both chips is an 8-bit shift register (Phase 15, Lesson 04). On each clock, each side puts its top bit on its output wire and shifts in the bit arriving from the other side. After 8 clocks, the two registers have **swapped their contents**:

```
before:   controller 1001 1111 (0x9F)       target 0100 0010 (0x42)
clock 1:  MOSI = 1, MISO = 0
clock 2:  MOSI = 0, MISO = 1
...
after 8:  controller 0100 0010 (0x42)       target 1001 1111 (0x9F)
```

So every SPI transfer sends and receives at the same time (**full duplex**). To read a sensor, the controller sends a command byte and then sends dummy bytes to clock the answer out. Because the clock travels with the data, there is no speed agreement to get wrong: SPI happily runs at 10-50 MHz on a board. The price: one extra chip-select wire per target. (The "mode" of SPI, 0 to 3, says which clock edge and idle level are used; both sides must use the same.)

### I2C: share two wires, use addresses

I2C has just two lines, both open-drain with pull-ups: SCL (clock) and SDA (data). Every target has a 7-bit address. A write looks like this:

```
START | address (7 bits) + W (0) | ACK | register | ACK | value | ACK | STOP
```

- **START:** SDA falls while SCL is high. Normally SDA only changes while SCL is low, so this pattern is unmistakable.
- **Address byte:** 7 address bits plus a direction bit (0 = write, 1 = read).
- **ACK:** after each byte, the controller releases SDA for one clock. The target that recognised its address pulls SDA low: "acknowledged". If nobody pulls, the pull-up keeps SDA high: NACK, "no one here".
- **STOP:** SDA rises while SCL is high.

For a device at 0x48: `0x48 << 1 | 0 = 0x90 = 1001 0000`. Our simulation writes register 0x01 of a device at 0x48 (ACK, ACK, ACK) and then tries 0x49, where nobody answers (NACK).

### Sizing the I2C pull-up

When a device releases SDA, the pull-up `R` charges the bus capacitance `Cb` from about 0 V:

```
v(t) = VDD x (1 - e^(-t / RC))
```

The I2C specification measures rise time from 30% to 70% of VDD. The time to reach a fraction `k` of VDD is `t = RC x ln(1 / (1 - k))`, so:

```
t_30 = RC x ln(1 / 0.7) = 0.357 RC
t_70 = RC x ln(1 / 0.3) = 1.204 RC
rise time = t_70 - t_30 = RC x ln(7/3) = 0.847 RC
```

The limits in the specification are 1000 ns for standard mode (100 kHz) and 300 ns for fast mode (400 kHz). So the largest allowed pull-up is:

```
R_max = t_rise_max / (0.847 x Cb)
```

With `Cb = 200 pF` in fast mode: `R_max = 300 ns / (0.847 x 200 pF) = 300e-9 / 1.694e-10 = 1771 ohm`.

The smallest allowed pull-up comes from the other direction: when a device pulls SDA low, the pull-up current flows into it, and a device only has to sink 3 mA while keeping the line under 0.4 V:

```
R_min = (VDD - 0.4 V) / 3 mA = (3.3 - 0.4) / 0.003 = 967 ohm
```

So at 3.3 V, 200 pF, fast mode: anything between about 1 k and 1.77 k, for example 1.5 kohm. In standard mode, `R_max = 1000 ns / (0.847 x 200 pF) = 1000e-9 / 1.694e-10 = 5.9 kohm`, which is why "4.7 k pull-ups" are such a common default.

### Worked example: which bus is fast enough?

A sensor must deliver 100 readings per second, each made of three 16-bit values (6 bytes). How busy does each bus get?

**UART at 9600 baud.** Each byte costs 10 bits on the wire:

```
6 bytes x 10 bits x 100 per second = 6000 bits/s, out of 9600: 62% of the line
```

It works, but with little room for anything else. At 115 200 baud it would be 5%.

**I2C at 100 kHz.** A typical register read: START, address + W, register number, repeated START, address + R, six data bytes, STOP. Each byte is 9 clocks (8 bits + ACK):

```
2 address bytes + 1 register byte + 6 data bytes = 9 bytes x 9 clocks = 81 clocks
plus START, repeated START, STOP: about 84 clocks = 0.84 ms at 100 kHz
100 reads per second: 84 ms of every second = 8.4% of the bus
```

At 400 kHz: about 2%.

**SPI at 1 MHz.** One command byte plus six data bytes, 8 clocks each, no addressing overhead:

```
7 x 8 = 56 clocks = 56 us per reading; 100 per second = 0.56% of the time
```

SPI wins on speed, I2C on wire count (two wires for many devices), UART on simplicity and distance.

### Worked example: decoding a byte off the wire

A logic analyser captures a UART line at 9600 baud, idle high, and shows, after the falling start edge, this sequence of levels sampled mid-bit: `0 | 1 0 1 0 0 0 1 0 | 1`. The first 0 is the start bit and the final 1 the stop bit. The eight data bits arrive LSB first, so reverse them to read the byte:

```
received order (b0..b7):  1 0 1 0 0 0 1 0
written MSB first:        0 1 0 0 0 1 0 1  = 0x45 = 69 = 'E'
```

The same habit (check the start and stop bits, reverse LSB-first data) is how you debug every serial link by eye.

## Build It

### Step 1: UART frames and a receiver

`uart_frame_bits(byte)` returns `[0, b0, ..., b7, 1]`. `uart_line(message, baud)` turns a message into a function `level(t)` that gives the line voltage (as 0 or 1) at any time, plus the total duration. The receiver:

```python
def uart_receive(level, duration, baud, scan_step):
    received, errors = [], 0
    t = 0.0
    previous = 1
    while t < duration:
        current = level(t)
        if previous == 1 and current == 0:
            start = t
            byte = 0
            for bit in range(8):
                byte |= level(start + (1.5 + bit) / baud) << bit
            if level(start + 9.5 / baud) != 1:
                errors += 1
            received.append(byte)
            t = start + 9.5 / baud
            previous = 1
            continue
        previous = current
        t += scan_step
    return received, errors
```

It looks for the start edge every 1/16 of a bit (as real UARTs do, with 16x oversampling), then samples mid-bit. The script then makes the transmitter 0-8% fast and watches decoding break past about 5%.

### Step 2: SPI as two shift registers

```python
def spi_transfer(master_byte, slave_byte):
    master, slave = master_byte, slave_byte
    trace = []
    for _ in range(8):
        mosi = (master >> 7) & 1
        miso = (slave >> 7) & 1
        master = ((master << 1) & 0xFF) | miso
        slave = ((slave << 1) & 0xFF) | mosi
        trace.append((mosi, miso))
    return master, slave, trace
```

### Step 3: I2C as wired-AND

`I2cBus.line(pulls_low)` is the wired-AND: the line is 0 if any device pulls. `write_register` sends the address, register and value bytes MSB first, and after each byte asks whether a device with that address exists to pull SDA low for ACK.

### Step 4: The pull-up and bus capacitance in the simulator

`i2c_rise(R, Cb)` charges a 200 pF capacitor through the pull-up and measures the 30%-70% rise time from the simulated waveform.

Run it:

```
uv run python phases/17-microcontrollers/06-uart-i2c-and-spi/code/main.py
```

You will see the frames for 'H' and 'i', the decoded "Hi!", decoding that survives 5% mismatch and breaks at 6% (silently, without a framing error), the SPI swap of 0x9F and 0x42, an I2C write with three ACKs and one with a NACK, and the rise-time table: 1 k passes fast mode, 2.2 k and 4.7 k pass only standard mode, 10 k fails both.

## Use It

- **UART:** the Arduino's `Serial.println()` and the "USB serial" of most boards are a UART behind a USB converter chip. GPS modules, Bluetooth modules (HC-05) and many debugging consoles use UART at 9600 or 115 200 baud. RS-232 and RS-485 are the same framing with different voltage levels for longer cables.
- **SPI:** SD cards, fast displays, flash memory chips (W25Q series), and fast ADCs use SPI because it can run at tens of MHz.
- **I2C:** temperature and humidity sensors (BME280), accelerometers (MPU-6050), small OLED displays (SSD1306), real-time clocks (DS3231), port expanders (MCP23017) and the DAC MCP4725 of Lesson 04 all use I2C. The famous datasheet table "I2C address 0x76 or 0x77, selected by a pin" is the 7-bit address.
- **The I2C specification** (NXP UM10204) is free; its table of rise times, sink currents and bus capacitance (400 pF maximum) is what you design to.
- **Logic analysers** (cheap 8-channel USB ones work well) record these lines and decode the protocols on screen. They are the first tool to grab when two chips will not talk.

## Try It in the Lab

The lab is an I2C bus at 3.3 V with 200 pF of capacitance. At t = 0 a device releases SDA (the line starts at 0 V). Choose the pull-up so that SDA passes 70% of VDD (2.31 V) within 400 ns, which corresponds to fast-mode timing, while the current into a device that holds the line low (at t = 0, when the line is at 0 V) stays at or below 3 mA. One goal punishes resistors that are too big, the other those that are too small.

## Common Mistakes

- **Crossing TX and RX wrongly.** One device's TX goes to the other's RX. TX to TX means both talk and neither listens.
- **Mismatched baud rate or ground.** Garbage characters usually mean the wrong baud rate; nothing at all often means no common ground wire between the boards.
- **Forgetting I2C pull-ups.** Without them the lines can never go high. Some boards include them; adding a second set halves the resistance and may exceed the 3 mA limit.
- **Using 7-bit and 8-bit addresses interchangeably.** A datasheet might say 0x48 (7-bit) or 0x90/0x91 (the 8-bit byte including R/W). They are the same device.
- **Long I2C cables.** Cable capacitance adds up fast; beyond a metre or so you need smaller pull-ups, lower speed, or a bus buffer.
- **Leaving SPI chip-selects floating.** A target whose CS floats low thinks it is being spoken to and fights on MISO. Pull every CS high by default.
- **Mixing SPI modes.** If clock polarity or phase differ, every byte comes out shifted by one bit.

## Exercises

1. Draw the 8N1 frame for 'A' (0x41). How long does it take to send "OK\r\n" at 115 200 baud? (0 10000010 1; 4 characters x 10 bits / 115 200 = 347 us.)
2. A UART runs from an internal oscillator that can be 3% off; the other side is a crystal (0.01%). Is that safe? What if both use 3%-accurate oscillators in opposite directions? (3% is inside 5.3%, but with little margin; 6% total is not.)
3. In SPI mode 0, the controller sends 0xA5 while the target sends 0x3C. Write MOSI and MISO for each of the 8 clocks, and the final contents of both registers.
4. An I2C bus has 5 devices at 10 pF each and 30 cm of cable at 50 pF/m. What is Cb? What is the largest pull-up for fast mode? (65 pF; 300 ns / (0.847 x 65 pF) = 5.4 kohm.)
5. Harder: modify `I2cBus` so that a read transfer works: START, address + R, ACK, then the target drives 8 bits and the controller ACKs, then STOP. Use it to read back the value you wrote.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Baud rate | "Speed" | Bits per second on the line, including start and stop bits |
| 8N1 | "Serial settings" | 8 data bits, no parity, 1 stop bit per character |
| Asynchronous | "No clock" | Both sides time bits with their own clocks agreed in advance |
| SPI | "The fast bus" | Clocked full-duplex serial with a chip-select per target |
| I2C | "The two-wire bus" | Open-drain clock and data shared by addressed devices |
| ACK | "Got it" | Receiver pulls SDA low during the ninth clock of a byte |
| Open-drain | "Pull-down only" | Output that can sink current but not source it; a resistor pulls high |
| Rise time | "Edge speed" | Time from 30% to 70% of VDD, about 0.847 RC for a pull-up |

## Further Reading

- [NXP, UM10204 "I2C-bus specification and user manual"](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) — the official specification, including the rise-time and pull-up sizing section
- [Texas Instruments, SLVA689 "I2C Bus Pullup Resistor Calculation"](https://www.ti.com/lit/an/slva689/slva689.pdf) — a short application note on exactly the calculation in this lesson
- [SparkFun tutorials: "Serial Communication", "Serial Peripheral Interface (SPI)" and "I2C"](https://learn.sparkfun.com/tutorials/serial-communication) — friendly introductions with pictures
- [Analog Devices, "Introduction to SPI Interface"](https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html) — SPI modes and timing
