#!/usr/bin/env python3
from qiskit import *
from math import pi
import numpy as np
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.tools.visualization import circuit_drawer
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(3)
# Apply H-gate to each qubit:
for qubit in range(3):
    qc.h(qubit)
# See the circuit:
qc.draw()
circuit_drawer(qc)

qc.show()
print('finished')