from itertools import product
from pathlib import Path

from sim import cost
from sim.lab import evaluate, load_task
from sim.logic import LogicCircuit

FUNCTIONS = {
    "majority": lambda a, b, c: int(a + b + c >= 2),
    "xor3 (sum bit)": lambda a, b, c: a ^ b ^ c,
    "a AND b, OR c": lambda a, b, c: (a & b) | c,
}


def add_mux(lc, tag, x0, x1, sel, out):
    lc.and_(f"{tag}.x0", x0, f"n_{sel}")
    lc.and_(f"{tag}.x1", x1, sel)
    lc.or_(out, f"{tag}.x0", f"{tag}.x1")


def build_lut(k):
    lc = LogicCircuit(f"LUT{k}")
    names = [f"i{n}" for n in range(k)]
    lc.inputs(*names)
    for name in names:
        lc.not_(f"n_{name}", name)
    level = [f"cfg{i}" for i in range(2 ** k)]
    for depth, sel in enumerate(reversed(names)):
        nxt = []
        for m in range(len(level) // 2):
            out = f"L{depth}_{m}" if len(level) > 2 else "out"
            add_mux(lc, f"M{depth}_{m}", level[2 * m], level[2 * m + 1], sel, out)
            nxt.append(out)
        level = nxt
    lc.outputs("out")
    return lc


def configure(lc, k, function):
    for i, bits in enumerate(product((0, 1), repeat=k)):
        lc.constant(f"cfg{i}", function(*bits))


def lut_area(k):
    muxes = 2 ** k - 1
    return 3 * muxes + k + cost.FLOP_AREA * 2 ** k


def break_even(nre_asic, unit_asic, nre_fpga, unit_fpga):
    return (nre_asic - nre_fpga) / (unit_fpga - unit_asic)


def main():
    print("Step 1: one 3-input LUT configured three ways")
    for name, function in FUNCTIONS.items():
        lut = build_lut(3)
        configure(lut, 3, function)
        wrong = sum(1 for bits in product((0, 1), repeat=3)
                    if lut.evaluate(dict(zip(("i0", "i1", "i2"), bits)))["out"] != function(*bits))
        config = "".join(str(function(*bits)) for bits in product((0, 1), repeat=3))
        print(f"  {name:16s}: configuration bits {config}, {8 - wrong} of 8 rows right")

    print("\nStep 2: the area of one LUT in our model (multiplexers + input inverters + configuration flip-flops)")
    for k in (3, 4, 6):
        lut = build_lut(k)
        print(f"  LUT{k}: {lut.gate_count():3d} gates of logic + {2 ** k:2d} configuration bits"
              f" = {lut_area(k):4.0f} gates, depth {lut.depth()} gate delays")

    print("\nStep 3: a 4-bit adder, in LUTs or in direct gates")
    luts = 4 * 2
    print(f"  LUT version: {luts} LUT3s (a sum and a carry per bit) = {luts * lut_area(3):.0f} gates")
    print(f"  direct gates (ripple adder): {cost.adder(4).area:.0f} gates")
    print(f"  ratio before counting routing: {luts * lut_area(3) / cost.adder(4).area:.1f}x")
    routing_factor = 3
    print(f"  with programmable routing about {routing_factor}x the logic area:"
          f" {luts * lut_area(3) * routing_factor / cost.adder(4).area:.0f}x")

    print("\nStep 4: what measurements found (Kuon and Rose, 2007, 90 nm FPGA vs standard-cell ASIC)")
    for what, factor in (("area, logic only", "about 35x"), ("area, using hard multipliers and memories", "about 18x"),
                         ("critical path delay", "about 3-4x"), ("dynamic power", "about 14x")):
        print(f"  {what:42s} {factor}")

    print("\nStep 5: when does a custom chip pay off? (toy prices)")
    nre_asic, unit_asic = 3_000_000, 4.0
    nre_fpga, unit_fpga = 20_000, 60.0
    volume = break_even(nre_asic, unit_asic, nre_fpga, unit_fpga)
    print(f"  ASIC: ${nre_asic:,.0f} up front, ${unit_asic:.2f} per chip; FPGA: ${nre_fpga:,.0f} up front, ${unit_fpga:.2f} per chip")
    print(f"  break-even volume = {volume:,.0f} units")
    for units in (1_000, 10_000, 100_000, 1_000_000):
        asic = nre_asic + unit_asic * units
        fpga = nre_fpga + unit_fpga * units
        cheaper = "ASIC" if asic < fpga else "FPGA"
        print(f"  {units:>9,d} units: ASIC ${asic / units:9.2f} each, FPGA ${fpga / units:7.2f} each -> {cheaper}")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for result in evaluate(task):
        print(f"  {'PASS' if result['passed'] else 'fail'}  {result['label']}: {result['value']} wrong rows")


if __name__ == "__main__":
    main()
