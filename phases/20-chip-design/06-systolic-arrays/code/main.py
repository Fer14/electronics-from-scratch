import numpy as np

from sim import cost


def systolic_matmul(x, w, trace_cycles=0):
    batch, k_dim = x.shape
    _, n_dim = w.shape
    x_reg = np.zeros((k_dim, n_dim), dtype=np.int64)
    p_reg = np.zeros((k_dim, n_dim), dtype=np.int64)
    y = np.zeros((batch, n_dim), dtype=np.int64)
    cycles = batch + k_dim + n_dim - 2
    busy = 0
    for t in range(cycles):
        new_x = np.zeros_like(x_reg)
        new_p = np.zeros_like(p_reg)
        for k in range(k_dim):
            for j in range(n_dim):
                if j == 0:
                    b = t - k
                    x_in = x[b, k] if 0 <= b < batch else 0
                    active = 0 <= b < batch
                else:
                    x_in = x_reg[k, j - 1]
                    active = 0 <= t - k - j < batch
                p_in = p_reg[k - 1, j] if k > 0 else 0
                new_x[k, j] = x_in
                new_p[k, j] = p_in + w[k, j] * x_in
                busy += active
        x_reg, p_reg = new_x, new_p
        for j in range(n_dim):
            b = t - (k_dim - 1) - j
            if 0 <= b < batch:
                y[b, j] = p_reg[k_dim - 1, j]
        if t < trace_cycles:
            cells = []
            for k in range(k_dim):
                row = []
                for j in range(n_dim):
                    b = t - k - j
                    row.append(f"x{b}{k}" if 0 <= b < batch else " . ")
                cells.append(" ".join(row))
            print(f"  cycle {t}: " + "  |  ".join(cells))
    return y, cycles, busy


def main():
    rng = np.random.default_rng(3)

    print("Step 1: a 3 x 3 weight-stationary array, watching the inputs flow (row by row)")
    x_small = rng.integers(0, 5, size=(4, 3))
    w_small = rng.integers(0, 5, size=(3, 3))
    y_small, cycles, busy = systolic_matmul(x_small, w_small, trace_cycles=6)
    print(f"  systolic result:\n{y_small}")
    print(f"  numpy x @ w:\n{x_small @ w_small}")
    print(f"  equal: {np.array_equal(y_small, x_small @ w_small)}, {cycles} cycles")

    print("\nStep 2: a bigger check, 16 x 16 array, batch 64, 8-bit numbers")
    x = rng.integers(0, 256, size=(64, 16))
    w = rng.integers(0, 256, size=(16, 16))
    y, cycles, busy = systolic_matmul(x, w)
    print(f"  equal to numpy: {np.array_equal(y, x @ w)}")
    print(f"  {cycles} cycles, {busy} useful MACs, utilization {busy / (cycles * 16 * 16) * 100:.1f}%")

    print("\nStep 3: utilization grows with the batch (16 x 16 array)")
    for batch in (1, 16, 64, 256, 1024):
        cycles = batch + 16 + 16 - 2
        print(f"  batch {batch:5d}: {cycles:5d} cycles, utilization {batch * 256 / (cycles * 256) * 100:5.1f}%")

    print("\nStep 4: compute grows with the area, input and output only with the edge")
    print(f"  {'N':>4s} {'MACs/cycle':>11s} {'values in+out/cycle':>20s} {'MACs per value moved':>21s}")
    for n in (4, 16, 64, 128, 256):
        print(f"  {n:4d} {n * n:11d} {2 * n:20d} {n * n / (2 * n):21.0f}")

    print("\nStep 5: area and throughput from sim.cost")
    for n in (8, 32, 128, 256):
        array = cost.systolic_array(n, n, 8)
        d = cost.Design(f"{n}x{n}")
        d.add("ARRAY", array, "in", "out")
        peak = d.throughput() * d.max_clock_mhz() * 1e6
        print(f"  {n:3d} x {n:<3d}: {array.area / 1e6:7.2f} M gates, {d.throughput():6.0f} MACs/cycle,"
              f" clock {d.max_clock_mhz():4.0f} MHz -> {peak / 1e12:6.2f} TMAC/s")

    print("\nStep 6: the alternative, every MAC fetching both operands from a shared register file")
    for n in (8, 32):
        macs = n * n
        ports = 2 * macs
        rf = cost.register_file(256, 8).area + (ports - 1) * cost.mux(256, 8).area
        array = cost.systolic_array(n, n, 8).area
        print(f"  {macs:5d} MACs: register file with {ports} read ports = {rf / 1e6:6.2f} M gates"
              f" vs the whole systolic array {array / 1e6:5.2f} M gates")


if __name__ == "__main__":
    main()
