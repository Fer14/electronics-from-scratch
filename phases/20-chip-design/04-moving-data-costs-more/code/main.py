from sim import cost

ENERGY_PJ_45NM = [
    ("8-bit integer add", 0.03),
    ("32-bit integer add", 0.1),
    ("8-bit integer multiply", 0.2),
    ("32-bit integer multiply", 3.1),
    ("16-bit float multiply", 1.1),
    ("32-bit float multiply", 3.7),
    ("64-bit read, 8 KB SRAM", 10.0),
    ("64-bit read, 1 MB SRAM", 100.0),
    ("64-bit read, DRAM", 2000.0),
]

PER_BYTE_PJ = {
    "register file": 10.0 / 8 / 4,
    "local SRAM (8 KB)": 10.0 / 8,
    "big SRAM (1 MB)": 100.0 / 8,
    "DRAM": 2000.0 / 8,
}

MAC_PJ = 0.2 + 0.1


def wire_energy_pj(length_mm, bits=1, cap_pf_per_mm=0.2, volts=0.9):
    return bits * cap_pf_per_mm * length_mm * volts ** 2


def energy_per_mac(source, reuse=1):
    return MAC_PJ + 2 * PER_BYTE_PJ[source] / reuse


def main():
    print("Step 1: energy per operation at 45 nm (Horowitz, ISSCC 2014, rounded)")
    for name, pj in ENERGY_PJ_45NM:
        print(f"  {name:26s} {pj:8.2f} pJ  ({pj / 0.2:8.1f}x an 8-bit multiply)")

    print("\nStep 2: the energy of a wire, from C * V^2")
    for mm in (0.01, 0.1, 1.0, 10.0):
        e = wire_energy_pj(mm)
        print(f"  move 1 bit {mm:5.2f} mm: {e:7.4f} pJ   move 8 bits: {wire_energy_pj(mm, 8):7.3f} pJ")
    print(f"  an 8-bit multiply (0.2 pJ) costs the same as moving one byte about"
          f" {0.2 / wire_energy_pj(1.0, 8):.2f} mm")

    print("\nStep 3: area of fetching operands vs area of computing (sim.cost, 8-bit data)")
    mac = cost.mac(8)
    print(f"  one 8-bit MAC: {mac.area:.0f} gates")
    for words in (8, 32, 128):
        rf = cost.register_file(words, 8)
        second_port = cost.mux(words, 8)
        total = rf.area + second_port.area
        print(f"  register file {words:3d} x 8 bits with 2 read ports: {total:6.0f} gates"
              f" ({total / mac.area:4.1f} MACs worth), read delay {rf.delay} gate delays")

    print("\nStep 4: energy per MAC depending on where both operands come from")
    for source in PER_BYTE_PJ:
        e = energy_per_mac(source)
        print(f"  {source:18s}: {e:8.2f} pJ per MAC ({(e - MAC_PJ) / e * 100:5.1f}% spent moving data)")

    print("\nStep 5: reuse rescues the expensive levels")
    for reuse in (1, 16, 256, 4096):
        print(f"  each byte used {reuse:5d} times: DRAM {energy_per_mac('DRAM', reuse):8.3f} pJ per MAC,"
              f" big SRAM {energy_per_mac('big SRAM (1 MB)', reuse):6.3f} pJ per MAC")

    print("\nStep 6: the same story in sim.cost energy units")
    for name, source in (("operands from SRAM", cost.sram(64 * 1024, width=16)), ("operands from DRAM", cost.dram(width=16))):
        d = cost.Design(name)
        d.add("fetch", source, "mem", "operands")
        d.add("mac", cost.mac(8), "operands", "acc")
        print(f"  {name}: fetch {source.energy:6.1f} + MAC {d.blocks['mac'][0].energy:5.1f}"
              f" = {d.energy():6.1f} units per MAC, latency {d.latency()} cycles")


if __name__ == "__main__":
    main()
