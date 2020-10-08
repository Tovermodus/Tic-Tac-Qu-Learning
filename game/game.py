#!/usr/bin/env python3


from .qiskit_circ import *
#from ..Interface import *

import sys

from game.qiskit_circ import QiskitCircuitMaker


class Game():
    def __init__(self):
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.interface_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.winning_combs = [[0, 1, 2], [0, 3, 6], [0, 4, 8],
                              [1, 4, 7], [2, 5, 8], [6, 7, 8],
                              [3, 4, 5], [2, 4, 6]]
        self.game_full = False
        self.moves = []
        self.superpositions_map = []
        self.superpositions = []
        self.superpositioncounter = {"X": 0, "O": 0}
        self.only_quantum = False


        self.index = {"X": 1, "O": 1}

    def print_table(self):

        print("     ")
        for i in range(0, 8, 3):
            print("  {:^7} | {:^7} | {:^7} ".format(self.numbers[i], self.numbers[i + 1], self.numbers[i + 2]))
            if i > 4:
                print("     ")
                continue
            print("  ________ ________ ________")




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
                self.end(False)
            elif X_win:
                self.end("X")
            elif O_win:
                self.end("O")

        for winning_comb in self.winning_combs:
            for i in winning_comb:
                if self.numbers[i] != player:
                    win = False
                    break
                else:
                    win = True
            if win:
                self.end(player)

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
        return False

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
            if self.superpositioncounter["X"] == 2 and self.superpositioncounter["O"] == 2:

                self.game_full = True
                self.final()
            else:
                pass

    def final(self):
        Q = QiskitCircuitMaker()
        circ = Q.set_qiskit_superpos_circ(self.superpositions)
        res = Q.measure(circ)
        self.set_end(res)
        self.print_table()
        self.check_for_win(False, True)
        sys.exit()




    def end(self, winner):
        if winner:
            print(f"Player {winner} has won!")
            sys.exit()
        else:
            print("Its a tie!")

    def get_board_state(self):
        return self.interface_numbers



