# Phase 19: Sensors and Signals

> A measurement is a chain from the physical world to a number, and every link either keeps the information or loses some of it. Learn where it leaks, and you can make a cheap sensor give an excellent reading.

This phase follows a measurement from start to finish. It begins with what a sensor is: a transfer function with a sensitivity, an offset, a range and non-linearities, plus the loading, calibration, accuracy and precision that decide whether a reading can be trusted. Then come the resistive sensors that are everywhere (NTC thermistors, light-dependent resistors, force-sensitive resistors) and the thermocouple, with the divider design that turns resistance into the biggest possible voltage swing, solved with our simulator. Signal conditioning shifts, amplifies and buffers that voltage with op-amps so it fills the ADC, and handles the millivolt outputs of strain-gauge bridges and the common-mode voltages around them. The second half is about the numbers once they are sampled: the sampling theorem and aliasing (and the anti-aliasing RC that must come before the ADC), quantization noise and the 6.02 N + 1.76 dB rule, the physical noise of resistors and currents and what averaging can and cannot do about it, and finally digital filters (moving average, exponential average and windowed-sinc FIR) written from scratch. It comes here because it ties together the analog circuits of Phases 04-13 with the microcontroller ADC of Phase 17.

**Prerequisites:** Phase 17 (Microcontrollers), Lesson 04 (ADC and DAC); Phase 13 (Operational Amplifiers); Phase 10 (Filters and Resonance); Phase 09 (Alternating Current), Lessons 02-03; Phase 04 (Kirchhoff's Laws), Lessons 05 and 07.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What a Sensor Is](01-what-a-sensor-is/) | Transfer function, sensitivity, offset and resolution in physical units; a loaded potentiometer in `sim`; two-point calibration; accuracy versus precision |
| 02 | [Temperature, Light and Force](02-temperature-light-and-force/) | NTC thermistors and the B equation, choosing the divider resistor for the largest swing (geometric mean) with `sim`, reading back to degrees, self-heating, LDRs, FSRs and thermocouples |
| 03 | [Signal Conditioning](03-signal-conditioning/) | Offset and gain to fill the ADC, a difference amplifier with clipping in `sim`, buffering a high-impedance source, strain-gauge bridges and common-mode rejection |
| 04 | [Sampling and Nyquist](04-sampling-and-nyquist/) | The Nyquist frequency, aliases and folding, identical samples of different tones, sinc reconstruction, and an RC anti-aliasing filter designed with `sim`'s AC analysis |
| 05 | [Quantization](05-quantization/) | Uniform rounding error, LSB / sqrt(12), SQNR = 6.02 N + 1.76 dB measured, SINAD and ENOB, small-signal distortion, and dither that lets averaging beat the LSB |
| 06 | [Noise](06-noise/) | Thermal and shot noise, noise bandwidth, averaging by sqrt(N), why 1/f noise defeats long averages, and cancelling mains hum by averaging whole periods |
| 07 | [Digital Filtering](07-digital-filtering/) | Moving average and its nulls, the exponential average as the twin of an RC simulated in `sim`, a windowed-sinc FIR checked against SciPy, median filtering, and a side-by-side comparison |

**Labs in this phase:**

- 02: choose the fixed resistor of a thermistor divider so 0 C to 50 C fills the ADC range
- 03: choose the gain resistors of a difference amplifier so a sensor's range fills the ADC without exceeding it
- 04: choose the resistor of an anti-aliasing RC that passes 100 Hz and attenuates the Nyquist frequency

Run the first lesson:

```
uv run python phases/19-sensors-and-signals/01-what-a-sensor-is/code/main.py
```
