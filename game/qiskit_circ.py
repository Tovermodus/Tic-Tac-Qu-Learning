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
        circ, superpositions = self.part_ent_circ(circ, superpositions)
        circ = self.set_double_circ(circ, superpositions)

        circ = self.set_single_circ(circ, superpositions)

        #circ = self.part_ent_circ(superpositions)
        measure_list = [i for i in range(length)]
        circ.measure(measure_list, measure_list)
        print(circ.draw())
        return circ, superpositions

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
        return circ


    def set_single_circ(self, circ, superpositions, output=False):
        superpositions_flat = []
        for i in range(len(superpositions)):
            for j in range(2):
                superpositions_flat.append(superpositions[i][j])

        uniq, uniq_counts = np.unique(superpositions, return_counts=True, axis=None)

        if output:
            print('List Superpositions:', superpositions)
            print('array verschiedener Zahlen in liste Superpos.', uniq)
            print('anzahl wie häufig diese Zahl in superpos vorkommt:', uniq_counts)

        true_uniq = []
        zwei_in_feld = []
        for i in range(len(uniq_counts)):
            if uniq_counts[i] == 1:
                true_uniq.append(uniq[i])
            if uniq_counts[i] == 2:
                zwei_in_feld.append(uniq[i])

        if output:
            print()
            print('Felder mit nur einer Superposition', true_uniq)
            print('Felder mit 2 Superpositionen', zwei_in_feld)
            print()

        pos = []
        for i in range(len(true_uniq)):
            pos.append(superpositions_flat.index(true_uniq[i]))

        if output:
            print('pos =', pos)

        pos = np.array(pos)
        pos_qbits = pos // 2

        ###find qbits, 2 mal in der liste pos_qbits vorkommen und somit nicht verschränkt sind
        var1, var2 = np.unique(pos_qbits, return_counts=True)
        n_ent_qbits = []
        par_ent_qbits = []
        for i in range(len(var2)):
            if var2[i] == 2:
                n_ent_qbits.append(var1[i])
            if var2[i] == 1:
                par_ent_qbits.append(var1[i])

        if output:
            print('qbit nummer', pos_qbits)
            print('nicht verschraenkte qbits:', n_ent_qbits)

        # draw circuit for the qbits that are not entagled
        for i in range(len(n_ent_qbits)):
            circ.h(n_ent_qbits[i])
            # circ.measure(n_ent_qbits[i], n_ent_qbits[i])

        return circ

    def part_ent_circ(self, circ, superpositions):

        already_set = []
        had = []
        length = len(superpositions)
        for i in range(length):
            for k in range(length):
                if superpositions[i] == superpositions[k]:
                    continue
                if i == k:
                    continue

                for j in superpositions[i]:

                    if j in superpositions[k]:
                        if i < k:

                            if (superpositions[i].index(j) == 0 and superpositions[k].index(j) == 0):
                                superpositions[i][0], superpositions[i][1] = superpositions[i][1], superpositions[i][0]


                            if (superpositions[i].index(j) == 1 and superpositions[k].index(j) == 1):
                                superpositions[k][0], superpositions[k][1] = superpositions[k][1], superpositions[k][0]

                            if (superpositions[i].index(j) == 0 and superpositions[k].index(j) == 1):
                                superpositions[k][0], superpositions[k][1] = superpositions[k][1], superpositions[k][0]
                                superpositions[i][0], superpositions[i][1] = superpositions[i][1], superpositions[i][0]

                            if not j in already_set:




                                if not i in had:
                                    circ.h(i)
                                if not k in had:
                                    circ.h(k)
                                circ.ch(i, k)
                                circ.cx(i, k)
                                already_set.append(j)
                                had.append(i)
                                had.append(k)
        print(superpositions)
        return circ, superpositions


    def measure(self, circ):
        backend = Aer.get_backend('statevector_simulator')
        job = execute(circ, backend)
        result = job.result()
        counts = execute(circ, Aer.get_backend('qasm_simulator'), shots=1).result().get_counts()
        print(counts)
        res = [i for i in counts.keys()]
        print(res)
        return res[0]