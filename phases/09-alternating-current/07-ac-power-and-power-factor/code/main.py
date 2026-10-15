import cmath
import math

import numpy as np

from sim import Circuit

V_RMS = 230.0
FREQ = 50.0
OMEGA = 2 * math.pi * FREQ
MOTOR_R = 16.0
MOTOR_L = 12.0 / OMEGA
CABLE_R = 0.5


def cycle_average(time, values, cycles):
    keep = time >= time[-1] - cycles / FREQ
    return float(np.trapezoid(values[keep], time[keep]) / (time[keep][-1] - time[keep][0]))


def cycle_rms(time, values, cycles):
    return math.sqrt(cycle_average(time, values**2, cycles))


def complex_power(v_rms_phasor, i_rms_phasor):
    return v_rms_phasor * i_rms_phasor.conjugate()


def main():
    peak = V_RMS * math.sqrt(2)
    t = np.arange(0, 1 / FREQ, 1e-6)
    v = peak * np.sin(OMEGA * t)

    print("=== Step 1: Instantaneous power in R, L and C (230 V RMS, 50 Hz) ===")
    loads = {
        "resistor 52.9 ohm": (52.9, 0.0),
        "inductor 168.4 mH": (OMEGA * 0.1684, 90.0),
        "capacitor 60.2 uF": (1 / (OMEGA * 60.2e-6), -90.0),
    }
    for name, (size, angle) in loads.items():
        i = peak / size * np.sin(OMEGA * t - math.radians(angle))
        p = v * i
        print(f"  {name:<20} p(t) from {p.min():8.1f} W to {p.max():8.1f} W, average {p.mean():8.2f} W")

    print("\n=== Step 2: A motor modelled as R + jX ===")
    z = complex(MOTOR_R, OMEGA * MOTOR_L)
    voltage = cmath.rect(V_RMS, 0.0)
    current = voltage / z
    s = complex_power(voltage, current)
    print(f"  Z = {z.real:.1f} + j{z.imag:.1f} ohm = {abs(z):.1f} ohm at {math.degrees(cmath.phase(z)):.2f} deg (L = {MOTOR_L * 1000:.2f} mH)")
    print(f"  I = 230 / Z = {abs(current):.2f} A RMS at {math.degrees(cmath.phase(current)):.2f} deg")
    print(f"  S = V x conj(I) = {s.real:.1f} + j{s.imag:.1f} VA")
    print(f"  real power      P = {s.real:8.1f} W")
    print(f"  reactive power  Q = {s.imag:8.1f} var")
    print(f"  apparent power |S| = {abs(s):8.1f} VA")
    print(f"  power factor   P / |S| = {s.real / abs(s):.3f} (lagging: current behind voltage)")

    print("\n=== Step 3: Check with a time simulation ===")
    c = Circuit()
    c.sine_source("V1", "line", "0", amplitude=peak, freq=FREQ)
    c.resistor("Rm", "line", "m", MOTOR_R)
    c.inductor("Lm", "m", "0", MOTOR_L)
    tr = c.transient(t_stop=0.2, dt=1e-5)
    p_avg = cycle_average(tr.time, tr.v("line") * tr.i("Rm"), cycles=5)
    i_rms = cycle_rms(tr.time, tr.i("Rm"), cycles=5)
    print(f"  average of v x i over the last 5 cycles = {p_avg:.1f} W")
    print(f"  RMS current = {i_rms:.2f} A, V_rms x I_rms = {V_RMS * i_rms:.1f} VA")
    print(f"  heat in the motor resistance I^2 R = {i_rms**2 * MOTOR_R:.1f} W")

    print("\n=== Step 4: Power factor correction with a parallel capacitor ===")
    q = s.imag
    c_needed = q / (OMEGA * V_RMS**2)
    print(f"  the capacitor must supply Q = {q:.1f} var: C = Q / (omega V^2) = {c_needed * 1e6:.1f} uF")
    for label, cap in (("no capacitor", 0.0), (f"{c_needed * 1e6:.1f} uF", c_needed), ("150 uF (too big)", 150e-6)):
        net = Circuit()
        net.sine_source("V1", "line", "0", amplitude=peak, freq=FREQ)
        net.resistor("Rm", "line", "m", MOTOR_R)
        net.inductor("Lm", "m", "0", MOTOR_L)
        if cap:
            net.capacitor("Cpf", "line", "0", cap)
        a = net.ac([FREQ], source="V1")
        line_current = complex(a.i("V1")[0]) * V_RMS
        pf = math.cos(cmath.phase(line_current))
        cable_loss = abs(line_current) ** 2 * CABLE_R
        print(f"  {label:<18} line current {abs(line_current):6.2f} A RMS, power factor {pf:.3f}, "
              f"loss in a {CABLE_R} ohm cable {cable_loss:5.1f} W")
    print(f"  the motor still gets P = {s.real:.1f} W in every case")


if __name__ == "__main__":
    main()
