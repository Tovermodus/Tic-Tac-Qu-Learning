#!/usr/bin/env python3

#from ..Interface import *


import numpy as np
from qiskit import QuantumCircuit
from qiskit import execute, Aer


def find_next_in_chain(flat_superpositions, index):
    for i in range(len(flat_superpositions)):
        if i == index:
            continue
        if flat_superpositions[i] == flat_superpositions[index]:
            return i
    return -1


def get_pair_index(index):
    print("index")
    print(index)
    if index % 2 == 1:
        print(index - 1)
        return index - 1
    else:
        print(index + 1)
        return index + 1
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

    def part_ent_circ(self, circ, superpositions):

        #        already_set = []
        #        had = []
        length = len(superpositions)
        flat_superpositions = []
        for i in range(length):
            flat_superpositions.append(superpositions[i][0])
            flat_superpositions.append(superpositions[i][1])
        print(flat_superpositions)
        entanglements = []
        flat_entanglements = []
        for i in range(len(flat_superpositions)):
            for j in range(i,len(flat_superpositions)):
                if flat_superpositions[i] in flat_entanglements or flat_superpositions[j] in flat_entanglements:
                    continue
                if flat_superpositions[i] == flat_superpositions[j]:
                    entanglement_position = len(entanglements)
                    entanglements.append([ flat_superpositions[get_pair_index(i)],flat_superpositions[i]])
                    flat_entanglements.append(flat_superpositions[i])
                    flat_entanglements.append(flat_superpositions[get_pair_index(i)])
                    print(i, get_pair_index(i))
                    chain_index = j
                    while find_next_in_chain(flat_superpositions, chain_index) != -1:
                        print(chain_index, get_pair_index(chain_index))
                        chain_index = get_pair_index(find_next_in_chain(flat_superpositions, chain_index))
                        entanglements[entanglement_position].append(flat_superpositions[chain_index])
                        entanglements[entanglement_position].append(flat_superpositions[get_pair_index(chain_index)])
                        flat_entanglements.append(get_pair_index(chain_index))
                        flat_entanglements.append(chain_index)
                        if flat_superpositions[chain_index] == entanglements[entanglement_position][0]:
                            break
        print("entanglements", entanglements)
        print(flat_entanglements)
    """
        print(entanglements)
        for i in range(length):
            for k in range(length):
                if i == k:
                    continue
                if(superpositions[i] == superpositions[k])
                    entanglement_position = len(entanglements)
                    entanglements.append()
                
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
    """

    def measure(self, circ):
        backend = Aer.get_backend('statevector_simulator')
        job = execute(circ, backend)
        result = job.result()
        counts = execute(circ, Aer.get_backend('qasm_simulator'), shots=1).result().get_counts()
        print(counts)
        res = [i for i in counts.keys()]
        print(res)
        return res[0]