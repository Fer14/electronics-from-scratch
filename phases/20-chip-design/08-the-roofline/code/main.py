from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim.lab import evaluate, load_task

PEAK_FLOPS = 400e12
BANDWIDTH = 2e12
BYTES_PER_VALUE = 2


def attainable(intensity):
    return np.minimum(PEAK_FLOPS, BANDWIDTH * np.asarray(intensity, dtype=float))


def matmul_counts(batch, d_in, d_out):
    flops = 2 * batch * d_in * d_out
    moved = BYTES_PER_VALUE * (d_in * d_out + batch * d_in + batch * d_out)
    return flops, moved


def layer_step(batch, d=8192):
    flops, moved = matmul_counts(batch, d, d)
    compute_s = flops / PEAK_FLOPS
    memory_s = moved / BANDWIDTH
    return flops / moved, compute_s, memory_s, max(compute_s, memory_s)


def main():
    ridge = PEAK_FLOPS / BANDWIDTH
    print("Step 1: the THOTH-1 roofline")
    print(f"  peak compute {PEAK_FLOPS / 1e12:.0f} TFLOP/s, memory bandwidth {BANDWIDTH / 1e12:.0f} TB/s")
    print(f"  ridge point = {PEAK_FLOPS / 1e12:.0f}e12 / {BANDWIDTH / 1e12:.0f}e12 = {ridge:.0f} FLOP per byte")
    for intensity in (1, 10, 100, 200, 1000):
        print(f"  intensity {intensity:5d} FLOP/byte -> at most {attainable(intensity) / 1e12:6.1f} TFLOP/s")

    print("\nStep 2: arithmetic intensity of common operations (bf16)")
    operations = {}
    n = 8192
    operations["add two vectors"] = (n, 3 * BYTES_PER_VALUE * n)
    operations["matrix x vector (batch 1)"] = matmul_counts(1, n, n)
    operations["matrix x 64 vectors"] = matmul_counts(64, n, n)
    operations["matrix x 1024 vectors"] = matmul_counts(1024, n, n)
    operations["square matmul 8192^3"] = matmul_counts(n, n, n)
    context, heads_dim = 4096, 8192
    kv_bytes = 2 * context * heads_dim * BYTES_PER_VALUE
    operations["attention decode, one sequence"] = (4 * context * heads_dim, kv_bytes)
    for name, (flops, moved) in operations.items():
        intensity = flops / moved
        bound = "compute" if intensity >= ridge else "memory"
        print(f"  {name:32s}: {intensity:8.1f} FLOP/byte -> {attainable(intensity) / 1e12:6.1f} TFLOP/s ({bound}-bound)")

    print("\nStep 3: one 8192 x 8192 layer, sweeping the batch")
    print(f"  {'batch':>6s} {'FLOP/byte':>10s} {'compute':>9s} {'memory':>9s} {'step':>9s} {'inputs/s':>12s} {'bound':>8s}")
    for batch in (1, 8, 32, 128, 210, 256, 512, 1024):
        intensity, compute_s, memory_s, step_s = layer_step(batch)
        bound = "compute" if compute_s >= memory_s else "memory"
        print(f"  {batch:6d} {intensity:10.1f} {compute_s * 1e6:7.1f}us {memory_s * 1e6:7.1f}us"
              f" {step_s * 1e6:7.1f}us {batch / step_s:12,.0f} {bound:>8s}")

    print("\nStep 4: the smallest batch that is compute-bound")
    batch = 1
    while layer_step(batch)[1] < layer_step(batch)[2]:
        batch += 1
    intensity, compute_s, memory_s, step_s = layer_step(batch)
    print(f"  batch {batch}: intensity {intensity:.1f} FLOP/byte, step {step_s * 1e6:.1f} us")

    print("\nStep 5: the roofline plot")
    x = np.logspace(-1, 4, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(x, attainable(x) / 1e12, color="black")
    for name, (flops, moved) in operations.items():
        intensity = flops / moved
        ax.scatter([intensity], [attainable(intensity) / 1e12], s=18)
        ax.annotate(name, (intensity, attainable(intensity) / 1e12), fontsize=6, xytext=(3, -8), textcoords="offset points")
    ax.axvline(ridge, linestyle=":", color="gray")
    ax.set_xlabel("arithmetic intensity (FLOP per byte)")
    ax.set_ylabel("attainable TFLOP/s")
    ax.set_title("THOTH-1 roofline")
    out = Path(__file__).parent / "out.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"  saved {out.name}")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        results = evaluate(task, {"S1": part})
        verdict = "PASS" if all(r["passed"] for r in results) else "fail"
        print(f"  {part['label']:10s}: layer step {results[0]['value']:.0f} us -> {verdict}")


if __name__ == "__main__":
    main()
