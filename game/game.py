#!/usr/bin/env python3

import sys
import numpy as np
import numpy as np
from qiskit import *

from qiskit import Aer
from qiskit.visualization import plot_state_city
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

from qiskit import QuantumCircuit



class Board():
    def __init__(self):
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.winning_combs = [[0, 1, 2], [0, 3, 6], [0, 4, 8],
                              [1, 4, 7], [2, 5, 8], [6, 7, 8],
                              [3, 4, 5], [2, 4, 6]]
        self.game_full = False
        self.moves = []
        self.superpositions_map = []
        self.superpositions = []
        self.superpositioncounter = {"X": 0, "O": 0}



    def print_table(self):

        print("     ")
        for i in range(0, 8, 3):
            print("  {:^7} | {:^7} | {:^7} ".format(self.numbers[i], self.numbers[i + 1], self.numbers[i + 2]))
            if i > 4:
                print("     ")
                continue
            print("  ________ ________ ________")

class Move(Board):

    def select_type(self, player):
        selected = False
        while not selected:
            try:
                selectedType = int(input("Select 1 for classical or 2 for quantum move."))
                if selectedType not in [1, 2]:
                    pass
                elif selectedType == 2 and self.superpositioncounter[player] > 2:
                    print("You've already made 2 quantum moves!")
                    pass
                else:
                    return selectedType
            except:
                print("Pick correct number!")

    def select_field(self):
        selected = False
        while not selected:
            try:
                selectedNumber = int(input("Select available field"))
                if isinstance(self.numbers[selectedNumber], str):
                    if "_" in self.numbers[selectedNumber]:
                        if not len(str(self.numbers[selectedNumber])) > 6:
                            return selectedNumber
                        else:
                            print("Field already filled to maximum.")

                else:
                    return selectedNumber
            except:
                print("Pick correct number!")

    def set_field(self, selectedfield, player, superposition, superpositionnumber=1):
        if superposition:
            self.superpositioncounter[player] += 1
            if isinstance(self.numbers[selectedfield], str):

                self.numbers[selectedfield] = f"{self.numbers[selectedfield]} {player}_{superpositionnumber}"
            else:
                self.numbers[selectedfield] = player + f"_{superpositionnumber}"
        else:
            self.numbers[selectedfield] = player



    def set_superposition(self, super1, super2, player):
        lis = [super1, super2]
        lis.sort()
        self.superpositions_map.append(player)
        self.superpositions.append(lis)

    def select_and_set_field(self, player, superpos, super_iter):
        if superpos:
            field_1 = self.select_field()
            field_2 = self.select_field()
            self.set_superposition(field_1, field_2, player)
            self.set_field(field_1, player, True, super_iter)
            self.set_field(field_2, player, True, super_iter)
        else:
            field = self.select_field()
            self.set_field(field, player, False)


    def check_for_win(self, player):
        win = False
        for winning_comb in self.winning_combs:
            for i in winning_comb:
                if self.numbers[i] != player:
                    win = False
                    break
                else:
                    win = True
            if win:
                end(player)



    def set_end(self, q_res):
        for i in range(len(self.superpositions)):
            index = int(q_res[i])
            pos = self.superpositions[i][index]
            player = self.superpositions_map[i]
            self.numbers[pos] = player



def end(winner):
    print(f"Player {winner} has won!")
    sys.exit()




class QiskitCircuitMaker():

    def set_qiskit_superpos_circ(self, superpositions):
        #self.superpositions.append([0,1])
        already_set_cx = []
        length = len(superpositions)

        initial_state = [0, 1]
        circ = QuantumCircuit(length, length)

        flag = False

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
                            circ.initialize(initial_state, k)
                            circ.cx(i, k)
                            already_set_cx.append(lis)
                            """superpositions = [superposition for superposition in 
                                              superpositions if superposition != superpositions[k]]"""
        for i in range(length):
            for j in range(length):
                """
                if superpositions[i][0] not in j:
                    continue
                else:
                    flag = True
                """
                print("")

        measure_list = [i for i in range(length)]
        circ.measure(measure_list, measure_list)
        print(circ.draw())
        return circ



def measure(circ):
    backend = Aer.get_backend('statevector_simulator')
    job = execute(circ, backend)
    result = job.result()
    counts = execute(circ, Aer.get_backend('qasm_simulator'), shots=1).result().get_counts()
    print(counts)
    res = [i for i in counts.keys()]
    print(res)
    return res[0]


def main():
    M = Move()
    i1 = 1
    i2 = 1
    for i in range(5):
        M.print_table()
        selectedType = M.select_type("X")
        if selectedType == 1:
            M.select_and_set_field("X", False, False)
        else:

            M.select_and_set_field("X", True, i1)
            i1 += 1

        M.print_table()

        M.check_for_win("X")
        if i == 4:
            break
        selectedType = M.select_type("O")
        if selectedType == 1:

            M.select_and_set_field("O", False, False)

        else:
            M.select_and_set_field("O", True, i2)
            i2 += 1

        M.check_for_win("O")
    Q = QiskitCircuitMaker()
    circ = Q.set_qiskit_superpos_circ(M.superpositions)
    res = measure(circ)
    M.set_end(res)
    M.print_table()


if __name__ == "__main__":
    main()

