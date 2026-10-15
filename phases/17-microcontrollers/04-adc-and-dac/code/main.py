from sim import Circuit

VREF = 3.3
ADC_BITS = 10
R_TOP = 33_000
R_BOTTOM = 8_200
DAC_BITS = 8
LADDER_R = 10_000


class SarAdc:
    def __init__(self, bits, vref):
        self.bits = bits
        self.vref = vref

    @property
    def lsb(self):
        return self.vref / 2 ** self.bits

    def dac_voltage(self, code):
        return code * self.lsb

    def convert(self, volts, verbose=False):
        code = 0
        for bit in reversed(range(self.bits)):
            trial = code | (1 << bit)
            keep = volts >= self.dac_voltage(trial)
            if verbose:
                print(f"    try bit {bit}: code {trial:0{self.bits}b} = {self.dac_voltage(trial):.4f} V -> "
                      f"{'input is higher, keep the 1' if keep else 'input is lower, clear it'}")
            if keep:
                code = trial
        return max(0, min(code, 2 ** self.bits - 1))


def divider_voltage(battery_volts):
    circuit = Circuit()
    circuit.voltage_source("VBAT", "bat", "0", battery_volts)
    circuit.resistor("RTOP", "bat", "adc", R_TOP)
    circuit.resistor("RBOT", "adc", "0", R_BOTTOM)
    result = circuit.dc()
    return result.v("adc"), result.i("RTOP")


def r2r_output(code, bits, mismatch=None):
    mismatch = mismatch or {}
    circuit = Circuit()
    circuit.resistor("RTERM", "n0", "0", 2 * LADDER_R)
    for bit in range(bits):
        level = VREF if (code >> bit) & 1 else 0.0
        circuit.voltage_source(f"VB{bit}", f"b{bit}", "0", level)
        circuit.resistor(f"R2_{bit}", f"b{bit}", f"n{bit}", 2 * LADDER_R * mismatch.get(bit, 1.0))
        if bit + 1 < bits:
            circuit.resistor(f"R_{bit}", f"n{bit}", f"n{bit + 1}", LADDER_R)
    return circuit.dc().v(f"n{bits - 1}")


def main():
    adc = SarAdc(ADC_BITS, VREF)
    print(f"{ADC_BITS}-bit ADC, reference {VREF} V: 1 LSB = {adc.lsb * 1e3:.3f} mV, codes 0..{2 ** ADC_BITS - 1}")

    print("\nOne successive-approximation conversion of 1.000 V")
    code = adc.convert(1.0, verbose=True)
    print(f"  result: code {code} -> {adc.dac_voltage(code):.4f} V (error {(1.0 - adc.dac_voltage(code)) * 1e3:.2f} mV, less than 1 LSB)")

    ratio = R_BOTTOM / (R_TOP + R_BOTTOM)
    thevenin = R_TOP * R_BOTTOM / (R_TOP + R_BOTTOM)
    print(f"\nBattery monitor: {R_TOP / 1e3:.0f} k over {R_BOTTOM / 1e3:.1f} k, ratio {ratio:.4f}, "
          f"source resistance seen by the ADC {thevenin / 1e3:.2f} kohm")
    print(f"  {'battery':>8s} {'ADC pin':>8s} {'code':>5s} {'firmware says':>13s} {'error':>8s} {'divider current':>15s}")
    for battery in [10.5, 11.8, 12.6, 13.8, 14.4]:
        pin_volts, current = divider_voltage(battery)
        code = adc.convert(pin_volts)
        estimate = adc.dac_voltage(code) / ratio
        print(f"  {battery:6.2f} V {pin_volts:6.3f} V {code:5d} {estimate:11.3f} V {(estimate - battery) * 1e3:6.1f} mV "
              f"{current * 1e6:12.1f} uA")
    print(f"  one ADC step is worth {adc.lsb / ratio * 1e3:.1f} mV of battery voltage")

    print(f"\n{DAC_BITS}-bit R-2R DAC (R = {LADDER_R / 1e3:.0f} k, 2R = {2 * LADDER_R / 1e3:.0f} k), reference {VREF} V")
    print(f"  {'code':>5s} {'binary':>10s} {'ladder out':>10s} {'ideal':>8s}")
    for code in [0, 1, 2, 64, 127, 128, 200, 255]:
        out = r2r_output(code, DAC_BITS)
        print(f"  {code:5d} {code:08b}   {out:8.4f} V {code * VREF / 2 ** DAC_BITS:6.4f} V")

    print("\nWith the MSB's 2R resistor 2% too large, the step from 127 to 128 goes wrong")
    lsb = VREF / 2 ** DAC_BITS
    for label, mismatch in [("perfect", None), ("MSB +2%", {DAC_BITS - 1: 1.02})]:
        low = r2r_output(127, DAC_BITS, mismatch)
        high = r2r_output(128, DAC_BITS, mismatch)
        step = high - low
        print(f"  {label:8s} 127 -> {low:.4f} V, 128 -> {high:.4f} V, step = {step * 1e3:6.2f} mV "
              f"= {step / lsb:5.2f} LSB (ideal 1.00)")


if __name__ == "__main__":
    main()
