#!/usr/bin/env python3

#from ..Interface import *


import numpy as np
from qiskit import QuantumCircuit
from qiskit import execute, Aer
from copy import deepcopy


def find_next_in_chain(flat_superpositions, index):
    for i in range(len(flat_superpositions)):
        if i == index:
            continue
        if flat_superpositions[i] == flat_superpositions[index]:
            return i
    return -1


def get_pair_index(index):
    if index % 2 == 1:
        return index - 1
    else:
        return index + 1


def getOriginalState(entanglement, stateIndex, superpositions,eliminate=False):
    state = [entanglement[2*stateIndex],entanglement [2*stateIndex+1]]
    if state in superpositions:
        ind = superpositions.index(state)
        if eliminate:
            superpositions[ind] = [-1,-1]
        return False, ind
    state = [entanglement[2*stateIndex+1],entanglement [2*stateIndex]]
    if state in superpositions:
        ind = superpositions.index(state)
        if eliminate:
            superpositions[ind] = [-1,-1]
        return True, ind
    return "Error"


class QiskitCircuitMaker():

    def __init__(self):
        self.initial_state = [0, 1]

    def set_qiskit_superpos_circ(self, superpositions):


        length = len(superpositions)

        initial_state = [0, 1]
        circ = QuantumCircuit(length, length)
        entanglements = self.identify_entanglements(superpositions)
        print(entanglements, "aksjdhalksj")
        new_superpositions = []
        for e in entanglements:
            if(e[0] == e[-1]):
                circ, superpositions = self.set_loop_circ(circ, e, deepcopy(superpositions))
            else:
                circ, superpositions = self.set_chain_circ(circ, e, deepcopy(superpositions))
            for i in range(len(e)//2):
                new_superpositions.append([e[i*2],e[i*2+1]])
            #circ.measure
        print(len(entanglements))
        measure_list = [i for i in range(length)]
        circ.measure(measure_list, measure_list)
        print(circ.draw())
        return circ, new_superpositions

    def set_loop_circ(self, circ, entanglement, superpositions):
        print("loop")
        if(len(entanglement) != 4):
            invert, index = getOriginalState(entanglement, 0, superpositions)
        else:
            invert, index = getOriginalState(entanglement, 0, superpositions, eliminate=True)
        circ.h(index)
        for i in range((len(entanglement)-2)//2):
            invert, index = getOriginalState(entanglement, i, superpositions)
            invertp, indexp = getOriginalState(entanglement, i+1, superpositions)
            circ.cx(index, indexp)
        return circ, superpositions

    def set_chain_circ(selfself, circ, entanglement, superpositions):
        print("chain")
        for i in range(len(entanglement)//2):
            invert, index = getOriginalState(entanglement, i, superpositions)
            circ.h(index)
        for i in range((len(entanglement)-2)//2):
            invert, index = getOriginalState(entanglement, i, superpositions)
            invertp, indexp = getOriginalState(entanglement, i+1, superpositions)
            circ.ch(index, indexp)
            circ.cx(index, indexp)
        return circ, superpositions


    def identify_entanglements(self, superpositions):

        #        already_set = []
        #        had = []
        length = len(superpositions)
        flat_superpositions = []
        for i in range(length):
            flat_superpositions.append(superpositions[i][0])
            flat_superpositions.append(superpositions[i][1])
        entanglements = []
        flat_entanglements = []
        for i in range(len(flat_superpositions)):
            for j in range(i,len(flat_superpositions)):
                if i == j:
                    continue
                if i in flat_entanglements or j in flat_entanglements:
                    continue
                if flat_superpositions[i] == flat_superpositions[j]:
                    chain_ends = [i, j]
                    entanglement_position = len(entanglements)
                    entanglements.append([])
                    flat_entanglements.append(chain_ends[0])
                    flat_entanglements.append(chain_ends[1])
                    flat_entanglements.append(get_pair_index(chain_ends[1]))
                    while len(chain_ends) > 0:
                        chain_pair = get_pair_index(chain_ends[0])
                        if(len(chain_ends) == 2):
                            entanglements[entanglement_position] = [flat_superpositions[chain_ends[0]]]+entanglements[entanglement_position]
                            entanglements[entanglement_position] = [flat_superpositions[chain_pair]]+entanglements[entanglement_position]
                        if(len(chain_ends) == 1):
                            entanglements[entanglement_position] = entanglements[entanglement_position] + [flat_superpositions[chain_ends[0]]]
                            entanglements[entanglement_position] = entanglements[entanglement_position] + [flat_superpositions[chain_pair]]
                        flat_entanglements.append(chain_pair)
                        flat_entanglements.append(chain_ends[0])
                        if find_next_in_chain(flat_superpositions, chain_pair) == -1:
                            chain_ends.remove(chain_ends[0])
                            continue

                        next_chain = find_next_in_chain(flat_superpositions, chain_pair)
                        if next_chain in flat_entanglements:
                            entanglements[entanglement_position] = entanglements[entanglement_position] + [flat_superpositions[chain_ends[1]]]
                            entanglements[entanglement_position] = entanglements[entanglement_position] + [flat_superpositions[get_pair_index(chain_ends[1])]]
                            chain_ends.remove(chain_ends[0])
                            break
                        chain_ends[0] = next_chain
        return entanglements

    def measure(self, circ):
        backend = Aer.get_backend('statevector_simulator')
        job = execute(circ, backend)
        result = job.result()
        counts = execute(circ, Aer.get_backend('qasm_simulator'), shots=1).result().get_counts()
        print(counts)
        res = [i for i in counts.keys()]
        print(res)
        return res[0]