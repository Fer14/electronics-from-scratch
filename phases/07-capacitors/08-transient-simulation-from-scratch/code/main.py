import numpy as np

from sim import Circuit


class TinyTransient:
    def __init__(self):
        self.nodes = {"0": -1}
        self.resistors = []
        self.voltage_sources = []
        self.current_sources = []
        self.capacitors = []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes) - 1
        return self.nodes[name]

    def resistor(self, a, b, ohms):
        self.resistors.append((self.node(a), self.node(b), 1.0 / ohms))

    def voltage_source(self, plus, minus, volts):
        self.voltage_sources.append((self.node(plus), self.node(minus), volts))

    def current_source(self, from_node, to_node, amps):
        self.current_sources.append((self.node(from_node), self.node(to_node), amps))

    def capacitor(self, a, b, farads, v0=0.0):
        self.capacitors.append((self.node(a), self.node(b), farads, v0))

    def size(self):
        return len(self.nodes) - 1 + len(self.voltage_sources)

    def stamp_conductance(self, matrix, a, b, conductance):
        if a >= 0:
            matrix[a, a] += conductance
        if b >= 0:
            matrix[b, b] += conductance
        if a >= 0 and b >= 0:
            matrix[a, b] -= conductance
            matrix[b, a] -= conductance

    def stamp_current(self, rhs, from_node, to_node, amps):
        if from_node >= 0:
            rhs[from_node] -= amps
        if to_node >= 0:
            rhs[to_node] += amps

    def solve_step(self, time, step, cap_volts, cap_currents, method):
        node_count = len(self.nodes) - 1
        matrix = np.zeros((self.size(), self.size()))
        rhs = np.zeros(self.size())
        for a, b, conductance in self.resistors:
            self.stamp_conductance(matrix, a, b, conductance)
        for from_node, to_node, amps in self.current_sources:
            self.stamp_current(rhs, from_node, to_node, amps(time) if callable(amps) else amps)
        for index, (a, b, farads, _) in enumerate(self.capacitors):
            if method == "backward_euler":
                conductance = farads / step
                history = conductance * cap_volts[index]
            else:
                conductance = 2 * farads / step
                history = conductance * cap_volts[index] + cap_currents[index]
            self.stamp_conductance(matrix, a, b, conductance)
            self.stamp_current(rhs, b, a, history)
        for index, (plus, minus, volts) in enumerate(self.voltage_sources):
            row = node_count + index
            if plus >= 0:
                matrix[plus, row] += 1
                matrix[row, plus] += 1
            if minus >= 0:
                matrix[minus, row] -= 1
                matrix[row, minus] -= 1
            rhs[row] = volts(time) if callable(volts) else volts
        return np.linalg.solve(matrix, rhs)

    def voltage(self, solution, node_index):
        return 0.0 if node_index < 0 else solution[node_index]

    def run(self, t_stop, step, method="backward_euler"):
        cap_volts = np.array([v0 for _, _, _, v0 in self.capacitors], dtype=float)
        cap_currents = np.zeros(len(self.capacitors))
        steps = int(round(t_stop / step))
        times = np.linspace(0.0, steps * step, steps + 1)
        history = np.zeros((steps + 1, len(self.nodes) - 1))
        history[0] = self.initial_node_voltages(cap_volts)
        for k in range(1, steps + 1):
            step_method = "backward_euler" if k == 1 else method
            solution = self.solve_step(times[k], step, cap_volts, cap_currents, step_method)
            for index, (a, b, farads, _) in enumerate(self.capacitors):
                new_volts = self.voltage(solution, a) - self.voltage(solution, b)
                if step_method == "backward_euler":
                    cap_currents[index] = farads / step * (new_volts - cap_volts[index])
                else:
                    cap_currents[index] = 2 * farads / step * (new_volts - cap_volts[index]) - cap_currents[index]
                cap_volts[index] = new_volts
            history[k] = solution[: len(self.nodes) - 1]
        return times, history

    def initial_node_voltages(self, cap_volts):
        guess = np.zeros(len(self.nodes) - 1)
        for index, (a, b, _, _) in enumerate(self.capacitors):
            if b < 0 and a >= 0:
                guess[a] = cap_volts[index]
        for plus, minus, volts in self.voltage_sources:
            if minus < 0 and plus >= 0:
                guess[plus] = volts(0.0) if callable(volts) else volts
        return guess

    def index_of(self, name):
        return self.nodes[name]


def rc_charge(method, step, tau=1e-3):
    tiny = TinyTransient()
    tiny.voltage_source("in", "0", 5.0)
    tiny.resistor("in", "cap", 1000.0)
    tiny.capacitor("cap", "0", tau / 1000.0)
    times, history = tiny.run(5 * tau, step, method)
    return times, history[:, tiny.index_of("cap")]


def show_one_rc():
    tau = 1e-3
    print("RC charge, R = 1 kOhm, C = 1 uF, 5 V, step h = tau / 10 = 0.1 ms")
    print(f"{'t (ms)':>7} {'exact (V)':>10} {'backward Euler':>15} {'trapezoidal':>12}")
    times, euler = rc_charge("backward_euler", tau / 10)
    _, trapezoid = rc_charge("trapezoidal", tau / 10)
    for k in (1, 2, 5, 10, 20, 50):
        exact = 5 * (1 - np.exp(-times[k] / tau))
        print(f"{times[k] * 1e3:>7.1f} {exact:>10.4f} {euler[k]:>15.4f} {trapezoid[k]:>12.4f}")
    print()


def show_error_vs_step():
    tau = 1e-3
    print("Worst error over the first 5 tau as the step shrinks")
    print(f"{'step':>10} {'backward Euler (mV)':>20} {'trapezoidal (mV)':>17}")
    for divisions in (5, 10, 20, 40, 80):
        step = tau / divisions
        times, euler = rc_charge("backward_euler", step)
        _, trapezoid = rc_charge("trapezoidal", step)
        exact = 5 * (1 - np.exp(-times / tau))
        print(f"{'tau/' + str(divisions):>10} {np.max(np.abs(euler - exact)) * 1e3:>20.3f} "
              f"{np.max(np.abs(trapezoid - exact)) * 1e3:>17.4f}")
    print("Halving the step roughly halves the Euler error (first order) and quarters the trapezoidal error (second order)")
    print()


def square_wave(time, period=4e-3):
    return 5.0 if (time % period) < period / 2 else 0.0


def show_ladder_against_sim():
    step, t_stop = 10e-6, 8e-3
    tiny = TinyTransient()
    tiny.voltage_source("in", "0", square_wave)
    tiny.resistor("in", "a", 1000.0)
    tiny.capacitor("a", "0", 1e-6)
    tiny.resistor("a", "b", 2200.0)
    tiny.capacitor("b", "0", 470e-9)
    for my_method, sim_method in (("backward_euler", "be"), ("trapezoidal", "trap")):
        compare_ladder(tiny, my_method, sim_method, step, t_stop)


def compare_ladder(tiny, my_method, sim_method, step, t_stop):
    times, history = tiny.run(t_stop, step, my_method)
    mine_a = history[:, tiny.index_of("a")]
    mine_b = history[:, tiny.index_of("b")]

    circuit = Circuit()
    circuit.pulse_source("V1", "in", "0", low=0.0, high=5.0, period=4e-3, duty=0.5)
    circuit.resistor("R1", "in", "a", 1000.0)
    circuit.capacitor("C1", "a", "0", 1e-6, v0=0.0)
    circuit.resistor("R2", "a", "b", 2200.0)
    circuit.capacitor("C2", "b", "0", 470e-9, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=step, method=sim_method)
    sim_time = np.asarray(result.time)
    sim_a = np.interp(times, sim_time, np.asarray(result.v("a")))
    sim_b = np.interp(times, sim_time, np.asarray(result.v("b")))

    print(f"Two-stage RC ladder, 5 V 250 Hz square wave, step 10 us: ours ({my_method}) vs sim (method='{sim_method}')")
    print(f"{'t (ms)':>7} {'ours a':>8} {'sim a':>8} {'ours b':>8} {'sim b':>8}")
    for moment in (0.5e-3, 1e-3, 2e-3, 3e-3, 4e-3, 6e-3, 8e-3):
        k = int(round(moment / step))
        print(f"{moment * 1e3:>7.1f} {mine_a[k]:>8.3f} {sim_a[k]:>8.3f} {mine_b[k]:>8.3f} {sim_b[k]:>8.3f}")
    worst = max(np.max(np.abs(mine_a - sim_a)[1:]), np.max(np.abs(mine_b - sim_b)[1:]))
    print(f"Largest difference between the two simulators: {worst:.1e} V")
    print()


if __name__ == "__main__":
    show_one_rc()
    show_error_vs_step()
    show_ladder_against_sim()
