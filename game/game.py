#!/usr/bin/env python3

import sys

from qiskit import QuantumCircuit

class Board():
    def __init__(self):
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.winning_combs = [[0, 1, 2], [0, 3, 6], [0, 4, 8],
                              [1, 4, 7], [2, 5, 8], [6, 7, 8],
                              [3, 4, 5], [2, 4, 6]]
        self.game_full = False
        self.moves = []
        self.superpositions_map = {"X": [], "O": []}
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
        self.superpositions_map[player].append([super1, super2])
        self.superpositions.append([super1, super2])

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

def end(winner):
    print(f"Player {winner} has won!")
    sys.exit()




class QiskitCircuitMaker(Board):

    def set_qiskit_superpos_circ(self):
        #self.superpositions.append([0,1])
        already_set_cx = []
        self.superpositions = [[1,2], [2,3], [1,2], [2,8]]
        length = len(self.superpositions)
        print(length)
        initial_state = [0, 1]
        circ = QuantumCircuit(length, length)
        circ.h(0)
        for i in range(length):
            for k in range(length):
                if self.superpositions[i] == self.superpositions[k]:

                    if i == k:
                        continue
                    else:
                        lis = [i, k].sort()
                        if not lis in already_set_cx:
                            circ.initialize(initial_state, k)
                            circ.cx(i, k)
                            already_set_cx.append(lis)
                    





        print(circ.draw())


def measure():
    pass


def main():
    B = Board()
    M = Move()
    i1 = 1
    i2 = 1
    for i in range(5):
        B.print_table()
        selectedType = M.select_type("X")
        if selectedType == 1:
            M.select_and_set_field("X", False, False)
        else:

            M.select_and_set_field("X", True, i1)
            i1 += 1

        B.print_table()

        M.check_for_win("X")

        selectedType = M.select_type("O")
        if selectedType == 1:

            M.select_and_set_field("O", False, False)

        else:
            M.select_and_set_field("O", True, i2)
            i2 += 1

        M.check_for_win("O")


if __name__ == "__main__":
    #main()
    Q = QiskitCircuitMaker()
    Q.set_qiskit_superpos_circ()

