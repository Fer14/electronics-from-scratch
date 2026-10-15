import math

import numpy as np

from sim import cost

FORMATS = {
    "fp32": (8, 23, 3.4028235e38),
    "fp16": (5, 10, 65504.0),
    "bf16": (8, 7, 3.3895314e38),
    "fp8 E5M2": (5, 2, 57344.0),
    "fp8 E4M3": (4, 3, 448.0),
    "fp4 E2M1": (2, 1, 6.0),
}


def quantize_float(x, exp_bits, man_bits, max_value):
    bias = 2 ** (exp_bits - 1) - 1
    min_exp = 1 - bias
    x = np.clip(np.asarray(x, dtype=np.float64), -max_value, max_value)
    mag = np.abs(x)
    exponent = np.floor(np.log2(np.where(mag > 0, mag, 1.0)))
    exponent = np.maximum(exponent, min_exp)
    step = 2.0 ** (exponent - man_bits)
    return np.clip(np.round(x / step) * step, -max_value, max_value)


def quantize_int(x, bits):
    levels = 2 ** (bits - 1) - 1
    scale = np.max(np.abs(x)) / levels
    return np.round(x / scale) * scale


def snr_db(reference, approx):
    noise = np.mean((reference - approx) ** 2)
    return 10 * math.log10(np.mean(reference ** 2) / noise)


def float_multiplier_area(exp_bits, man_bits):
    return cost.multiplier(man_bits + 1).area + cost.adder(exp_bits).area


def archetype(name, blocks):
    d = cost.Design(name)
    node = "in"
    for i, (label, block) in enumerate(blocks):
        d.add(label, block, node, f"n{i}")
        node = f"n{i}"
    return d


def main():
    print("Step 1: where three kinds of chip spend their area (sim.cost blocks, illustrative)")
    cpu = archetype("CPU core", [
        ("4 x 64-bit multipliers", cost.gates(4 * cost.multiplier(64).area, 0)),
        ("4 x 64-bit adders", cost.gates(4 * cost.adder(64).area, 0)),
        ("register file 180 x 64, 8 ports", cost.gates(6 * 180 * 64 + 8 * cost.mux(180, 64).area, 0)),
        ("caches 32 KB + 32 KB + 512 KB", cost.sram(8 * (64 + 512) * 1024)),
        ("branch prediction, reorder, decode", cost.gates(400_000, 0)),
    ])
    gpu = archetype("GPU multiprocessor", [
        ("128 fp32 multiply-add lanes", cost.gates(128 * (float_multiplier_area(8, 23) + cost.adder(32).area), 0)),
        ("register file 256 KB", cost.sram(256 * 1024 * 8)),
        ("shared memory / L1 128 KB", cost.sram(128 * 1024 * 8)),
        ("schedulers and control", cost.gates(200_000, 0)),
    ])
    tpu = archetype("matrix accelerator", [
        ("128 x 128 array of bf16 MACs", cost.gates(128 * 128 * (float_multiplier_area(8, 7) + cost.adder(32).area + 6 * 32), 0)),
        ("on-chip buffer 4 MB", cost.sram(4 * 1024 * 1024 * 8)),
        ("control and DMA", cost.gates(100_000, 0)),
    ])
    for design, macs in ((cpu, 4), (gpu, 128), (tpu, 128 * 128)):
        total = design.area()
        print(f"  {design.name}: {total / 1e6:7.1f} M gates, {macs} multiply-adds per cycle,"
              f" {macs / (total / 1e6):8.1f} per M gates")
        for label, (block, _, _) in design.blocks.items():
            print(f"     {label:38s} {block.area / total * 100:5.1f}%")

    print("\nStep 2: number formats (exponent bits, mantissa bits, largest value)")
    for name, (e, m, top) in FORMATS.items():
        print(f"  {name:9s}: {1 + e + m:2d} bits = 1 sign + {e} exponent + {m:2d} mantissa,"
              f" max {top:.4g}, relative step {2.0 ** -m:.4f}")

    rng = np.random.default_rng(11)
    weights = rng.normal(0.0, 0.02, size=20000)
    print("\nStep 3: rounding 20,000 weights (normal, std 0.02) to each format")
    for name, (e, m, top) in FORMATS.items():
        if name == "fp32":
            continue
        plain = quantize_float(weights, e, m, top)
        scale = top / np.max(np.abs(weights))
        scaled = quantize_float(weights * scale, e, m, top) / scale
        print(f"  {name:9s}: SNR {snr_db(weights, plain):6.1f} dB as is, {snr_db(weights, scaled):6.1f} dB with a per-tensor scale")
    for bits in (8, 4):
        print(f"  int{bits}     : SNR {snr_db(weights, quantize_int(weights, bits)):6.1f} dB with a per-tensor scale")

    print("\nStep 3b: activations with rare large outliers (1 in 200 values is 50x bigger)")
    acts = rng.normal(0.0, 1.0, size=20000)
    acts[::200] *= 50
    e, m, top = FORMATS["fp8 E4M3"]
    scale = top / np.max(np.abs(acts))
    fp8 = quantize_float(acts * scale, e, m, top) / scale
    print(f"  fp8 E4M3 with a per-tensor scale: SNR {snr_db(acts, fp8):5.1f} dB,"
          f" ordinary values {snr_db(acts[1::200], fp8[1::200]):5.1f} dB")
    int8 = quantize_int(acts, 8)
    print(f"  int8 with a per-tensor scale    : SNR {snr_db(acts, int8):5.1f} dB,"
          f" ordinary values {snr_db(acts[1::200], int8[1::200]):5.1f} dB")

    print("\nStep 4: multiplier area grows with the mantissa squared")
    base = float_multiplier_area(8, 23)
    for name, (e, m, _) in FORMATS.items():
        area = float_multiplier_area(e, m)
        print(f"  {name:9s}: {area:6.0f} gates, {base / area:6.1f} times as many per area as fp32")
    print(f"  int8     : {cost.multiplier(8).area:6.0f} gates, {base / cost.multiplier(8).area:6.1f} times as many per area as fp32")

    print("\nStep 5: why accumulators stay wide (sum of 4096 products)")
    x = rng.normal(0.0, 1.0, size=4096)
    w = rng.normal(0.0, 1.0, size=4096)
    exact = float(np.dot(x, w))
    e, m, top = FORMATS["bf16"]
    acc_bf16 = 0.0
    for xi, wi in zip(x, w):
        acc_bf16 = float(quantize_float(acc_bf16 + xi * wi, e, m, top))
    acc_fp32 = float(np.sum((x * w).astype(np.float32), dtype=np.float32))
    print(f"  exact {exact:9.4f}, fp32 accumulator {acc_fp32:9.4f}, bf16 accumulator {acc_bf16:9.4f}")
    print(f"  error: fp32 {abs(acc_fp32 - exact):.2e}, bf16 {abs(acc_bf16 - exact):.2e}")


if __name__ == "__main__":
    main()
