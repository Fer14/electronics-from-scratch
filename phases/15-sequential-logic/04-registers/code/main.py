from sim.logic import LogicCircuit

BITS = 4


def bits_of(value, width=BITS):
    return [(value >> i) & 1 for i in range(width)]


def value_of(out, names):
    return sum(out[name] << i for i, name in enumerate(names))


def load_register():
    lc = LogicCircuit("4-bit register with load enable")
    din = [f"din{i}" for i in range(BITS)]
    q = [f"q{i}" for i in range(BITS)]
    lc.inputs(*din, "load")
    lc.not_("nload", "load")
    for i in range(BITS):
        lc.and_(f"p{i}", din[i], "load")
        lc.and_(f"r{i}", q[i], "nload")
        lc.or_(f"dn{i}", f"p{i}", f"r{i}")
        lc.dff(f"dn{i}", q[i], name=f"F{i}")
    lc.outputs(*q)
    return lc


def builtin_register():
    lc = LogicCircuit("4-bit register, built-in enable")
    din = [f"din{i}" for i in range(BITS)]
    q = [f"q{i}" for i in range(BITS)]
    lc.inputs(*din, "load")
    lc.register("R", din, q, enable="load")
    lc.outputs(*q)
    return lc


def shift_register():
    lc = LogicCircuit("4-bit shift register")
    lc.inputs("serial_in")
    lc.dff("serial_in", "q3")
    lc.dff("q3", "q2")
    lc.dff("q2", "q1")
    lc.dff("q1", "q0")
    lc.outputs("q3", "q2", "q1", "q0")
    return lc


def drive_load(lc, value, load):
    inputs = {f"din{i}": bit for i, bit in enumerate(bits_of(value))}
    inputs["load"] = load
    return value_of(lc.step(inputs), [f"q{i}" for i in range(BITS)])


def main():
    print("=== 4-bit register with load enable (mux in front of each flip-flop) ===")
    reg = load_register()
    ref = builtin_register()
    plan = [(9, 1), (3, 0), (12, 0), (12, 1), (5, 0), (0, 1), (15, 1), (6, 0)]
    print("  edge  din  load | q    | built-in")
    for n, (value, load) in enumerate(plan, start=1):
        mine = drive_load(reg, value, load)
        theirs = drive_load(ref, value, load)
        print(f"   {n}    {value:2d}    {load}   | {mine:2d}   |  {theirs:2d}")
    print(f"  gates {reg.gate_count()} + flip-flops {reg.counts()['dff']}; per bit: 2 AND + 1 OR + 1 DFF, plus one shared NOT")

    print("\n=== Shift register: serial in, parallel out ===")
    sr = shift_register()
    message = 0b1011
    sent = [(message >> k) & 1 for k in range(BITS)]
    print(f"  sending {message:04b} one bit per clock edge, LSB first: {sent}")
    for edge, bit in enumerate(sent + [0, 0], start=1):
        out = sr.step({"serial_in": bit})
        pattern = f"{out['q3']}{out['q2']}{out['q1']}{out['q0']}"
        print(f"   edge {edge}: serial_in = {bit} -> q3 q2 q1 q0 = {pattern}")
    print("  after 4 edges the whole 4-bit word sits in parallel on q3..q0 = 1011; more edges shift it out")

    print("\n=== Parallel to serial: how a UART sends a byte ===")
    byte = 0b01001101
    line = [(byte >> k) & 1 for k in range(8)]
    print(f"  byte 0x{byte:02X} = {byte:08b}, sent LSB first on one wire: {line}")
    baud = 9600
    print(f"  at {baud} bits per second, 8 data bits + start + stop take {10 / baud * 1e3:.2f} ms")


if __name__ == "__main__":
    main()
