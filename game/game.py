#!/usr/bin/env python3

import sys
#from ..Interface import *
from qiskit import *



from qiskit import QuantumCircuit, execute, Aer
from qiskit import QuantumCircuit
import numpy as np



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


        self.index = {"X": 1, "O": 1}

    def print_table(self):

        print("     ")
        for i in range(0, 8, 3):
            print("  {:^7} | {:^7} | {:^7} ".format(self.numbers[i], self.numbers[i + 1], self.numbers[i + 2]))
            if i > 4:
                print("     ")
                continue
            print("  ________ ________ ________")

class Move(Board):


    def select_type(self, player, machine=False):
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

    def select_field(self, machine=False):
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


    def check_for_win(self, player, ending=False):
        win = False
        X_win = False
        O_win =False
        if ending:
            for winning_comb in self.winning_combs:
                for i in winning_comb:
                    if self.numbers[i] != "X":
                        win = False
                        break
                    else:
                        win = True
                if win:
                    X_win = True
                    break
            win = False
            for winning_comb in self.winning_combs:
                for i in winning_comb:
                    if self.numbers[i] != "O":
                        win = False
                        break
                    else:
                        win = True
                if win:
                    O_win = True
                    break
            if X_win and O_win:
                end(False)
            elif X_win:
                end("X")
            elif O_win:
                end("O")

        for winning_comb in self.winning_combs:
            for i in winning_comb:
                if self.numbers[i] != player:
                    win = False
                    break
                else:
                    win = True
            if win:
                end(player)

    def executeTurn(self, type, player):
        if type == 1:
            self.select_and_set_field(player, False, False)
        else:

            self.select_and_set_field(player, True, self.index[player])
            self.index[player] += 1
        self.print_table()

    def executeMachineTurn(self, field, player, type):
        if type == 1:
            self.set_field(field[0], player, False, False)
        else:
            self.set_field(field[0], player, True, self.index[player])
            self.set_field(field[1], player, True, self.index[player])
            self.index[player] += 1

    def set_end(self, q_res):
        for i in range(len(self.superpositions)):
            index = int(q_res[i])
            pos = self.superpositions[i][index]
            player = self.superpositions_map[i]
            self.numbers[pos] = player
        for i in range(len(self.numbers)):
            if isinstance(self.numbers[i], int):
                self.numbers[i] = ""
            elif "X_" in self.numbers[i] or "O_" in self.numbers[i]:
                self.numbers[i] = ""

    def check_full(self):
        if all(isinstance(x, str) for x in self.numbers):
            self.game_full = True
            self.final()

    def final(self):
        Q = QiskitCircuitMaker()
        circ = Q.set_qiskit_superpos_circ(self.superpositions)
        res = measure(circ)
        self.set_end(res)
        self.print_table()
        self.check_for_win(False, True)
        sys.exit()




def end(winner):
    if winner:
        print(f"Player {winner} has won!")
        sys.exit()
    else:
        print("Its a tie!")




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
        return circ

    def set_single_circ(self, circ, superpositions):

        ### create a copy of the superposition list that is flat
        superpositions_flat = []
        for i in range(len(superpositions)):
            for j in range(2):
                superpositions_flat.append(superpositions[i][j])

        ### find the unique numbers in that list and how many counts of that number there are.
        uniq, uniq_counts = np.unique(superpositions, return_counts=True, axis=None)

        # find the numbers (fields in the game) that have only one superposition on them and output
        true_uniq = []
        for i in range(len(uniq_counts)):
            if uniq_counts[i] == 1:
                true_uniq.append(uniq[i])

        pos = []
        for i in range(len(true_uniq)):
            pos.append(superpositions_flat.index(true_uniq[i]))

        pos = np.array(pos)
        pos_qbits = pos // 2
        # print('pos_qbits in true_uinqe fields arraay=', pos_qbits,'\n')

        # print('Following fields are only ocupied by one superposition: ')
        # for i in range(len(true_uniq)):
        # print('Field:', true_uniq[i], 'with qbit:', pos_qbits[i])

        ### find qbits that are not entagled with other qbit's
        single_qbits, single_qbits_counts = np.unique(pos_qbits, return_counts=True)

        n_ent_qbits = []
        for i in range(len(single_qbits_counts)):
            if single_qbits_counts[i] == 2:
                n_ent_qbits.append(i)
                # print('qbit:', i, 'is not entangeled')

        # draw circuit for the qbits that are not entagled
        for i in range(len(n_ent_qbits)):
            circ.h(n_ent_qbits[i])
            #circ.measure(n_ent_qbits[i], n_ent_qbits[i])

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


def machine_input():
    return





def main():

    M = Move()
    for i in range(5):
        M.print_table()
        machine = False
        #machine = isMachine()
        if machine:
            #fields, type = getAction(1, 1)
            #M.executeMachineTurn(fields, "X" , type)
            M.print_table()
        else:
            selectedType = M.select_type("X")
            M.executeTurn(selectedType, "X")
        M.check_full()
        M.check_for_win("X")
        if i == 4:
            break
        if machine:
            #fields, type = getAction(1, 1)
            #M.executeMachineTurn(fields, "O", type)
            M.print_table()
        else:
            selectedType = M.select_type("O")
            M.executeTurn(selectedType, "O")
        M.check_for_win("O")
        M.check_full()
    M.final()





if __name__ == "__main__":
    main()


