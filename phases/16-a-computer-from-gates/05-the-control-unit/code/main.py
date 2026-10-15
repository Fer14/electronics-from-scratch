from itertools import product

from sim.logic import LogicCircuit

SIGNALS = ["PC_OUT", "MEM_OUT", "A_OUT", "ALU_OUT", "MAR_IN", "MEM_IN", "IR_IN", "A_IN",
           "B_IN", "OUT_IN", "PC_IN", "FLAGS_IN", "PC_INC", "END", "HALT"]
NAMES = {
    0x00: "NOP", 0x01: "OUT", 0x0F: "HLT", 0x10: "LDI", 0x11: "LDA", 0x12: "STA",
    0x20: "ADD", 0x21: "SUB", 0x22: "AND", 0x23: "OR", 0x24: "XOR",
    0x28: "ADDI", 0x29: "SUBI", 0x2A: "ANDI", 0x2B: "ORI", 0x2C: "XORI",
    0x30: "JMP", 0x31: "JZ", 0x32: "JNZ", 0x33: "JC", 0x34: "JNC",
}
FETCH = [{"PC_OUT", "MAR_IN"}, {"MEM_OUT", "IR_IN", "PC_INC"}]
POINT = {"PC_OUT", "MAR_IN"}
ADDRESS = {"MEM_OUT", "MAR_IN", "PC_INC"}


def jump_taken(opcode, z, c):
    return {0x30: True, 0x31: z == 1, 0x32: z == 0, 0x33: c == 1, 0x34: c == 0}[opcode]


def steps_for(opcode, z=0, c=0):
    if opcode == 0x00:
        tail = [{"END"}]
    elif opcode == 0x01:
        tail = [{"A_OUT", "OUT_IN", "END"}]
    elif opcode == 0x0F:
        tail = [{"HALT"}]
    elif opcode == 0x10:
        tail = [POINT, {"MEM_OUT", "A_IN", "PC_INC", "END"}]
    elif opcode == 0x11:
        tail = [POINT, ADDRESS, {"MEM_OUT", "A_IN", "END"}]
    elif opcode == 0x12:
        tail = [POINT, ADDRESS, {"A_OUT", "MEM_IN", "END"}]
    elif 0x20 <= opcode <= 0x24:
        tail = [POINT, ADDRESS, {"MEM_OUT", "B_IN"}, {"ALU_OUT", "A_IN", "FLAGS_IN", "END"}]
    elif 0x28 <= opcode <= 0x2C:
        tail = [POINT, {"MEM_OUT", "B_IN", "PC_INC"}, {"ALU_OUT", "A_IN", "FLAGS_IN", "END"}]
    elif 0x30 <= opcode <= 0x34:
        last = {"MEM_OUT", "PC_IN", "END"} if jump_taken(opcode, z, c) else {"PC_INC", "END"}
        tail = [POINT, last]
    else:
        tail = [{"END"}]
    return FETCH + tail


def microcode(opcode, step, z, c):
    steps = steps_for(opcode, z, c)
    return steps[step] if step < len(steps) else set()


def control_word(signals):
    return sum(1 << SIGNALS.index(s) for s in signals)


def step_counter():
    lc = LogicCircuit("3-bit step counter with END reset")
    lc.inputs("end")
    toggle = "one"
    lc.constant("one", 1)
    for i in range(3):
        lc.xor(f"d{i}", f"t{i}", toggle)
        lc.dff(f"d{i}", f"t{i}", name=f"T{i}", reset="end")
        if i < 2:
            lc.and_(f"k{i + 1}", toggle, f"t{i}")
            toggle = f"k{i + 1}"
    lc.outputs("t2", "t1", "t0")
    return lc


def classes(opcode):
    return {
        "ldi": int(opcode == 0x10),
        "lda": int(opcode == 0x11),
        "alum": int(0x20 <= opcode <= 0x24),
        "alui": int(0x28 <= opcode <= 0x2C),
        "two": int(opcode in NAMES and opcode not in (0x00, 0x01, 0x0F)),
        "mem": int(opcode in (0x11, 0x12) or 0x20 <= opcode <= 0x24),
    }


def hardwired():
    lc = LogicCircuit("hardwired MAR_IN and A_IN")
    lc.inputs("t0", "t1", "t2", "t3", "t4", "t5", "ldi", "lda", "alum", "alui", "two", "mem")
    lc.and_("m2", "t2", "two")
    lc.and_("m3", "t3", "mem")
    lc.or_("MAR_IN", "t0", "m2", "m3")
    lc.and_("a3", "t3", "ldi")
    lc.and_("a4", "t4", "lda")
    lc.and_("a5", "t5", "alum")
    lc.and_("a4i", "t4", "alui")
    lc.or_("A_IN", "a3", "a4", "a5", "a4i")
    lc.outputs("MAR_IN", "A_IN")
    return lc


def main():
    print("=== Microcode: the control words of every instruction, step by step ===")
    for opcode in [0x00, 0x01, 0x0F, 0x10, 0x11, 0x12, 0x20, 0x28, 0x30, 0x31]:
        steps = steps_for(opcode, z=1)
        print(f"  {opcode:02X} {NAMES[opcode]:4s} ({len(steps)} cycles)")
        for t, signals in enumerate(steps):
            print(f"      T{t}: {control_word(signals):04X}  {', '.join(s for s in SIGNALS if s in signals)}")
    print("  JZ with Z = 0 instead ends with: " + ", ".join(sorted(steps_for(0x31, z=0)[3])))

    print("\n=== As a ROM ===")
    address_bits = 8 + 3 + 2
    print(f"  address = opcode (8 bits) + step (3 bits) + Z + C = {address_bits} bits -> {2 ** address_bits} words")
    print(f"  each word = {len(SIGNALS)} control bits -> {2 ** address_bits * len(SIGNALS)} bits of microcode ROM")
    used = sum(len(steps_for(op, z, c)) for op in NAMES for z, c in product((0, 1), repeat=2))
    print(f"  words actually used by the {len(NAMES)} instructions: {used}")

    print("\n=== The step counter: counts T0, T1, ... and resets when END is active ===")
    counter = step_counter()
    lda = steps_for(0x11)
    sequence = []
    for _ in range(2):
        for signals in lda:
            out = counter.evaluate({"end": 0})
            sequence.append(4 * out["t2"] + 2 * out["t1"] + out["t0"])
            counter.step({"end": int("END" in signals)})
    print(f"  two LDA instructions in a row: T-states {sequence}")

    print("\n=== Hardwired logic for two control signals, checked against the microcode ===")
    hw = hardwired()
    print(f"  MAR_IN = T0 + T2·two + T3·mem        A_IN = T3·LDI + T4·LDA + T5·ALUm + T4·ALUi")
    wrong = checked = 0
    for opcode in NAMES:
        for step in range(6):
            for z, c in product((0, 1), repeat=2):
                inputs = {f"t{k}": int(k == step) for k in range(6)}
                inputs.update(classes(opcode))
                out = hw.evaluate(inputs)
                want = microcode(opcode, step, z, c)
                wrong += out["MAR_IN"] != int("MAR_IN" in want)
                wrong += out["A_IN"] != int("A_IN" in want)
                checked += 2
    print(f"  {checked} checks over all instructions, steps and flags: {wrong} wrong; {hw.gate_count()} gates")


if __name__ == "__main__":
    main()
