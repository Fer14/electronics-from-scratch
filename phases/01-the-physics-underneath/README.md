# Phase 01: The Physics Underneath

> Every rule in electronics is a shortcut for something electrons are physically doing.

Phase 00 introduced electricity in plain words: charge, current, voltage, power and the circuit. This phase opens the box and starts working with numbers. First come the two number tools every later lesson needs: units and prefixes (why 20 mA is 0.02 A and 4.7 kΩ is 4700 Ω), and scientific notation with orders of magnitude, so that a nanoamp and a kiloamp both feel like real quantities. Then we go inside the atom, with protons, neutrons and the electrons that do almost all the moving, and with J.J. Thomson's 1897 discovery that electrons exist at all. From there we build up the physics in small steps. Charge comes in two kinds, a naming choice Benjamin Franklin made before anyone knew about electrons, and it pushes and pulls according to Coulomb's law. An electric field is the push waiting at every point in space. Voltage is energy per charge, the electrical version of height. Materials are conductors, insulators or semiconductors depending on how many charges are free to move. Current is charge flowing past a point each second, and power is how fast that flow delivers energy. Every idea is checked with numbers you can work out yourself: how many electrons are in a copper wire, how slowly they actually drift, and how much a kilowatt-hour costs. This phase comes before any circuits so that Ohm's and Kirchhoff's laws (Phases 03 and 04) will feel like consequences of the physics, not rules to memorize.

**Prerequisites:** Phase 00 (Meet Electricity). If you can use a calculator and run a Python script, you are ready for the numbers.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Units and Prefixes](01-units-and-prefixes/) | Volts, amps, ohms, watts, joules, coulombs and friends, prefixes from pico to giga, conversions, unit sanity checks, mAh and Wh |
| 02 | [Scientific Notation and Orders of Magnitude](02-scientific-notation-and-orders-of-magnitude/) | Powers of ten, engineering notation, the range of real currents, voltages and resistances, and quick Fermi estimates |
| 03 | [Atoms and Electrons](03-atoms-and-electrons/) | What atoms are made of, the electron's charge and mass, valence electrons, Thomson's cathode rays, and counting the atoms in a copper wire |
| 04 | [Electric Charge and Coulomb's Law](04-electric-charge-and-coulombs-law/) | Two kinds of charge, Franklin's sign convention, conservation and quantization, the coulomb, Coulomb's law, and adding forces as vectors |
| 05 | [The Electric Field](05-the-electric-field/) | The field as force per unit charge, Faraday's field lines, the field of a point charge and between two plates, and superposition on a grid |
| 06 | [Energy, Potential and Voltage](06-energy-potential-and-voltage/) | Work and potential energy, the height analogy, the volt as a joule per coulomb, the electron-volt, and ground as the chosen zero |
| 07 | [Conductors, Insulators and Semiconductors](07-conductors-insulators-and-semiconductors/) | Free electrons and how many there are, a resistivity table spanning more than 20 orders of magnitude, and why silicon is special |
| 08 | [Current as Moving Charge](08-current-as-moving-charge/) | The ampere as a coulomb per second, electrons per second, slow drift vs fast signals, and conventional vs electron flow |
| 09 | [Energy and Power](09-energy-and-power/) | Joules and watts, P = V x I from the definitions, kilowatt-hours and the electricity bill, battery energy, efficiency and heat |

**Labs in this phase:** [Energy and Power](09-energy-and-power/) has a small dc lab where you choose a load to hit a target power.

Run the first lesson:

```
uv run python phases/01-the-physics-underneath/01-units-and-prefixes/code/main.py
```
