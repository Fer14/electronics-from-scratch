import numpy as np

from sim import Circuit

VDD = 3.3


def uart_frame_bits(byte):
    return [0] + [(byte >> bit) & 1 for bit in range(8)] + [1]


def uart_line(message, baud, idle_bits=2):
    bits = []
    for character in message.encode("ascii"):
        bits += [1] * idle_bits + uart_frame_bits(character)
    bits += [1] * idle_bits
    edges = np.arange(len(bits) + 1) / baud

    def level(t):
        index = np.searchsorted(edges, t, side="right") - 1
        return bits[min(max(index, 0), len(bits) - 1)]

    return level, edges[-1]


def uart_receive(level, duration, baud, scan_step):
    received, errors = [], 0
    t = 0.0
    previous = 1
    while t < duration:
        current = level(t)
        if previous == 1 and current == 0:
            start = t
            byte = 0
            for bit in range(8):
                byte |= level(start + (1.5 + bit) / baud) << bit
            if level(start + 9.5 / baud) != 1:
                errors += 1
            received.append(byte)
            t = start + 9.5 / baud
            previous = 1
            continue
        previous = current
        t += scan_step
    return received, errors


def spi_transfer(master_byte, slave_byte):
    master, slave = master_byte, slave_byte
    trace = []
    for _ in range(8):
        mosi = (master >> 7) & 1
        miso = (slave >> 7) & 1
        master = ((master << 1) & 0xFF) | miso
        slave = ((slave << 1) & 0xFF) | mosi
        trace.append((mosi, miso))
    return master, slave, trace


class I2cBus:
    def __init__(self, devices):
        self.devices = devices

    def line(self, pulls_low):
        return 0 if any(pulls_low) else 1

    def write_register(self, address, register, value):
        events = ["START"]
        frame = (address << 1) | 0
        for byte in [frame, register, value]:
            for bit in reversed(range(8)):
                master_bit = (byte >> bit) & 1
                events.append(str(self.line([master_bit == 0])))
            target = self.devices.get(address)
            acknowledges = target is not None
            sda = self.line([acknowledges])
            events.append("ACK" if sda == 0 else "NACK")
            if not acknowledges:
                events.append("STOP")
                return events, False
        self.devices[address][register] = value
        events.append("STOP")
        return events, True


def i2c_rise(pull_up_ohms, bus_farads):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RPU", "vdd", "sda", pull_up_ohms)
    circuit.capacitor("CBUS", "sda", "0", bus_farads, v0=0.0)
    tau = pull_up_ohms * bus_farads
    result = circuit.transient(t_stop=5 * tau, dt=tau / 500)
    time, volts = np.asarray(result.time), np.asarray(result.v("sda"))
    t30 = np.interp(0.3 * VDD, volts, time)
    t70 = np.interp(0.7 * VDD, volts, time)
    return t70 - t30, tau


def main():
    baud = 9600
    print(f"UART 8N1 at {baud} baud: one bit lasts {1e6 / baud:.2f} us, one character (10 bits) {10e3 / baud:.3f} ms")
    for character in "Hi":
        bits = uart_frame_bits(ord(character))
        print(f"  '{character}' = 0x{ord(character):02X} = {ord(character):08b}, on the wire (start, LSB first, stop): "
              + "".join(str(b) for b in bits))
    level, duration = uart_line("Hi!", baud)
    received, errors = uart_receive(level, duration, baud, scan_step=1 / (16 * baud))
    print(f"  receiver decoded: {bytes(received).decode('ascii')!r}, framing errors {errors}")

    print("\nBaud-rate mismatch: transmitter fast by a few percent, receiver at 9600")
    for mismatch in [0.0, 0.02, 0.04, 0.05, 0.06, 0.08]:
        level, duration = uart_line("Hello", baud * (1 + mismatch))
        received, errors = uart_receive(level, duration, baud, scan_step=1 / (16 * baud))
        text = "".join(chr(b) if 32 <= b < 127 else "?" for b in received)
        hex_bytes = " ".join(f"{b:02X}" for b in received)
        print(f"  {mismatch * 100:4.1f}% fast: received {text!r:9s} ({hex_bytes})  framing errors {errors}  "
              f"{'ok' if text == 'Hello' and errors == 0 else 'BROKEN'}")
    print(f"  limit: the stop-bit sample at 9.5 bits may drift at most half a bit: 0.5 / 9.5 = {0.5 / 9.5 * 100:.1f}%")

    print("\nSPI mode 0: master sends 0x9F while the sensor sends back 0x42, one bit per clock")
    master_after, slave_after, trace = spi_transfer(0x9F, 0x42)
    print("  clock  MOSI  MISO")
    for clock, (mosi, miso) in enumerate(trace, 1):
        print(f"  {clock:5d}  {mosi:4d}  {miso:4d}")
    print(f"  after 8 clocks the master holds 0x{master_after:02X} and the sensor holds 0x{slave_after:02X}")

    print("\nI2C: write 0x07 into register 0x01 of the device at address 0x48 (open-drain, wired-AND)")
    bus = I2cBus({0x48: {}})
    for address in [0x48, 0x49]:
        events, ok = bus.write_register(address, 0x01, 0x07)
        print(f"  to 0x{address:02X}: {' '.join(events)}  -> {'written' if ok else 'nobody answered'}")

    bus_farads = 200e-12
    minimum_ohms = (VDD - 0.4) / 0.003
    print(f"\nI2C rise time with {bus_farads * 1e12:.0f} pF of bus capacitance (30% to 70% of VDD)")
    print(f"  smallest pull-up allowed by the 3 mA sink limit: ({VDD} - 0.4) / 3 mA = {minimum_ohms:.0f} ohm")
    for ohms in [1000, 2200, 4700, 10000]:
        rise, tau = i2c_rise(ohms, bus_farads)
        standard = "ok" if rise <= 1000e-9 else "too slow"
        fast = "ok" if rise <= 300e-9 else "too slow"
        print(f"  {ohms:6d} ohm: tau = {tau * 1e9:6.0f} ns, rise = {rise * 1e9:6.0f} ns "
              f"(theory {np.log(7 / 3) * tau * 1e9:6.0f} ns)  100 kHz: {standard:8s} 400 kHz: {fast}")


if __name__ == "__main__":
    main()
