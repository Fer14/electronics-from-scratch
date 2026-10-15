import math

from sim import Circuit

RHO_COPPER = 1.72e-8

PROCESS = [
    ("cut the copper-clad laminate to panel size", "inner and outer layers start as FR-4 with copper on both faces"),
    ("drill", "every via and through-hole, by CNC drill or laser for tiny vias"),
    ("plate the holes", "a thin chemical copper seed, then electroplating to about 25 um"),
    ("image", "photoresist film exposed to the layer pattern with UV light"),
    ("etch", "unprotected copper dissolved away, leaving traces and pads"),
    ("solder mask", "green (or other colour) varnish everywhere except pads"),
    ("silkscreen", "white legend: references, outlines, polarity marks"),
    ("surface finish", "HASL solder, ENIG gold or OSP protects the bare pads"),
    ("electrical test", "flying probes or a bed of nails check every net for opens and shorts"),
    ("rout the outline", "a milling bit cuts each board out of the panel"),
]


def boards_per_panel(board_w, board_h, panel_w=457.0, panel_h=610.0, margin=10.0, spacing=2.0):
    usable_w = panel_w - 2 * margin
    usable_h = panel_h - 2 * margin
    best = 0
    for w, h in ((board_w, board_h), (board_h, board_w)):
        across = int((usable_w + spacing) // (w + spacing))
        down = int((usable_h + spacing) // (h + spacing))
        best = max(best, across * down)
    return best


def order_cost(quantity, board_w, board_h, layers=2, setup=30.0, per_cm2=0.012):
    area_cm2 = board_w * board_h / 100
    layer_factor = {2: 1.0, 4: 2.2, 6: 3.5}[layers]
    return setup * layer_factor + quantity * area_cm2 * per_cm2 * layer_factor


def board_yield(board_w, board_h, defects_per_dm2):
    area_dm2 = board_w * board_h / 1e4
    return math.exp(-defects_per_dm2 * area_dm2)


def etched_width(drawn_width_um, copper_um=35.0, etch_factor=3.0):
    undercut_each_side = copper_um / etch_factor
    return drawn_width_um - 2 * undercut_each_side


def via_resistance(drill_m=0.3e-3, plating_m=25e-6, length_m=1.6e-3):
    barrel_area = math.pi * (drill_m - plating_m) * plating_m
    return RHO_COPPER * length_m / barrel_area


def current_through_vias(count, amps=3.0):
    r_via = via_resistance()
    c = Circuit()
    c.current_source("I1", "0", "top", amps)
    for n in range(count):
        c.resistor(f"VIA{n + 1}", "top", "0", r_via)
    r = c.dc()
    return r.v("top"), r.i("VIA1"), r.p("VIA1")


def main():
    print("Step 1: the fabrication sequence of a 2-layer board")
    for n, (step, detail) in enumerate(PROCESS, start=1):
        print(f"  {n:2d}. {step:44s} {detail}")

    print("\nStep 2: boards per 457 x 610 mm production panel")
    for w, h in ((50, 50), (100, 80), (160, 100), (23, 17)):
        count = boards_per_panel(w, h)
        used = count * w * h / (457 * 610) * 100
        print(f"  {w:3d} x {h:3d} mm board: {count:4d} per panel, {used:4.1f}% of the panel area")

    print("\nStep 3: price per board falls with quantity (50 x 50 mm, toy price model)")
    for layers in (2, 4):
        for quantity in (5, 50, 500, 5000):
            total = order_cost(quantity, 50, 50, layers)
            print(f"  {layers} layers, {quantity:5d} boards: total ${total:8.2f}, ${total / quantity:6.3f} each")

    print("\nStep 4: bare-board yield with 0.05 defects per square decimetre")
    for w, h in ((50, 50), (100, 100), (200, 200)):
        y = board_yield(w, h, 0.05)
        print(f"  {w:3d} x {h:3d} mm: yield {y * 100:5.1f}%")

    print("\nStep 5: etching eats the edges (etch factor 3)")
    for drawn in (100, 150, 200):
        for copper in (35, 70):
            final = etched_width(drawn, copper)
            print(f"  drawn {drawn} um in {copper} um copper -> about {final:5.1f} um after etching")

    print("\nStep 6: plated vias carrying 3 A")
    r_via = via_resistance()
    print(f"  one 0.3 mm via, 25 um plating, 1.6 mm long: {r_via * 1000:.2f} mOhm")
    for count in (1, 2, 4, 8):
        drop, amps, watts = current_through_vias(count)
        print(f"  {count} vias in parallel: drop {drop * 1000:5.2f} mV, {amps:.2f} A and {watts * 1000:5.2f} mW per via")


if __name__ == "__main__":
    main()
