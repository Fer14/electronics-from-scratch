from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sim import Circuit

DIVISIONS_ACROSS = 10
DIVISIONS_UP = 8
COLUMNS_PER_DIVISION = 6
ROWS_PER_DIVISION = 2


def record_signals():
    c = Circuit()
    c.sine_source("Vsine", "ch1", "0", amplitude=2.0, freq=1000.0, offset=1.0)
    c.resistor("Rload1", "ch1", "0", 1000.0)
    c.pulse_source("Vpulse", "ch2", "0", low=0.0, high=5.0, period=1e-3, duty=0.25)
    c.resistor("Rload2", "ch2", "0", 1000.0)
    t = c.transient(t_stop=5e-3, dt=1e-6)
    return np.asarray(t.time), np.asarray(t.v("ch1")), np.asarray(t.v("ch2"))


def rising_crossings(time, volts, level):
    below = volts[:-1] < level
    above = volts[1:] >= level
    indices = np.nonzero(below & above)[0]
    fractions = (level - volts[indices]) / (volts[indices + 1] - volts[indices])
    return time[indices] + fractions * (time[indices + 1] - time[indices])


def ascii_screen(time, traces, trigger_time, seconds_per_division):
    width = DIVISIONS_ACROSS * COLUMNS_PER_DIVISION + 1
    height = DIVISIONS_UP * ROWS_PER_DIVISION + 1
    screen = [[" "] * width for _ in range(height)]
    for row in range(height):
        for column in range(width):
            on_vertical = column % COLUMNS_PER_DIVISION == 0
            on_horizontal = row % ROWS_PER_DIVISION == 0
            if on_vertical and on_horizontal:
                screen[row][column] = "+"
            elif row == height // 2:
                screen[row][column] = "-"
            elif column == width // 2:
                screen[row][column] = ":"
    start = trigger_time - seconds_per_division
    for symbol, volts, volts_per_division, position_divisions in traces:
        for column in range(width):
            moment = start + column * seconds_per_division / COLUMNS_PER_DIVISION
            value = np.interp(moment, time, volts)
            divisions_up = value / volts_per_division + position_divisions
            row = round(height // 2 - divisions_up * ROWS_PER_DIVISION)
            if 0 <= row < height:
                screen[row][column] = symbol
    return "\n".join("  |" + "".join(line) + "|" for line in screen)


def measurements(time, volts, level):
    crossings = rising_crossings(time, volts, level)
    period = float(np.mean(np.diff(crossings)))
    return {
        "max (V)": float(volts.max()),
        "min (V)": float(volts.min()),
        "peak-to-peak (V)": float(volts.max() - volts.min()),
        "mean (V)": float(volts.mean()),
        "RMS (V)": float(np.sqrt(np.mean(volts**2))),
        "period (ms)": period * 1000,
        "frequency (Hz)": 1.0 / period,
        "duty (%)": 100.0 * float(np.mean(volts > level)),
    }


print("Step 1: record two signals with the simulator (5 ms, 1 us steps)")
time, channel_1, channel_2 = record_signals()
print(f"  {len(time)} samples; channel 1 is a 1 kHz sine, channel 2 a 1 kHz pulse train")

print()
print("Step 2: a trigger finds the same moment in every cycle")
trigger_level = 1.0
crossings = rising_crossings(time, channel_1, trigger_level)
print(f"  channel 1 rises through {trigger_level} V at: " + ", ".join(f"{1000 * x:.3f} ms" for x in crossings))
print("  each crossing is one period later: a stable picture needs the screen to start at one of them")

print()
print("Step 3: draw the screen (0.2 ms/div, trigger on channel 1 rising at 1 V)")
print("  * = channel 1 (sine), 1 V/div, its 0 V on the centre line")
print("  o = channel 2 (pulse), 2 V/div, its 0 V moved down 4 divisions to the bottom edge")
print(ascii_screen(time, [("o", channel_2, 2.0, -4.0), ("*", channel_1, 1.0, 0.0)], crossings[1], 0.2e-3))

print()
print("Step 4: automatic measurements")
for name, volts, level in [("channel 1", channel_1, 1.0), ("channel 2", channel_2, 2.5)]:
    window = time >= 1e-3
    values = measurements(time[window], volts[window], level)
    print(f"  {name}:")
    for key, value in values.items():
        print(f"    {key:<17} {value:10.3f}")
print("  sine check: RMS = sqrt(offset^2 + amplitude^2 / 2) = sqrt(1 + 2) = 1.732 V")

print()
print("Step 5: x1 versus x10 probe on a 1 Mohm / 1 Mohm divider from 10 V (true 5 V)")
for name, probe_series, factor in [("x1 probe ", 0.0, 1.0), ("x10 probe", 9e6, 10.0)]:
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 10.0)
    c.resistor("R1", "vcc", "mid", 1e6)
    c.resistor("R2", "mid", "0", 1e6)
    if probe_series:
        c.resistor("Rprobe", "mid", "scope", probe_series)
    else:
        c.switch("Sprobe", "mid", "scope", closed=True)
    c.resistor("Rscope", "scope", "0", 1e6)
    r = c.dc()
    print(f"  {name}: scope input sees {r.v('scope'):.3f} V, display x{factor:.0f} = {factor * r.v('scope'):.3f} V")

print()
print("Step 6: sampling too slowly makes a fake slow wave (aliasing)")
for sample_rate in [20000.0, 1100.0]:
    sample_times = np.arange(0, 0.02, 1.0 / sample_rate)
    samples = 2.0 * np.sin(2 * np.pi * 1000.0 * sample_times)
    spectrum = np.abs(np.fft.rfft(samples))
    frequencies = np.fft.rfftfreq(len(samples), 1.0 / sample_rate)
    print(f"  1000 Hz sine sampled at {sample_rate:>7.0f} samples/s looks like {frequencies[np.argmax(spectrum)]:.0f} Hz")

figure, axis = plt.subplots(figsize=(8, 5))
start = crossings[1] - 0.2e-3
window = (time >= start) & (time <= start + 2e-3)
axis.plot((time[window] - start) * 1000, channel_1[window], label="channel 1")
axis.plot((time[window] - start) * 1000, channel_2[window], label="channel 2")
axis.set_xticks(np.arange(0, 2.01, 0.2))
axis.set_yticks(np.arange(-4, 4.01, 1))
axis.set_ylim(-4, 4)
axis.grid(True)
axis.set_xlabel("time (ms), 0.2 ms/div")
axis.set_ylabel("volts, 1 V/div")
axis.legend()
figure.tight_layout()
figure.savefig(Path(__file__).parent / "out.png", dpi=100)
print()
print("  saved", Path(__file__).parent / "out.png")
