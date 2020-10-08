#!/usr/bin/env python3

#from ..Interface import *


import numpy as np
from qiskit import QuantumCircuit
from qiskit import execute, Aer


class QiskitCircuitMaker():

    def __init__(self):
        self.initial_state = [0, 1]

    def set_qiskit_superpos_circ(self, superpositions):


        length = len(superpositions)

        initial_state = [0, 1]
        circ = QuantumCircuit(length, length)

        circ = self.set_double_circ(circ, superpositions)

        circ = self.set_single_circ(circ, superpositions)
        measure_list = [i for i in range(length)]
        circ.measure(measure_list, measure_list)
        print(circ.draw())
        return circ

    def set_double_circ(self, circ, superpositions):
        already_set_cx = []
        length = len(superpositions)
        for i in range(length):
            for k in range(length):
                if superpositions[i] == superpositions[k]:
                    if i == k:
                        continue
                    else:
                        lis = [i, k]
                        lis.sort()
                        if not lis in already_set_cx:
                            circ.h(i)
                            circ.initialize(self.initial_state, k)
                            circ.cx(i, k)
                            already_set_cx.append(lis)
                            print('already set cx =', already_set_cx)
        return circ

    def set_single_circ(self, circ, superpositions):
        superpositions_flat = []
        for i in range(len(superpositions)):
            for j in range(2):
                superpositions_flat.append(superpositions[i][j])

        uniq, uniq_counts = np.unique(superpositions, return_counts=True, axis=None)

        true_uniq = []
        for i in range(len(uniq_counts)):
            if uniq_counts[i] == 1:
                true_uniq.append(uniq[i])


        pos = []
        for i in range(len(true_uniq)):
            pos.append(superpositions_flat.index(true_uniq[i]))

        pos = np.array(pos)
        pos_qbits = pos // 2

        ###find qbits, 2 mal in der liste pos_qbits vorkommen und somit nicht verschränkt sind
        var1, var2 = np.unique(pos_qbits, return_counts=True)
        n_ent_qbits = []
        for i in range(len(var2)):
            if var2[i] == 2:
                n_ent_qbits.append(var1[i])

        # draw circuit for the qbits that are not entagled
        for i in range(len(n_ent_qbits)):
            circ.h(n_ent_qbits[i])
            # circ.measure(n_ent_qbits[i], n_ent_qbits[i])

        return circ


    def measure(self, circ):
        backend = Aer.get_backend('statevector_simulator')
        job = execute(circ, backend)
        result = job.result()
        counts = execute(circ, Aer.get_backend('qasm_simulator'), shots=1).result().get_counts()
        print(counts)
        res = [i for i in counts.keys()]
        print(res)
        return res[0]