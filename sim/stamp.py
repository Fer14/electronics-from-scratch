"""The equation board: a matrix A and a right-hand side b that every element writes into.

Unknowns are the node voltages (ground is index -1 and never appears) followed by
branch currents for the elements that need one (voltage sources, inductors, capacitors,
controlled sources, op-amp outputs). Row n of a node says: the currents leaving node n
through the elements equal the current pushed into node n by the sources.
"""
import numpy as np


def node_voltage(x, index):
    if index < 0:
        return 0.0 * x[..., 0] if np.ndim(x) > 1 else 0.0
    return x[..., index]


class Stamper:
    def __init__(self, size, dtype=float, matrix=True):
        self.A = np.zeros((size, size), dtype) if matrix else None
        self.b = np.zeros(size, dtype)

    def add(self, row, col, value):
        if self.A is not None and row >= 0 and col >= 0:
            self.A[row, col] += value

    def rhs(self, row, value):
        if row >= 0:
            self.b[row] += value

    def conductance(self, a, b, g):
        self.add(a, a, g)
        self.add(b, b, g)
        self.add(a, b, -g)
        self.add(b, a, -g)

    def inject(self, a, b, amps):
        self.rhs(a, -amps)
        self.rhs(b, amps)

    def branch(self, a, b, k):
        self.add(a, k, 1.0)
        self.add(b, k, -1.0)

    def branch_voltage(self, k, a, b, coeff=1.0):
        self.add(k, a, coeff)
        self.add(k, b, -coeff)

    def linearized(self, nodes, v0, currents, jac):
        for i, ni in enumerate(nodes):
            offset = currents[i]
            for j, nj in enumerate(nodes):
                self.add(ni, nj, jac[i][j])
                offset -= jac[i][j] * v0[j]
            self.rhs(ni, -offset)


def solve(A, b):
    try:
        return np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return np.linalg.lstsq(A, b, rcond=None)[0]
