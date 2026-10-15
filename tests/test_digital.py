"""Digital checks: logic simulation, flip-flops and the chip cost model."""
from itertools import product

from sim.cost import Design, adder, mac, multiplier, register, systolic_array
from sim.logic import LogicCircuit, array_multiplier, full_adder, ripple_adder


def test_full_adder_truth_table():
    lc = LogicCircuit()
    lc.inputs("a", "b", "cin")
    full_adder(lc, "a", "b", "cin", "s", "cout")
    lc.outputs("s", "cout")
    rows = lc.truth_table()
    assert len(rows) == 8
    for row in rows:
        total = row["a"] + row["b"] + row["cin"]
        assert row["s"] == total % 2 and row["cout"] == total // 2
    assert lc.gate_count() == 5
    assert lc.depth() == 3


def test_all_gates():
    expected = {"and": [0, 0, 0, 1], "or": [0, 1, 1, 1], "nand": [1, 1, 1, 0], "nor": [1, 0, 0, 0],
                "xor": [0, 1, 1, 0], "xnor": [1, 0, 0, 1]}
    for op, column in expected.items():
        lc = LogicCircuit()
        lc.inputs("a", "b")
        lc.gate(op, ["a", "b"], "y")
        lc.outputs("y")
        assert [row["y"] for row in lc.truth_table()] == column, op
    lc = LogicCircuit()
    lc.inputs("a")
    lc.not_("y", "a")
    lc.outputs("y")
    assert [row["y"] for row in lc.truth_table()] == [1, 0]


def test_adders_and_multiplier():
    for bits in (1, 3, 4):
        lc = ripple_adder(bits)
        for x, y in product(range(2 ** bits), repeat=2):
            inputs = {**{f"a{i}": (x >> i) & 1 for i in range(bits)}, **{f"b{i}": (y >> i) & 1 for i in range(bits)}}
            out = lc.evaluate(inputs)
            total = sum(out[f"s{i}"] << i for i in range(bits)) + (out["cout"] << bits)
            assert total == x + y
        assert lc.gate_count() == adder(bits).area
        assert lc.depth() == adder(bits).delay
    for bits in (1, 2, 4, 6):
        lc = array_multiplier(bits)
        assert lc.gate_count() == multiplier(bits).area
        assert lc.depth() == multiplier(bits).delay
        for x, y in product(range(2 ** bits), repeat=2):
            inputs = {**{f"a{i}": (x >> i) & 1 for i in range(bits)}, **{f"b{i}": (y >> i) & 1 for i in range(bits)}}
            out = lc.evaluate(inputs)
            assert sum(out[f"p{k}"] << k for k in range(2 * bits)) == x * y


def test_counter_with_flip_flops():
    lc = LogicCircuit()
    lc.not_("d0", "q0")
    lc.xor("d1", "q1", "q0")
    lc.register("count", ["d0", "d1"], ["q0", "q1"])
    lc.outputs("q1", "q0")
    values = []
    for _ in range(6):
        out = lc.step()
        values.append(out["q1"] * 2 + out["q0"])
    assert values == [1, 2, 3, 0, 1, 2]


def test_sr_latch_remembers():
    lc = LogicCircuit()
    lc.inputs("s", "r")
    lc.nor("q", "r", "qn")
    lc.nor("qn", "s", "q")
    lc.outputs("q")
    assert lc.evaluate({"s": 1, "r": 0})["q"] == 1
    assert lc.evaluate({"s": 0, "r": 0})["q"] == 1
    assert lc.evaluate({"s": 0, "r": 1})["q"] == 0
    assert lc.evaluate({"s": 0, "r": 0})["q"] == 0


def test_event_glitch():
    lc = LogicCircuit()
    lc.inputs("a")
    lc.not_("na", "a")
    lc.and_("y", "a", "na")
    events = lc.events({"a": 0}, {"a": 1})
    ys = [value for time, name, value in events if name == "y"]
    assert ys == [1, 0]


def test_cost_model_sanity():
    assert adder(8).area == 40 and adder(8).delay == 17
    assert multiplier(8).area > 4 * multiplier(4).area * 0.9
    assert multiplier(4).area / multiplier(8).area < 0.3
    d = Design("mac")
    d.add("mult", multiplier(8), "in", "p")
    d.add("acc", adder(24), "p", "sum")
    d.add("reg", register(24), "sum", "out")
    assert d.area() == multiplier(8).area + adder(24).area + register(24).area
    assert d.critical_path() == multiplier(8).delay + adder(24).delay
    assert d.latency() == 1
    piped = Design("pipelined")
    piped.add("mult", multiplier(8), "in", "p")
    piped.add("cut", register(16), "p", "q")
    piped.add("acc", adder(24), "q", "sum")
    piped.add("reg", register(24), "sum", "out")
    assert piped.critical_path() == max(multiplier(8).delay, adder(24).delay)
    assert piped.latency() == 2
    assert piped.area() > d.area()
    assert piped.max_clock_mhz() > d.max_clock_mhz()
    loop = Design("accumulator")
    loop.add("acc", adder(16), "x", "sum")
    loop.add("reg", register(16), "sum", "x")
    assert loop.critical_path() == adder(16).delay
    small, big = systolic_array(4, 4, 8), systolic_array(8, 8, 8)
    assert big.area == 4 * small.area and big.ops == 64
    assert big.delay == mac(8).delay
    assert "critical path" in d.report()
