import numpy as np

from sim.logic import LogicCircuit


def regenerate(v, threshold=2.5, vdd=5.0):
    return np.where(v > threshold, vdd, 0.0)


def run_chains(stages, noise_rms, seed=14):
    rng = np.random.default_rng(seed)
    message = np.array([0, 1, 1, 0, 1, 0, 0, 1] * 25)
    sent = message * 5.0
    analog = sent.copy()
    for _ in range(stages):
        analog = analog + rng.normal(0.0, noise_rms, analog.size)
    digital = sent.copy()
    for _ in range(stages):
        digital = regenerate(digital + rng.normal(0.0, noise_rms, digital.size))
    analog_error = np.sqrt(np.mean((analog - sent) ** 2))
    digital_error = np.sqrt(np.mean((digital - sent) ** 2))
    wrong_analog = int(np.sum((analog > 2.5).astype(int) != message))
    wrong_digital = int(np.sum((digital > 2.5).astype(int) != message))
    return analog_error, digital_error, wrong_analog, wrong_digital, message.size


def read_input(v, vil, vih):
    if v <= vil:
        return "0"
    if v >= vih:
        return "1"
    return "undefined"


def buffer_chain(stages):
    lc = LogicCircuit("buffer chain")
    lc.inputs("in")
    previous = "in"
    for k in range(1, stages + 1):
        lc.gate("buf", [previous], f"s{k}")
        previous = f"s{k}"
    lc.outputs(previous)
    return lc


def main():
    print("=== Analog chain vs digital chain ===")
    for stages, noise_rms in [(10, 0.2), (10, 0.5), (10, 1.0)]:
        a_err, d_err, a_wrong, d_wrong, n = run_chains(stages, noise_rms)
        print(f"After {stages} stages with {noise_rms:.2f} V of noise per stage")
        print(f"  analog  chain: typical error {a_err:.2f} V  (theory {noise_rms:.2f} x sqrt({stages}) = {noise_rms * np.sqrt(stages):.2f} V), wrong bits {a_wrong}/{n}")
        print(f"  digital chain: typical error {d_err:.2f} V, wrong bits {d_wrong}/{n}")

    print("\n=== Noise margins ===")
    families = {
        "74HC at 5 V": {"VOH": 4.4, "VOL": 0.1, "VIH": 3.5, "VIL": 1.5},
        "LVCMOS 3.3 V": {"VOH": 2.4, "VOL": 0.4, "VIH": 2.0, "VIL": 0.8},
    }
    for name, lv in families.items():
        nmh = lv["VOH"] - lv["VIH"]
        nml = lv["VIL"] - lv["VOL"]
        print(f"{name:13s}: NMH = {lv['VOH']:.1f} - {lv['VIH']:.1f} = {nmh:.1f} V, NML = {lv['VIL']:.1f} - {lv['VOL']:.1f} = {nml:.1f} V, worst = {min(nmh, nml):.1f} V")
    mixed = families["LVCMOS 3.3 V"]["VOH"] - families["74HC at 5 V"]["VIH"]
    print(f"3.3 V output driving a 5 V 74HC input: NMH = 2.4 - 3.5 = {mixed:.1f} V (negative: not guaranteed)")

    print("\n=== What a 74HC input at 5 V reads ===")
    for v in [0.8, 1.5, 2.5, 3.49, 3.5, 4.0]:
        print(f"  {v:4.2f} V -> {read_input(v, 1.5, 3.5)}")

    print("\n=== Ten buffers in sim.logic ===")
    chain = buffer_chain(10)
    for bit in (0, 1):
        print(f"  in = {bit} -> after 10 buffers: {chain.evaluate({'in': bit})['s10']}")


if __name__ == "__main__":
    main()
