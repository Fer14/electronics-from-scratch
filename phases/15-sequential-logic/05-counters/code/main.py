from sim.logic import LogicCircuit


def sync_counter(bits):
    lc = LogicCircuit(f"{bits}-bit synchronous counter")
    lc.inputs("en")
    toggle = "en"
    for i in range(bits):
        lc.xor(f"d{i}", f"q{i}", toggle)
        lc.dff(f"d{i}", f"q{i}", name=f"F{i}")
        if i < bits - 1:
            lc.and_(f"t{i + 1}", toggle, f"q{i}")
            toggle = f"t{i + 1}"
    lc.outputs(*[f"q{i}" for i in range(bits)])
    return lc


def decade_counter():
    lc = LogicCircuit("decade counter 0-9")
    lc.inputs("en")
    lc.and_("nine", "q3", "q0")
    lc.and_("wrap", "nine", "en")
    toggle = "en"
    for i in range(4):
        lc.xor(f"d{i}", f"q{i}", toggle)
        lc.dff(f"d{i}", f"q{i}", name=f"F{i}", reset="wrap")
        if i < 3:
            lc.and_(f"t{i + 1}", toggle, f"q{i}")
            toggle = f"t{i + 1}"
    lc.outputs("q3", "q2", "q1", "q0")
    return lc


def count(out, bits):
    return sum(out[f"q{i}"] << i for i in range(bits))


def ripple_counter_events(start, bits=4, tcq_ns=10):
    q = [(start >> i) & 1 for i in range(bits)]
    events = []
    time = 0
    stage = 0
    while stage < bits:
        time += tcq_ns
        old = q[stage]
        q[stage] ^= 1
        events.append((time, sum(b << i for i, b in enumerate(q))))
        if old == 1:
            stage += 1
        else:
            break
    return events


def main():
    print("=== 4-bit synchronous counter: q_i flips when en and all lower bits are 1 ===")
    counter = sync_counter(4)
    values = [count(counter.step({"en": 1}), 4) for _ in range(18)]
    print(f"  18 edges with en = 1: {values}")
    held = [count(counter.step({"en": e}), 4) for e in [0, 0, 1, 0, 1]]
    print(f"  then en = 0, 0, 1, 0, 1:  {held}")
    print(f"  gates {counter.gate_count()}, flip-flops {counter.counts()['dff']}, logic depth before the flip-flops: {counter.depth()}")

    print("\n=== Each bit divides the clock by two again ===")
    counter = sync_counter(4)
    trace = [counter.step({"en": 1}) for _ in range(16)]
    for i in range(4):
        wave = "".join("‾" if row[f"q{i}"] else "_" for row in trace)
        print(f"  q{i} {wave}   period {2 ** (i + 1):2d} clock cycles, f = f_clk / {2 ** (i + 1)}")
    f_clk = 16e6
    print(f"  with a 16 MHz clock: q0 = {f_clk / 2 / 1e6:.0f} MHz, q3 = {f_clk / 16 / 1e6:.0f} MHz")

    print("\n=== Decade counter: synchronous reset when the count is 9 ===")
    dec = decade_counter()
    seq = [count(dec.step({"en": 1}), 4) for _ in range(23)]
    print(f"  {seq}")
    print("  9 = 1001 is the only count 0..9 with q3 = q0 = 1, so 'nine = q3·q0' is enough to detect it")

    print("\n=== A ripple counter going from 7 to 8, 10 ns per flip-flop ===")
    for time, value in ripple_counter_events(7):
        print(f"  t = {time:2d} ns: count reads {value:2d} ({value:04b})")
    print("  the outputs pass through 6, 4 and 0 before settling at 8: never decode a ripple counter while it ripples")
    worst = 4 * 10
    print(f"  settling time grows with the number of bits: 4 x 10 ns = {worst} ns; the synchronous counter settles in one tcq")


if __name__ == "__main__":
    main()
