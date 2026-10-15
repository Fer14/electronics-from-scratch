# Phase 08: Magnetism and Inductors

> Moving charge makes magnetism, and changing magnetism moves charge. Coils, transformers and motors are those two sentences built in copper.

So far every circuit in this course has been about charges pushed through resistors or stored on capacitor plates. This phase opens the other half of electromagnetism. You start with plain magnets and the invisible field around them, then discover (as Oersted did in 1820) that every current is surrounded by a magnetic field, and (as Faraday did in 1831) that a changing magnetic field pushes a voltage around a wire. Those two facts give you the inductor, the partner of the capacitor that resists changes in current instead of voltage; the RL transient and the dangerous voltage spike you get when you switch a coil off; the transformer that trades voltage for current; and the motor and generator, which turn out to be the same machine. It comes right after capacitors because the inductor mirrors the capacitor almost equation for equation, and right before alternating current because AC is what spinning generators make and what transformers need.

**Prerequisites:** Phase 01 (The Physics Underneath), Phase 05 (Circuit Analysis and Our Simulator), Phase 07 (Capacitors)

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Magnets and Magnetic Fields](01-magnets-and-magnetic-fields/) | Poles, field lines, the tesla, the 1/z³ field of a magnet, and the sideways force F = q v B on a moving charge |
| 02 | [Electromagnetism](02-electromagnetism/) | The field around a wire, coils and solenoids, iron cores and saturation, forces on wires, and driving a relay coil |
| 03 | [Faraday's Law and Induction](03-faradays-law-and-induction/) | Magnetic flux, EMF = -N dPhi/dt, Lenz's law, the spinning-coil sine wave and a magnet falling through a coil |
| 04 | [The Inductor](04-the-inductor/) | Self-induction, L = mu N² A / l, v = L di/dt, energy ½ L I², and why an inductor is a wire at DC |
| 05 | [RL Transients](05-rl-transients/) | tau = L / R, exponential rise and decay, inductive kick and the flyback diode |
| 06 | [Transformers](06-transformers/) | Turns ratio, power conservation, reflected impedance, coupled coils simulated two ways |
| 07 | [Motors and Generators](07-motors-and-generators/) | Torque, back-EMF, the motor equation, stall current, efficiency, and generators as brakes |

Labs in this phase:

- **02 Pull in the relay without cooking its coil** (dc): choose the series resistor for a 400 ohm relay coil on 24 V
- **04 Let the DC through** (dc): find the part that is a wire at DC
- **05 Set the RL time constant to 1 ms** (transient): pick R so that tau = L / R hits the target
- **07 Switch off the motor without a spark** (transient): tame the inductive kick of a motor winding

Run the first lesson:

```bash
uv run python phases/08-magnetism-and-inductors/01-magnets-and-magnetic-fields/code/main.py
```
