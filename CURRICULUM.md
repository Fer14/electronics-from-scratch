# Electronics from Scratch — curriculum (23 phases)

Single source of truth for phase and lesson slugs. Every lesson folder is `phases/NN-phase-slug/MM-lesson-slug/`.

Principles:
- **Start from absolute zero.** Assume the reader has never heard words like "voltage", "current", "ground", "node", "load" or "short". Every new word is introduced in plain language before it is used, every symbol is explained, and every formula is first told as a sentence.
- **Physics before rules.** Each rule (Ohm, Kirchhoff, capacitor charging, the diode equation) is shown to come from something physical before it is used as a tool.
- **Build it.** Each lesson's `code/main.py` computes or simulates what the lesson explains, with numbers the reader can check by hand. From Phase 05 on, our own circuit simulator (`sim/`) does the heavy lifting.
- **Do it.** Most lessons have a lab task (`lab/task.json`) in the interactive lab: put the right part in the right slot and meet the goal.
- **Depth over speed.** Lessons are long and detailed; it is fine to take many small steps.

| # | Phase (slug) | Lessons (MM-slug: title) |
|---|---|---|
| 00 | `00-words-and-units` | 01-what-electronics-is · 02-the-vocabulary · 03-units-and-si-prefixes · 04-scientific-notation-and-orders-of-magnitude · 05-reading-a-schematic · 06-safety-first |
| 01 | `01-the-physics-underneath` | 01-atoms-and-electrons · 02-electric-charge-and-coulombs-law · 03-the-electric-field · 04-energy-potential-and-voltage · 05-conductors-insulators-and-semiconductors · 06-current-as-moving-charge · 07-energy-and-power |
| 02 | `02-your-first-circuits` | 01-the-closed-loop · 02-batteries-and-loads · 03-switches-open-and-short-circuits · 04-series-and-parallel-intuition · 05-the-water-analogy-and-its-limits · 06-the-breadboard · 07-measuring-with-a-multimeter |
| 03 | `03-resistance-and-ohms-law` | 01-what-resistance-is · 02-resistivity-and-wires · 03-ohms-law · 04-resistors-and-color-codes · 05-power-and-heat · 06-tolerances-and-ratings · 07-when-ohms-law-fails |
| 04 | `04-kirchhoffs-laws` | 01-nodes-branches-and-loops · 02-kirchhoffs-current-law · 03-kirchhoffs-voltage-law · 04-series-and-parallel-resistors · 05-the-voltage-divider · 06-the-current-divider · 07-the-wheatstone-bridge |
| 05 | `05-circuit-analysis-and-our-simulator` | 01-systematic-analysis · 02-nodal-analysis · 03-mesh-analysis · 04-modified-nodal-analysis-from-scratch · 05-superposition · 06-thevenin-and-norton · 07-maximum-power-transfer · 08-dependent-sources |
| 06 | `06-sources-batteries-and-measurement` | 01-ideal-and-real-sources · 02-internal-resistance · 03-how-batteries-work · 04-inside-the-multimeter · 05-loading-and-measurement-error · 06-the-oscilloscope · 07-lab-power-supplies |
| 07 | `07-capacitors` | 01-storing-charge · 02-capacitance · 03-charging-and-discharging · 04-the-time-constant · 05-capacitors-in-series-and-parallel · 06-energy-in-the-electric-field · 07-real-capacitors · 08-transient-simulation-from-scratch |
| 08 | `08-magnetism-and-inductors` | 01-magnets-and-magnetic-fields · 02-electromagnetism · 03-faradays-law-and-induction · 04-the-inductor · 05-rl-transients · 06-transformers · 07-motors-and-generators |
| 09 | `09-alternating-current` | 01-why-alternating-current · 02-sine-waves-frequency-and-phase · 03-rms-values · 04-complex-numbers-for-circuits · 05-phasors · 06-impedance · 07-ac-power-and-power-factor |
| 10 | `10-filters-and-resonance` | 01-what-a-filter-does · 02-rc-low-pass-and-high-pass · 03-decibels-and-bode-plots · 04-rl-filters · 05-rlc-resonance · 06-band-pass-and-band-stop · 07-quality-factor · 08-ac-analysis-in-our-simulator |
| 11 | `11-semiconductors-and-diodes` | 01-why-silicon · 02-doping-n-and-p · 03-the-pn-junction · 04-the-diode-equation · 05-solving-nonlinear-circuits · 06-rectifiers · 07-leds · 08-zener-diodes |
| 12 | `12-transistors` | 01-the-transistor-idea · 02-the-bjt · 03-the-bjt-as-a-switch · 04-the-mosfet · 05-the-mosfet-as-a-switch · 06-amplifiers-and-biasing · 07-small-signal-thinking · 08-current-mirrors |
| 13 | `13-operational-amplifiers` | 01-the-ideal-op-amp · 02-the-comparator · 03-inverting-and-non-inverting-amplifiers · 04-summers-and-difference-amplifiers · 05-integrators-and-differentiators · 06-active-filters · 07-real-op-amp-limits |
| 14 | `14-digital-logic` | 01-analog-vs-digital · 02-binary-numbers · 03-boolean-algebra · 04-logic-gates · 05-cmos-gates-from-transistors · 06-combinational-circuits · 07-adders · 08-multiplexers-and-decoders |
| 15 | `15-sequential-logic` | 01-memory-from-feedback · 02-latches · 03-flip-flops-and-the-clock · 04-registers · 05-counters · 06-finite-state-machines · 07-timing-and-metastability |
| 16 | `16-a-computer-from-gates` | 01-what-a-computer-is · 02-the-alu · 03-memory · 04-the-datapath · 05-the-control-unit · 06-instructions-and-assembly · 07-running-a-program |
| 17 | `17-microcontrollers` | 01-what-a-microcontroller-is · 02-gpio · 03-pwm · 04-adc-and-dac · 05-timers-and-interrupts · 06-uart-i2c-and-spi · 07-a-virtual-microcontroller |
| 18 | `18-power-electronics` | 01-linear-regulators · 02-switching-converters · 03-the-buck-converter · 04-the-boost-converter · 05-motors-and-the-h-bridge · 06-batteries-and-charging · 07-heat-and-thermal-design |
| 19 | `19-sensors-and-signals` | 01-what-a-sensor-is · 02-temperature-light-and-force · 03-signal-conditioning · 04-sampling-and-nyquist · 05-quantization · 06-noise · 07-digital-filtering |
| 20 | `20-chip-design` | 01-from-gates-to-adders · 02-multiplying-in-hardware · 03-the-mac · 04-moving-data-costs-more · 05-clocks-critical-paths-and-pipelining · 06-systolic-arrays · 07-memory-on-the-chip · 08-the-roofline · 09-fpga-and-asic · 10-cpu-gpu-and-accelerators · 11-from-rtl-to-the-fab |
| 21 | `21-pcb-design-and-manufacturing` | 01-from-schematic-to-board · 02-footprints-and-traces · 03-ground-planes-and-current-return · 04-design-rules · 05-fabrication · 06-soldering-and-assembly · 07-debugging-a-board |
| 22 | `22-capstone` | 01-requirements · 02-architecture · 03-schematic · 04-simulation · 05-the-board · 06-bring-up · 07-what-comes-next |
