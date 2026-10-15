# Lab task format (`lab/task.json`)

Each lesson that has a hands-on exercise ships one `lab/task.json`. The same file is used by:
- the web lab (`lab/`), which draws the board, lets you drop parts into slots, simulates and checks the goals;
- `scripts/check.py`, which proves every task is solvable by simulating its reference solution with `sim/`.

## Kinds

| `kind` | Simulation | Typical goals |
|---|---|---|
| `dc` | operating point (`Circuit.dc()`) | voltage, current, power ranges |
| `transient` | time simulation (`Circuit.transient()`) | value at a time, time to cross a threshold, frequency |
| `ac` | frequency sweep (`Circuit.ac()`) | gain in dB at a frequency, cutoff frequency |
| `logic` | gate-level simulation (`sim.logic`) | truth table |
| `chip` | cost model (`sim.cost`) | area under a budget, critical path under a clock period, correct result |

## Schema

```json
{
  "id": "11-07-leds",
  "title": "Light the LED without burning it",
  "kind": "dc",
  "story": "A red LED wants about 10 mA. Your battery gives 9 V. Pick the resistor.",
  "board": {
    "nodes": {"vcc": [1, 1], "a": [5, 1], "gnd": [5, 4]},
    "ground": "gnd",
    "fixed": [
      {"type": "battery", "id": "B1", "plus": "vcc", "minus": "gnd", "volts": 9},
      {"type": "led", "id": "D1", "anode": "a", "cathode": "gnd", "color": "red"}
    ],
    "slots": [
      {"id": "S1", "a": "vcc", "b": "a", "accepts": ["resistor"]}
    ]
  },
  "parts": [
    {"type": "resistor", "ohms": 100},
    {"type": "resistor", "ohms": 680},
    {"type": "resistor", "ohms": 10000}
  ],
  "goals": [
    {"measure": "current", "of": "D1", "min": 0.005, "max": 0.015, "label": "LED current between 5 and 15 mA"},
    {"measure": "power", "of": "S1", "max": 0.25, "label": "the resistor stays under 1/4 W"}
  ],
  "solution": {"S1": {"type": "resistor", "ohms": 680}},
  "hints": ["The LED keeps about 2 V across itself.", "The resistor gets the rest: I = (9 - 2) / R."]
}
```

- `nodes` maps node names to grid coordinates (x 0–10, y 0–6) used only for drawing.
- Component types: `battery`/`voltage_source` (`plus`, `minus`, `volts`), `current_source` (`from`, `to`, `amps`), `resistor` (`a`, `b`, `ohms`), `capacitor` (`a`, `b`, `farads`, optional `v0`), `inductor` (`a`, `b`, `henries`, optional `i0`), `diode` (`anode`, `cathode`), `led` (`anode`, `cathode`, `color`), `zener` (`anode`, `cathode`, `vz`), `switch` (`a`, `b`, `closed`), `npn`/`pnp` (`c`, `b`, `e`), `nmos`/`pmos` (`d`, `g`, `s`), `opamp` (`plus`, `minus`, `out`), `pulse_source`/`sine_source` (`plus`, `minus`, plus wave parameters), `vcvs` (voltage-controlled voltage source: `plus`, `minus`, `cplus`, `cminus`, `gain`) and `vccs` (voltage-controlled current source: `plus`, `minus`, `cplus`, `cminus`, `gm`; the current `gm·v(cplus, cminus)` flows from `plus` through the source to `minus`), and for `logic`: `gate` (`op` one of and/or/not/nand/nor/xor, `inputs`, `output`).
- A slot connects its two terminals (`a`, `b`, or the type's own terminal names) and lists which part types it accepts; a filled slot behaves like a component with the slot's id.
- `measure` values: `voltage` (`at` node, or `between` [n1, n2]), `current` (`of` a component, positive in its reference direction), `power` (`of`), and for other kinds `voltage_at_time`, `time_to_cross`, `frequency`, `gain_db_at`, `cutoff_frequency`, `truth_table`, `area`, `critical_path`.
- `solution` maps slot ids to parts. `scripts/check.py` fills the slots with it, simulates and requires all goals to pass.

## Details per kind (what `sim/lab.py` and the web lab accept)

Common to every kind:
- `ground` defaults to `"gnd"`; the names `"0"` and `"gnd"` are always ground.
- A part dropped in a slot gets the slot's id (goals refer to `S1`, not to the part).
- Slot terminals: if the slot names the part's own terminals (`anode`/`cathode`, `c`/`b`/`e`, `d`/`g`/`s`, `plus`/`minus`/`out`, `plus`/`minus` for sources, `from`/`to`), they are used; otherwise the slot's `a`, `b` (and `c`) are mapped in order onto the part's terminals (e.g. `a` = anode, `b` = cathode; `a` = plus, `b` = minus).
- Extra part types: `wire` (a closed switch, 0 Ω) and `open` (nothing connected).
- Every goal takes `min` and/or `max` (SI units) and an optional `label`.
- Optional `"sim"` object with analysis settings (see below).

Optional component parameters: `diode` takes `model` (`"1n4148"`, `"1n4007"`, `"schottky"`) or `Is`, `n`; `led` colors are `red`, `orange`, `yellow`, `green`, `blue`, `white`, `infrared`; `zener` takes `vz`; `npn`/`pnp` take `beta`; `nmos`/`pmos` take `vth`, `k`; `opamp` takes `gain` and `rails: [lo, hi]`; `switch` takes `closed` and, in transients, `toggle_at: [t1, t2, ...]`; `pulse_source` takes `low`, `high`, `period`, `duty`, `delay`; `sine_source` takes `amplitude`, `freq`, `offset`, `phase_deg`; `vcvs`/`vccs` take `plus`, `minus`, `cplus`, `cminus`, `gain`/`gm`.

### `dc`
Measures: `voltage` (`at` or `between`), `current` (`of`; for transistors `"Q1"` is the collector/drain current, `"Q1.b"` the base current, `"Q1.e"` the emitter current), `power` (`of`; dissipated by passive parts and transistors, delivered by sources).
Current sign: resistor/switch/capacitor/inductor from `a` to `b`; diode/LED/zener from anode to cathode; battery: current leaving its `plus` terminal; current source: its `amps`.

### `transient`
`"sim": {"t_stop": 5e-3, "dt": 1e-5}` (default `t_stop` 1 s, `dt` = t_stop/2000). Capacitors start at `v0` (default 0) and inductors at `i0` (default 0).
Measures: `voltage_at_time` (`at`/`between`, `time`), `current_at_time` (`of`, `time`), `time_to_cross` (`at`, `level`, optional `direction` `"rising"`/`"falling"`; fails if it never crosses), `frequency` (`at`; from rising crossings of the mid level), `peak_voltage`, `min_voltage`, `ripple` (peak-to-peak over the second half of the run), `peak_current` (`of`), and `voltage`/`current`/`power` (value at the end of the run).

### `ac`
`"sim": {"source": "V1", "f_start": 1, "f_stop": 1e6, "points": 200}` (the source gets amplitude 1; default: the first source). Measures: `gain_db_at` (`at`, `freq`, optional `ref` node), `phase_deg_at` (same), `cutoff_frequency` (`at`; the frequency where the gain falls 3 dB below its largest value).

### `logic`
Board: `"inputs": ["a", "b"]`, `"outputs": ["s", "c"]`, optional `"clock": "clk"`. Fixed parts: `{"type": "gate", "id": "G1", "op": "xor", "inputs": ["a", "b"], "output": "s"}` and `{"type": "dff", "id": "F1", "d": "n1", "q": "q"}` (rising-edge, starts at 0). Slots: `{"id": "S1", "inputs": ["a", "b"], "output": "c", "accepts": ["gate"]}`; parts: `{"type": "gate", "op": "and"}` (a `not` uses only the first input). Node coordinates are optional for logic boards: nets without coordinates are laid out automatically in columns by logic depth (give coordinates for small, hand-drawn boards).
Measures: `truth_table` with `"expect": {"s": [0, 1, 1, 0], ...}`, one value per input combination counted in binary with the first input as the most significant bit; `sequence` with `"steps": [{"a": 1}, {"a": 0}, ...]` (one clock cycle per step, outputs read after the edge) and `"expect": {"q": [1, 0, ...]}`; `gate_count` and `depth` (logic levels) with `min`/`max`.

### `chip`
The board is a graph: nodes are points where data flows, every fixed part or slot is a block from node `a` to node `b`. Block types (part `type`): `adder` (`bits`), `multiplier` (`bits`), `mac` (`bits`, optional `acc_bits`), `register` (`bits`; cuts the timing path and adds one cycle of latency), `pipelined_multiplier` (`bits`, `stages`), `mux` (`inputs`, `bits`), `register_file` (`words`, `bits`), `sram` (`bits`), `systolic_array` (`rows`, `cols`, `bits`), `wire` (`bits`, optional `length`), `gates` (`area`, `depth`, optional `bits`). Costs come from `sim.cost` (area in gate units, delay in gate delays).
Measures: `area`, `critical_path` (longest gate-delay path between registers), `latency` (registers on the longest input-to-output path), `throughput` (MACs per cycle), `bits_moved` (bits crossing block boundaries per cycle), `energy` (per cycle, in gate-switch units), `bits` (`of` a block; e.g. an accumulator must be wide enough).
