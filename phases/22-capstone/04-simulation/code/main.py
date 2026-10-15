import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit
from sim.lab import evaluate, load_task

VDD = 3.3
ADC_MAX = 1023
ON_CODE = 390
OFF_CODE = 584
AVERAGE_SAMPLES = 4
TARGET_AVG_A = 0.0057
PWM_HZ = 1000


def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7


def light_code(lux, noise):
    volts = VDD * 10_000 / (ldr_ohms(max(lux, 0.01)) + 10_000)
    return int(min(max(round(volts / VDD * ADC_MAX + noise), 0), ADC_MAX))


def battery_code(vbat):
    return int(round(vbat / 2 / VDD * ADC_MAX))


def pwm_led(vbat, duty, cycles=40):
    period = 1 / PWM_HZ
    c = Circuit()
    c.voltage_source("BAT", "bat_ideal", "0", vbat)
    c.resistor("R_INT", "bat_ideal", "vbat", 0.5)
    c.pulse_source("PB1", "pin", "0", low=0.0, high=VDD, period=period, duty=duty)
    c.resistor("R4", "pin", "base", 2200)
    c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    c.resistor("R5", "vbat", "led_a", 68)
    c.led("D1", "led_a", "led_k", color="white")
    t = c.transient(t_stop=cycles * period, dt=period / 200)
    last = t.time >= (cycles - 10) * period
    current = t.i("D1")
    return t.time, current, float(current[last].mean()), float(current.max())


class Firmware:
    def __init__(self, hysteresis=True, averaging=True):
        self.hysteresis = hysteresis
        self.averaging = averaging
        self.history = []
        self.on = False
        self.switches = 0

    def duty_for(self, vbat_code):
        vbat = vbat_code / ADC_MAX * VDD * 2
        on_current = max((vbat - 3.09) / 75.0, 1e-4)
        return min(TARGET_AVG_A / on_current, 1.0)

    def tick(self, light, vbat_code):
        self.history = (self.history + [light])[-AVERAGE_SAMPLES:]
        value = sum(self.history) / len(self.history) if self.averaging else light
        if self.hysteresis:
            wanted = (value < ON_CODE) if not self.on else not (value > OFF_CODE)
        else:
            wanted = value < (ON_CODE + OFF_CODE) / 2
        if wanted != self.on:
            self.switches += 1
            self.on = wanted
        return self.duty_for(vbat_code) if self.on else 0.0


def night_lux(seconds):
    hour = 18 + seconds / 3600
    if hour < 19.5:
        base = 120.0
    elif hour < 21.0:
        base = 120.0 * 10 ** (-(hour - 19.5) / 1.5 * 2.4)
    elif hour < 6.0 + 24:
        base = 0.5
    elif hour < 7.5 + 24:
        base = 0.5 * 10 ** ((hour - 30.0) / 1.5 * 2.9)
    else:
        base = 400.0
    wobble = 1 + 0.25 * math.sin(seconds / 37.0) * math.sin(seconds / 11.0)
    lux = base * wobble
    for start in (5.5 * 3600, 8.2 * 3600):
        if start <= seconds < start + 2:
            lux = max(lux, 60.0)
    return lux


def run_night(firmware, vbat=4.2):
    seconds = np.arange(0, 15 * 3600)
    duties = np.zeros(len(seconds))
    lux = np.zeros(len(seconds))
    for n, s in enumerate(seconds):
        lux[n] = night_lux(float(s))
        noise = 2.0 * math.sin(s * 1.7)
        duties[n] = firmware.tick(light_code(lux[n], noise), battery_code(vbat))
    return seconds, lux, duties


def main():
    print("Step 1: PWM through the transistor (4.5 V battery, 1 kHz, 30% duty)")
    time, current, average, peak = pwm_led(4.5, 0.3)
    on_fraction = float((current > peak / 2).mean())
    print(f"  peak LED current {peak * 1000:.2f} mA, average {average * 1000:.2f} mA,"
          f" LED on for {on_fraction * 100:.1f}% of the time")
    print(f"  PWM at {PWM_HZ} Hz: far above the ~100 Hz where people notice flicker (R3)")

    print("\nStep 2: battery compensation keeps the average current steady (R5)")
    fw = Firmware()
    averages = []
    for vbat in (4.5, 4.2, 3.9, 3.6):
        duty = fw.duty_for(battery_code(vbat))
        _, _, avg, peak = pwm_led(vbat, duty)
        _, _, fixed_avg, _ = pwm_led(vbat, 0.3)
        averages.append(avg)
        print(f"  battery {vbat:.1f} V (code {battery_code(vbat)}): duty {duty * 100:5.1f}%, average {avg * 1000:5.2f} mA"
              f" (fixed 30% duty would give {fixed_avg * 1000:5.2f} mA)")
    spread = (max(averages) - min(averages)) / max(averages) * 100
    print(f"  spread of the compensated average: {spread:.1f}% (R5 allows 20%)")

    print("\nStep 3: one whole night, 18:00 to 09:00, one decision per second")
    designs = {"hysteresis + 4 s average": Firmware(),
               "single threshold, no averaging": Firmware(hysteresis=False, averaging=False)}
    results = {}
    for name, firmware in designs.items():
        seconds, lux, duties = run_night(firmware)
        on = duties > 0
        on_hours = on.sum() / 3600
        first_on = seconds[np.argmax(on)] / 3600 + 18
        last_on = seconds[len(on) - 1 - np.argmax(on[::-1])] / 3600 + 18
        results[name] = (seconds, lux, duties)
        print(f"  {name:31s}: {firmware.switches:4d} switchings, on {on_hours:5.2f} h,"
              f" first on {first_on:5.2f} h, last on {last_on - 24:5.2f} h next morning")
    for name, (seconds, lux, duties) in results.items():
        for label, start in (("headlights", 5.5 * 3600), ("headlights", 8.2 * 3600)):
            window = (seconds >= start - 5) & (seconds < start + 10)
            state = "stays on" if duties[window].min() > 0 else "goes OFF"
            print(f"  {name:31s}: {label} at {18 + start / 3600:5.2f} h ({lux[window].max():.0f} lux) -> LED {state}")
    seconds, lux, duties = results["hysteresis + 4 s average"]

    print("\nStep 4: plot of the night")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4.5), sharex=True)
    hours = seconds / 3600 + 18
    ax1.semilogy(hours, lux, linewidth=0.6)
    ax1.set_ylabel("light (lux)")
    for name, (_, _, d) in results.items():
        ax2.plot(hours, d * 100, linewidth=0.8, label=name)
    ax2.set_ylabel("LED duty (%)")
    ax2.set_xlabel("hour (18 = 6 pm, 30 = 6 am)")
    ax2.legend(fontsize=7)
    out = Path(__file__).parent / "night.png"
    fig.tight_layout()
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print(f"  saved {out.name}")

    print("\nStep 5: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        result = evaluate(task, {"S1": part})[0]
        print(f"  duty {part['duty'] * 100:3.0f}%: filtered sense voltage {result['value'] * 1000:5.2f} mV"
              f" -> {'PASS' if result['passed'] else 'fail'}")


if __name__ == "__main__":
    main()
