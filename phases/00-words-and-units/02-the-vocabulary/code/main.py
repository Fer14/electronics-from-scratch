import numpy as np

ELECTRON_CHARGE = 1.602176634e-19

GLOSSARY = [
    ("charge", "Q", "coulomb (C)", "the property that makes particles push or pull on each other"),
    ("voltage", "V", "volt (V)", "the push on charge between two points: energy per charge"),
    ("current", "I", "ampere (A)", "how much charge flows past a point each second"),
    ("resistance", "R", "ohm (Ω)", "how hard a part makes it for current to flow"),
    ("power", "P", "watt (W)", "how fast energy is delivered or used"),
    ("energy", "E", "joule (J)", "the total amount of work done or stored"),
    ("circuit", "-", "-", "a closed loop that charge can travel around"),
    ("source", "-", "-", "a part that pushes charge and gives energy (battery, socket)"),
    ("load", "-", "-", "a part that takes energy and turns it into something (lamp, motor)"),
    ("node", "-", "-", "a set of points joined by wire, all at the same voltage"),
    ("branch", "-", "-", "one path between two nodes, holding one part"),
    ("ground", "-", "-", "the node we agree to call 0 V and measure everything from"),
    ("short circuit", "-", "-", "an unintended path with almost no resistance"),
    ("open circuit", "-", "-", "a break in the loop, so no current can flow"),
    ("conductor", "-", "-", "a material that lets charge move easily (copper)"),
    ("insulator", "-", "-", "a material that almost stops charge moving (plastic, glass)"),
    ("terminal", "-", "-", "a place on a component where you connect a wire"),
    ("polarity", "-", "-", "which terminal is + and which is -"),
]

FLASHLIGHT_PARTS = [
    ("battery", "source", "plus", "top", "minus", "gnd"),
    ("bulb", "load", "a", "top", "b", "strip"),
    ("switch", "control", "a", "strip", "b", "gnd"),
]


def nodes_of(parts):
    found = []
    for _, _, _, first_node, _, second_node in parts:
        for node in (first_node, second_node):
            if node not in found:
                found.append(node)
    return found


def flashlight_state(battery_volts, bulb_ohms, switch_closed, internal_ohms=0.0, bulb_shorted=False):
    load_ohms = 0.0 if bulb_shorted else bulb_ohms
    if not switch_closed:
        return {"current": 0.0, "top": battery_volts, "strip": battery_volts, "across_switch": battery_volts}
    current = battery_volts / (internal_ohms + load_ohms)
    top = battery_volts - current * internal_ohms
    return {"current": current, "top": top, "strip": 0.0, "across_switch": 0.0}


print("Step 1: the glossary")
print(f"  {'word':<14} {'symbol':<7} {'unit':<12} meaning")
for word, symbol, unit, meaning in GLOSSARY:
    print(f"  {word:<14} {symbol:<7} {unit:<12} {meaning}")

print()
print("Step 2: quiz yourself (answers shown underneath)")
rng = np.random.default_rng(7)
picks = rng.choice(len(GLOSSARY), size=4, replace=False)
for number, index in enumerate(picks, start=1):
    word, _, _, meaning = GLOSSARY[index]
    print(f"  Q{number}. Which word means: '{meaning}'?")
    print(f"       answer: {word}")

print()
print("Step 3: the flashlight in these words")
print(f"  {'part':<8} {'role':<8} terminals -> nodes")
for name, role, first_terminal, first_node, second_terminal, second_node in FLASHLIGHT_PARTS:
    print(f"  {name:<8} {role:<8} {first_terminal}->{first_node}, {second_terminal}->{second_node}")
nodes = nodes_of(FLASHLIGHT_PARTS)
print(f"  nodes: {nodes}  ({len(nodes)} nodes, {len(FLASHLIGHT_PARTS)} branches)")
print("  ground: 'gnd' is the node we call 0 V")

print()
print("Step 4: numbers for the flashlight (preview: current = voltage / resistance)")
battery_volts = 3.0
bulb_ohms = 12.0
state = flashlight_state(battery_volts, bulb_ohms, switch_closed=True)
power = battery_volts * state["current"]
seconds = 3600
charge = state["current"] * seconds
electrons = charge / ELECTRON_CHARGE
print(f"  source voltage: {battery_volts} V    load resistance: {bulb_ohms} Ω")
print(f"  current = {battery_volts} V / {bulb_ohms} Ω = {state['current']:.2f} A")
print(f"  power   = {battery_volts} V x {state['current']:.2f} A = {power:.2f} W")
print(f"  energy in one hour = {power:.2f} W x {seconds} s = {power * seconds:.0f} J")
print(f"  charge in one hour = {state['current']:.2f} A x {seconds} s = {charge:.0f} C")
print(f"  that is {charge:.0f} C / {ELECTRON_CHARGE:.4e} C = {electrons:.3e} electrons")
print(f"  node voltages measured from ground: top = {state['top']:.1f} V, strip = {state['strip']:.1f} V, gnd = 0.0 V")

print()
print("Step 5: open and short")
opened = flashlight_state(battery_volts, bulb_ohms, switch_closed=False)
print(f"  switch open : current = {opened['current']:.2f} A, voltage across the switch gap = {opened['across_switch']:.1f} V")
internal_ohms = 0.2
normal = flashlight_state(battery_volts, bulb_ohms, True, internal_ohms=internal_ohms)
shorted = flashlight_state(battery_volts, bulb_ohms, True, internal_ohms=internal_ohms, bulb_shorted=True)
print(f"  with the battery's own {internal_ohms} Ω inside it:")
print(f"    normal      : current = {normal['current']:.3f} A, heat inside battery = {normal['current'] ** 2 * internal_ohms:.3f} W")
print(f"    bulb shorted: current = {shorted['current']:.1f} A, heat inside battery = {shorted['current'] ** 2 * internal_ohms:.1f} W")
print(f"    the short draws {shorted['current'] / normal['current']:.0f} times more current")
