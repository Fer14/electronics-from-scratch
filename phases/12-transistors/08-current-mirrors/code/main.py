from sim import Circuit

SUPPLY = 5.0


def bjt_mirror(reference_ohms, load_ohms, beta=100.0, output_area=1.0, supply=SUPPLY):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", supply)
    circuit.resistor("RREF", "vcc", "x", reference_ohms)
    circuit.npn("Q1", c="x", b="x", e="0", beta=beta)
    circuit.npn("Q2", c="out", b="x", e="0", beta=beta, Is=1e-14 * output_area)
    circuit.resistor("RL", "vcc", "out", load_ohms)
    return circuit.dc()


def show_basic():
    result = bjt_mirror(4700.0, 2200.0)
    reference = result.i("RREF")
    output = result.i("Q2")
    print("Basic NPN mirror: R_REF = 4.7 kohm from 5 V into a diode-connected Q1, Q2 copies its current")
    print(f"  V_BE (shared) = {result.v('x'):.4f} V")
    print(f"  I_REF = (5 - V_BE) / 4.7k = {reference * 1000:.4f} mA")
    print(f"  I_OUT = {output * 1000:.4f} mA   ratio {output / reference:.4f}   (formula beta / (beta + 2) = {100 / 102:.4f})")
    print()


def show_load_independence():
    print("The output current does not care about the load, until the load asks for too much voltage")
    print(f"  {'R_load':>8} {'I_OUT':>10} {'V_CE(Q2)':>9}")
    for load in [100.0, 1000.0, 2200.0, 4300.0, 4700.0, 5600.0, 10000.0]:
        result = bjt_mirror(4700.0, load)
        print(f"  {load:>7.0f}  {result.i('Q2') * 1000:>8.4f}mA {result.v('out'):>8.3f}V")
    print("  Compliance: Q2 needs V_CE above about 0.2 V. Beyond R_L of about 5 kohm it saturates and the current drops.")
    print()


def show_beta_effect():
    print("Effect of beta (the two base currents are stolen from I_REF)")
    for beta in [20.0, 50.0, 100.0, 300.0]:
        result = bjt_mirror(4700.0, 2200.0, beta=beta)
        print(f"  beta {beta:>4.0f}: I_OUT / I_REF = {result.i('Q2') / result.i('RREF'):.4f}   formula {beta / (beta + 2):.4f}")
    print()


def show_ratio():
    print("Scaling: make Q2's emitter area N times bigger and it carries N times the current")
    for area in [1.0, 2.0, 4.0]:
        result = bjt_mirror(4700.0, 1000.0, output_area=area)
        print(f"  area x{area:.0f}: I_OUT / I_REF = {result.i('Q2') / result.i('RREF'):.3f}")
    print()


def show_supply_change():
    print("A mirror copies I_REF, so I_OUT follows the supply through R_REF")
    for supply in [4.5, 5.0, 5.5]:
        result = bjt_mirror(4700.0, 2200.0, supply=supply)
        print(f"  supply {supply:.1f} V: I_OUT = {result.i('Q2') * 1000:.4f} mA")
    print()


def mosfet_mirror(load_ohms, lam):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", SUPPLY)
    circuit.resistor("RREF", "vdd", "x", 10e3)
    circuit.nmos("M1", d="x", g="x", s="0", vth=0.7, k=2e-3, lam=lam)
    circuit.nmos("M2", d="out", g="x", s="0", vth=0.7, k=2e-3, lam=lam)
    circuit.resistor("RL", "vdd", "out", load_ohms)
    return circuit.dc()


def show_mosfet_mirror():
    print("MOSFET mirror (V_th 0.7 V, k 2 mA/V^2, R_REF 10 kohm): no gate current, so no beta error")
    for lam in [0.0, 0.05]:
        cells = []
        for load in [100.0, 2000.0, 5000.0]:
            result = mosfet_mirror(load, lam)
            cells.append(f"R_L {load:>5.0f}: {result.i('M2') * 1e6:7.2f} uA")
        reference = mosfet_mirror(100.0, lam).i("RREF")
        print(f"  lambda {lam:.2f} (I_REF {reference * 1e6:.2f} uA)   " + "   ".join(cells))
    print("  With lambda > 0 (channel-length modulation) the copy depends on V_DS: a finite output resistance.")


def main():
    show_basic()
    show_load_independence()
    show_beta_effect()
    show_ratio()
    show_supply_change()
    show_mosfet_mirror()


if __name__ == "__main__":
    main()
