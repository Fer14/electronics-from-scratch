# What Comes Next

> You started not knowing what a volt was. You end with a device you specified, simulated, laid out and debugged. Everything after this is the same method, applied to bigger things.

**Type:** Learn
**Prerequisites:** Phase 22 (Capstone), Lessons 01-06, and with them the whole course
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Verification matrix | A table listing every requirement with the evidence that it is met | A checklist signed at the end of a building inspection |
| Version 2 (rev B) | The next iteration of a design, fixing problems and adding features | The second edition of a book |
| Certification | Official testing that a product meets safety and radio-emission rules before it can be sold (CE, FCC, UL) | A car's roadworthiness test |
| EMC | Electromagnetic compatibility: a device must not disturb others, nor be disturbed by them | Neighbours agreeing not to play music too loudly |
| DFM | Design for manufacturing: making a design easy and cheap to build in volume | A recipe a bakery can repeat a thousand times a day |
| Firmware toolchain | The compiler, programmer and debugger used to put real code on a real microcontroller | The kitchen tools behind the recipe |
| Learning path | A sequence of topics and projects that builds on what you know | A hiking trail with marked stages |

## Learning Objectives

- Close the capstone with a verification matrix: every requirement, its evidence, pass or fail.
- Measure one design improvement (a MOSFET switch) with the same tools, and list others with the requirement each would change.
- Look back over the course and see how each phase contributed to the night light.
- Choose next steps: real tools (KiCad, a microcontroller toolchain, an oscilloscope), deeper subjects (analog, power, RF, digital and chip design) and the bridge to *Deep Learning from Scratch*.

## The Problem

A project is not finished when it works on your desk. It is finished when you can show, requirement by requirement, that it does what was promised, when you know what you would change next, and when someone else could pick it up from your documents. And a course is not finished when the last lesson is read, but when you know what to do next on your own.

This lesson does both: it closes the night light, and it points beyond it.

## The Physics

None that is new, and that is the point. Every number in the capstone came from physics you met earlier in the course:

- The **LDR** works because light frees charge carriers in a semiconductor (Phase 01, Lesson 07; Phase 11, Lesson 01).
- The **divider** that turns light into a voltage is Kirchhoff and Ohm (Phases 03-04).
- The **ADC** that turns the voltage into a number is quantization (Phase 17, Lesson 04; Phase 19, Lesson 05).
- The **LED** glows because electrons and holes recombine in a junction (Phase 11, Lessons 03 and 07).
- The **transistor** switch is a current-controlled valve made of two junctions (Phase 12).
- **PWM** dimming works because the eye averages fast pulses, and an RC filter does the same mathematically (Phases 07, 10 and 17).
- The **battery** is chemistry pumping charge (Phase 06, Lesson 03; Phase 18, Lesson 06).
- The **board** is resistivity, return currents and heat (Phase 21).
- The **firmware** runs on logic built from those same transistors (Phases 14-16).

## The Concept

### The verification matrix

The script re-runs the key checks from this phase in one place:

| Req | Evidence | Result |
|---|---|---|
| R1 | thresholds at ADC codes 389 and 583 for 5 and 15 lux (far apart) | PASS |
| R2 | 2 switchings in a full night with wobble and headlights (Lesson 04) | PASS |
| R3 | 1 kHz PWM, average 5.74 mA at 4.5 V | PASS |
| R4 | 32.3 nights from 2,000 mAh | PASS |
| R5 | average current spread 0.6% from 4.5 V to 3.6 V | PASS |
| R6 | 4.5 V maximum, parts \$1.79, board 40 x 30 mm (Lesson 05) | PASS |

Every requirement has evidence that someone else can re-run. That is the difference between "I think it works" and "here is why it works".

What the matrix does *not* prove is just as important. All of it is simulation and calculation. Real LDRs vary by a factor of two, real transistors' gains vary, real batteries sag in the cold. The next step would be measurements on real boards (Lesson 06's plan), over temperature and with several samples of each part.

### One improvement, measured

Lesson 02 noticed that 7% of the energy goes into the NPN transistor's base. A logic-level N-channel MOSFET needs gate current only while switching (its gate is a capacitor, Phase 12, Lesson 04):

```
NPN:    drive current 1.17 mA while on   ->  32.3 nights
MOSFET: drive current about 0 mA         ->  34.9 nights
```

About 2.6 more nights for a part that costs the same. The MOSFET also has a slightly lower on-voltage, so the LED current changes a little (15.2 instead of 14.7 mA at 4.2 V), which means the firmware's compensation would need recalibrating: every change ripples through the design, and the simulation shows where.

### Ideas for version 2

| Idea | Requirement it changes |
|---|---|
| logic-level MOSFET switch | R4: about 2-3 more nights |
| constant-current LED driver chip | R5: brightness independent of the battery, no calibration needed |
| ambient light sensor chip (I2C) | R1: calibrated lux readings; no cadmium (RoHS) |
| motion sensor (PIR): light only when someone passes | R4: months instead of weeks |
| USB-C charging and a Li-ion cell | R4: rechargeable; needs a charger IC and battery protection |
| enclosure with a light guide and a button | the product: keeps the LED's light away from the LDR, adds a manual mode |

Each is a new mini-project with the same steps: requirement, architecture, schematic, simulation, board, bring-up.

### Looking back: the course in one picture

```
 Phases 00-04   words, physics, first circuits, Ohm, Kirchhoff     -> the divider, the LED resistor
 Phases 05-06   our simulator, real sources and meters               -> every number in this phase
 Phases 07-10   capacitors, inductors, AC, filters                   -> decoupling, PWM averaging
 Phases 11-13   diodes, transistors, op-amps                         -> the LED, the switch, hysteresis
 Phases 14-17   logic, sequential logic, a computer, microcontrollers -> the firmware's hardware
 Phases 18-19   power and sensors                                    -> the LDO, the battery, the LDR, filtering
 Phase 20       chip design                                          -> what is inside the microcontroller, at scale
 Phase 21       PCB design and manufacturing                         -> the board
 Phase 22       the capstone                                         -> all of it, in one device
```

### Where to go next

**Build it for real.**
- Draw the schematic and board in **KiCad** (free), order five boards from a low-cost fab, and assemble them.
- Program a real microcontroller: an AVR (ATtiny) with avr-gcc or the Arduino environment, a Raspberry Pi Pico (RP2040) in C or MicroPython, or an STM32. Write the state machine of Lesson 04 in C.
- Get three instruments: a multimeter, a bench supply with current limit, and an oscilloscope (even an inexpensive USB one). Phase 06 explains what each does.

**Go deeper.**
- **Analog design**: amplifiers, noise, precision measurement. *The Art of Electronics* (Horowitz and Hill) is the companion for life.
- **Power electronics**: switching converters, battery management, motor drives (Phase 18 was the start).
- **RF and wireless**: antennas, transmission lines, Bluetooth and LoRa modules; needs the AC and filter ideas of Phases 09-10.
- **Digital and chip design**: Verilog on an FPGA with open-source tools (Yosys, nextpnr), then a real tape-out of a tiny design through a shared shuttle such as Tiny Tapeout (Phase 20, Lessons 09-11).
- **Products**: EMC, safety and certification (CE in Europe, FCC in the US), DFM and test. Products sold to the public must pass them; many design decisions (grounding, filtering, enclosure) are driven by these tests.

**Bridge to the other THOTH series.**
- *Deep Learning from Scratch* trains the models whose arithmetic Phase 20 put into silicon. You now know why those models use bf16 and fp8, why batching matters, why the KV cache is expensive, and what a "TFLOP" physically is.
- *Classic ML from Scratch* covers the statistics behind sensor calibration and anomaly detection, for example to tell a broken sensor from a real event.

### Safety, once more

We stayed at 12 V or less throughout the course, on purpose. If you move on to mains-powered projects, high-current batteries or high-voltage supplies, go back to Phase 00, Lesson 08 and take it seriously: learn from someone experienced, use isolated and certified power modules, and never work on live mains circuits alone.

## Build It

Run:

```
uv run python phases/22-capstone/07-what-comes-next/code/main.py
```

### Step 1: The verification matrix

```python
checks = [
    ("R1", f"on/off codes {on_code}/{off_code} for 5/15 lux", off_code - on_code > 50),
    ...
    ("R5", f"average current spread {spread * 100:.1f}% from 4.5 V to 3.6 V", spread <= 0.2),
    ...
]
```

`light_code` re-simulates the divider; `pwm_average` re-runs a short PWM transient at 4.5 V and 3.6 V with the compensated duty of Lesson 04; `nights` repeats Lesson 02's budget. R2 and R6 point to the evidence produced in Lessons 04 and 05.

### Step 2: The MOSFET

```python
def driver(vbat, switch="npn"):
    ...
    if switch == "npn":
        c.resistor("R4", "pin", "base", 2200)
        c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    else:
        c.resistor("R4", "pin", "gate", 100)
        c.nmos("M1", d="led_k", g="gate", s="0", vth=1.2, k=0.2)
```

The same driver with either switch. In DC the MOSFET's gate draws no current, so the drive current is zero and the nights go up.

### Step 3: Version 2

A list of ideas with the requirement each would change.

## Use It

- **Design reviews and post-mortems**: after every project, real teams write down what went well, what did not and what they would change. Our verification matrix and version-2 list are a small version of that document.
- **Open-source hardware**: publishing your schematic, board files, firmware and this kind of documentation (for example on GitHub, with an open hardware licence) lets others build, check and improve your device.
- **Portfolios**: a small, well-documented device with requirements, simulations and measurements is worth more to an employer or a university than a box of half-finished projects.

## Common Mistakes

- **Declaring victory on simulation alone.** Simulation predicts; measurement confirms. Plan the measurements.
- **Changing one thing without re-checking the others.** The MOSFET improved R4 but shifted the LED current, which affects R5's calibration.
- **Adding features before fixing the basics.** A motion sensor is exciting; a light that switches off when the batteries are half full is a failure. Verify version 1 first.
- **Stopping at the course.** The method is the valuable part. Apply it to your next idea while it is fresh.

## Exercises

1. Write the verification matrix of your own small project idea (at least four requirements), with the evidence you would need for each.
2. In the script, change the MOSFET's threshold to 2.5 V (`vth=2.5`). Does it still switch the LED fully with a 3.3 V gate drive? What does that teach you about "logic-level" MOSFETs?
3. Re-run the battery budget with a PIR motion sensor (quiescent current about 15 µA) that lights the LED for 2 minutes, 20 times per night, instead of all night. How many nights do the batteries last now?
4. Choose one "go deeper" direction and write a three-step learning plan for it, with one concrete project per step.
5. Harder: redesign the night light for a single 18650 Li-ion cell (3.0-4.2 V) with USB-C charging. Write the new requirements, sketch the new block diagram and power tree, and say which lessons of this phase you would redo and why.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Verification matrix | "the compliance table" | Every requirement listed with its evidence and verdict |
| Version 2 | "rev B" | The next iteration, driven by what version 1 taught you |
| Certification | "getting the CE mark" | Official tests for safety and EMC before a product can be sold |
| DFM | "making it buildable" | Design choices that make volume production cheap and reliable |
| Learning path | "what to study next" | A planned sequence of topics and projects |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed. (Cambridge University Press, 2015) — the reference to keep on your desk.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed. (McGraw-Hill, 2016) — projects and practical techniques.
- [KiCad](https://www.kicad.org/), [Tiny Tapeout](https://tinytapeout.com/) and the [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/) — real tools to continue with.
- [MIT OpenCourseWare 6.002, Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — a university-level second pass through the foundations.
