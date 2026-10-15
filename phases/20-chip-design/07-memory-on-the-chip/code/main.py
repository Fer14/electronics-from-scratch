from collections import OrderedDict
from pathlib import Path

from sim import cost
from sim.lab import evaluate, load_task

HIERARCHY = [
    ("flip-flop register", "a few", "< 1 ns", 0.05, "6 gates per bit in our model"),
    ("SRAM 8-64 KB", "KB", "~1 ns", 0.2, "6 transistors per bit"),
    ("SRAM 1-100 MB", "MB", "5-20 ns", 1.5, "same cells, longer wires"),
    ("HBM (stacked DRAM)", "16-24 GB per stack", "~100 ns", 4.0, "1 transistor + 1 capacitor per bit"),
    ("DDR DRAM", "GB", "~100 ns", 25.0, "same cells, off-package wires"),
]

MISS_CYCLES = 100
HIT_CYCLES = 1


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.lines = OrderedDict()
        self.hits = 0
        self.misses = 0

    def access(self, address):
        if address in self.lines:
            self.lines.move_to_end(address)
            self.hits += 1
            return HIT_CYCLES
        self.misses += 1
        self.lines[address] = True
        if len(self.lines) > self.capacity:
            self.lines.popitem(last=False)
        return MISS_CYCLES


def weight_stream_naive(batch, k_dim, n_dim):
    for _ in range(batch):
        for j in range(n_dim):
            for k in range(k_dim):
                yield (k, j)


def weight_stream_tiled(batch, k_dim, n_dim, tile):
    for k0 in range(0, k_dim, tile):
        for j0 in range(0, n_dim, tile):
            for _ in range(batch):
                for j in range(j0, j0 + tile):
                    for k in range(k0, k0 + tile):
                        yield (k, j)


def run_cache(stream, capacity):
    cache = LRUCache(capacity)
    cycles = sum(cache.access(address) for address in stream)
    return cache.hits, cache.misses, cycles


def scratchpad_cycles(batch, k_dim, n_dim, tile, words_per_cycle):
    tiles = (k_dim // tile) * (n_dim // tile)
    load = tile * tile / words_per_cycle
    compute = batch * tile * tile
    return load + tiles * max(load, compute), load, compute


def delivered_macs_per_cycle(array_n, buffer_bits, dram_bytes_per_cycle=2.0):
    weight_bits = array_n * array_n * 8
    per_input_bits = array_n * 8 + array_n * 24
    batch = max((buffer_bits - weight_bits) // per_input_bits, 0)
    peak = array_n * array_n
    if batch == 0:
        return 0, batch
    return min(peak, dram_bytes_per_cycle * batch), batch


def main():
    print("Step 1: the memory hierarchy, orders of magnitude")
    print(f"  {'level':20s} {'size':>20s} {'latency':>9s} {'pJ per bit':>11s}  cell")
    for name, size, latency, pj, cell in HIERARCHY:
        print(f"  {name:20s} {size:>20s} {latency:>9s} {pj:11.2f}  {cell}")

    print("\nStep 2: storing bits as flip-flops or as SRAM (sim.cost)")
    for kbits in (1, 16, 256):
        bits = kbits * 1024
        flops = cost.register(bits).area
        sram = cost.sram(bits).area
        print(f"  {kbits:4d} kbit: flip-flops {flops:9.0f} gates, SRAM {sram:7.0f} gates ({flops / sram:.0f}x smaller)")

    batch, k_dim, n_dim = 16, 64, 64
    print(f"\nStep 3: a hardware cache (LRU, 1024 words) reading the weights of a {k_dim} x {n_dim} layer, batch {batch}")
    for name, stream in (("naive order", weight_stream_naive(batch, k_dim, n_dim)),
                         ("tiled order (32 x 32 tiles)", weight_stream_tiled(batch, k_dim, n_dim, 32))):
        hits, misses, cycles = run_cache(stream, 1024)
        print(f"  {name:28s}: {hits:6d} hits, {misses:6d} misses,"
              f" hit rate {hits / (hits + misses) * 100:5.1f}%, {cycles:8d} cycles")

    print("\nStep 4: a software-managed scratchpad with double buffering (8 words per cycle from DRAM)")
    total, load, compute = scratchpad_cycles(batch, k_dim, n_dim, 32, 8)
    print(f"  each tile: load {load:.0f} cycles, compute {compute:.0f} cycles,"
          f" overlapped -> {total:.0f} cycles in total, the same every run")

    print("\nStep 5: split an area budget of 60,000 gates between the MAC array and its buffer")
    print(f"  {'array':>7s} {'buffer':>8s} {'area':>8s} {'fits':>5s} {'batch held':>11s} {'delivered MACs/cycle':>21s}")
    for n in (4, 8, 16):
        for kbits in (4, 16, 64):
            bits = kbits * 1024
            area = cost.systolic_array(n, n, 8).area + cost.sram(bits).area
            delivered, held = delivered_macs_per_cycle(n, bits)
            fits = "yes" if area <= 60_000 else "no"
            print(f"  {n:3d}x{n:<3d} {kbits:5d} kb {area:8.0f} {fits:>5s} {held:11d} {delivered:21.0f}")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for result in evaluate(task):
        print(f"  {'PASS' if result['passed'] else 'fail'}  {result['label']}: {result['value']:.0f}")


if __name__ == "__main__":
    main()
