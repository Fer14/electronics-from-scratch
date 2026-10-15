# Phase 17: Microcontrollers

> A microcontroller is the computer you built in Phase 16, shrunk onto one chip and given legs: it reads the world through some pins and pushes on it through others.

In Phase 16 you built a computer from gates. This phase turns it into the thing that actually sits inside microwaves, thermostats, toys and cars: a microcontroller, one chip holding a small processor, flash memory for the program, RAM, and a set of peripherals that talk to the outside world. Each lesson adds one peripheral to a virtual microcontroller written in Python and then uses our circuit simulator to see what happens on the other side of the pin. You will run assembly code and count its cycles, configure pins as outputs and inputs with pull-ups, size the resistor for an LED, make "analog" voltages with PWM and an RC filter, measure voltages with a successive-approximation ADC and make them with an R-2R DAC, keep time with timers and react with interrupts, debounce buttons, and send bytes over UART, SPI and I2C (including sizing I2C pull-ups for the bus capacitance). The last lesson puts everything on one chip: a firmware image with an interrupt vector runs a night light that reads a light sensor and dims an LED, while `sim` plays the outside world. It comes here because it needs both halves of the course: the digital machinery of Phases 14-16 and the analog circuits of Phases 04-13.

**Prerequisites:** Phase 16 (A Computer from Gates); Phase 15 (Sequential Logic) for counters and registers; Phase 11 (Semiconductors and Diodes), Lesson 07 (LEDs); Phase 07 (Capacitors) for RC charging; Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What a Microcontroller Is](01-what-a-microcontroller-is/) | Core, flash, RAM and peripherals on one chip; an assembler and a fetch-decode-execute core in Python; cycles to time; memory-mapped I/O driving an LED in `sim` |
| 02 | [GPIO](02-gpio/) | DDR, PORT and PIN registers; an output as a source with driver resistance; LED resistor sizing; sourcing vs sinking; pull-ups, floating inputs and VIL/VIH |
| 03 | [PWM](03-pwm/) | A PWM timer from a counter and a compare register; duty, frequency and resolution; PWM into an RC filter in `sim`; average and ripple |
| 04 | [ADC and DAC](04-adc-and-dac/) | LSB and codes; a successive-approximation ADC bit by bit; a battery-monitor divider and source resistance; an R-2R ladder DAC in `sim` and the MSB step error |
| 05 | [Timers and Interrupts](05-timers-and-interrupts/) | Prescaler and compare values; polling vs interrupts in a cycle-level simulation (lost ticks and latency); software debounce; RC debounce timing in `sim` |
| 06 | [UART, I2C and SPI](06-uart-i2c-and-spi/) | UART frames and baud mismatch; SPI as swapping shift registers; I2C open-drain, addresses and ACK; I2C pull-up sizing from rise time in `sim` |
| 07 | [A Virtual Microcontroller](07-a-virtual-microcontroller/) | A complete virtual chip: firmware with vectors, sleep, timer, ADC, PWM, GPIO and UART, running a night light against an LDR divider and an RC filter simulated by `sim` |

**Labs in this phase:**

- 02: choose the series resistor for an LED on a 3.3 V GPIO pin (LED current and pin voltage)
- 03: choose the PWM duty cycle that gives a target average after an RC filter
- 04: choose the divider resistor that fits a 14.4 V battery into a 3.3 V ADC
- 05: choose the debounce capacitor so a released button crosses the logic threshold at the right time
- 06: choose the I2C pull-up for fast-mode rise time without exceeding the 3 mA sink current
- 07: choose the capacitor that smooths the night light's PWM with little ripple and fast enough settling

Run the first lesson:

```
uv run python phases/17-microcontrollers/01-what-a-microcontroller-is/code/main.py
```
