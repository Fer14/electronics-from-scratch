import random

from sim.logic import LogicCircuit

WORDS = 16
ADDR_BITS = 4
BITS = 8


def build_ram():
    lc = LogicCircuit("16 x 8 RAM")
    addr = [f"addr{k}" for k in range(ADDR_BITS)]
    din = [f"din{i}" for i in range(BITS)]
    lc.inputs(*addr, *din, "we")
    for k in range(ADDR_BITS):
        lc.not_(f"naddr{k}", addr[k])
    for w in range(WORDS):
        literals = [addr[k] if (w >> k) & 1 else f"naddr{k}" for k in range(ADDR_BITS)]
        lc.and_(f"sel{w}", *literals)
        lc.and_(f"wen{w}", f"sel{w}", "we")
        lc.register(f"word{w}", din, [f"m{w}_{i}" for i in range(BITS)], enable=f"wen{w}")
    for i in range(BITS):
        for w in range(WORDS):
            lc.and_(f"rd{w}_{i}", f"m{w}_{i}", f"sel{w}")
        lc.or_(f"dout{i}", *[f"rd{w}_{i}" for w in range(WORDS)])
    lc.outputs(*[f"dout{i}" for i in range(BITS)])
    return lc


def access(ram, address, data=0, write=0):
    inputs = {f"addr{k}": (address >> k) & 1 for k in range(ADDR_BITS)}
    inputs.update({f"din{i}": (data >> i) & 1 for i in range(BITS)})
    inputs["we"] = write
    if write:
        ram.step(inputs)
    out = ram.evaluate(inputs)
    return sum(out[f"dout{i}"] << i for i in range(BITS))


class Memory:
    def __init__(self, size=256):
        self.cells = [0] * size

    def read(self, address):
        return self.cells[address & 0xFF]

    def write(self, address, value):
        self.cells[address & 0xFF] = value & 0xFF


def main():
    ram = build_ram()
    counts = ram.counts()
    print("=== A 16-byte RAM from flip-flops, a decoder and multiplexers ===")
    print(f"  flip-flops: {counts['dff']} (16 words x 8 bits)")
    print(f"  gates: {ram.gate_count()} ({counts['not']} NOT, {counts['and']} AND, {counts['or']} OR)")
    print(f"  read path depth: {ram.depth()} gate delays (decoder AND, read AND, 16-input OR)")

    print("\n=== Write a few bytes, then read them back ===")
    for address, value in [(3, 42), (7, 200), (15, 0x5A), (0, 1)]:
        access(ram, address, value, write=1)
        print(f"  write {value:3d} to address {address:2d}")
    for address in [0, 3, 7, 8, 15]:
        print(f"  read address {address:2d} -> {access(ram, address)}")
    access(ram, 3, 99, write=1)
    print(f"  overwrite address 3 with 99, read back -> {access(ram, 3)}; address 7 still -> {access(ram, 7)}")

    print("\n=== Random test against a Python list ===")
    rng = random.Random(3)
    model = [0] * WORDS
    for address in range(WORDS):
        access(ram, address, 0, write=1)
    wrong = 0
    for _ in range(200):
        address = rng.randrange(WORDS)
        if rng.random() < 0.5:
            value = rng.randrange(256)
            access(ram, address, value, write=1)
            model[address] = value
        else:
            wrong += access(ram, address) != model[address]
    print(f"  200 random reads and writes: {wrong} mismatches")

    print("\n=== How memory grows ===")
    for words in [16, 256, 65536]:
        addr_bits = words.bit_length() - 1
        flops = words * BITS
        read_gates = words * BITS + BITS
        print(f"  {words:6d} bytes: {addr_bits:2d} address bits, {flops:7d} flip-flops, ~{read_gates:7d} read gates, ~{flops * 22:9d} transistors as DFFs vs {flops * 6:8d} as 6T SRAM cells")

    print("\n=== The T8 uses a 256-byte memory modelled in Python with the same behaviour ===")
    mem = Memory()
    mem.write(0x10, 25)
    mem.write(0x11, 300)
    print(f"  read 0x10 -> {mem.read(0x10)}, read 0x11 -> {mem.read(0x11)} (300 keeps only its low 8 bits)")


if __name__ == "__main__":
    main()
