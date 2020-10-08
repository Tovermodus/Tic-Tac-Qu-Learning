#!/usr/bin/env python3


#from ..Interface import *

import sys

from qiskit_circ import QiskitCircuitMaker


class Game():
    def __init__(self):
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.interface_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0]
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
                    if selectedType == 2:
                        self.superpositioncounter[player] += 1
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

            if isinstance(self.numbers[selectedfield], str):
                self.numbers[selectedfield] = f"{self.numbers[selectedfield]} {player}_{superpositionnumber}"
                if self.numbers[selectedfield][0] == "X" and self.numbers[selectedfield][0] == "X":
                    self.interface_numbers[selectedfield] = 4
                if self.numbers[selectedfield][0] == "O" and self.numbers[selectedfield][0] == "O":
                    self.interface_numbers[selectedfield] = 5
                if self.numbers[selectedfield][0] == "X" and self.numbers[selectedfield][0] == "O":
                    self.interface_numbers[selectedfield] = 3
                if self.numbers[selectedfield][0] == "O" and self.numbers[selectedfield][0] == "X":
                    self.interface_numbers[selectedfield] = 3
            else:
                self.numbers[selectedfield] = player + f"_{superpositionnumber}"
                if self.numbers[selectedfield][0] == "O":
                    self.interface_numbers[selectedfield] = 2
                if self.numbers[selectedfield][0] == "X":
                    self.interface_numbers[selectedfield] = 1
        else:
            self.numbers[selectedfield] = player
            if player == "X":
                self.interface_numbers[selectedfield] = 6
            if player == "O":
                self.interface_numbers[selectedfield] = 7



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
            X_win = self.check_for_win_comb("X")

            O_win = self.check_for_win_comb("X")

            if X_win and O_win:
                self.end(False)
                return 0
            elif X_win:
                self.end("X")
                return 1
            elif O_win:
                self.end("O")
                return -1

        win = self.check_for_win_comb(player)
        if win:
            winner = self.end(player)
            return winner
        else:
            return False

    def check_for_win_comb(self, player):
        win = False
        for winning_comb in self.winning_combs:
            for i in winning_comb:
                if self.numbers[i] != player:
                    win = False
                    break
                else:
                    win = True
            if win:
                return True
        return False


    def executeTurn(self, type, player):
        if type == 1:
            self.select_and_set_field(player, False, False)
        else:

            self.select_and_set_field(player, True, self.index[player])
            self.index[player] += 1
        self.print_table()

    def executeMachineTurn(self, field, player, type):
        if field not in self.numbers:
            return False
        if type not in (1, 2):
            return False
        if type == 1:
            self.set_field(field[0], player, False, False)
            return True
        else:
            self.set_field(field[0], player, True, self.index[player])
            self.set_field(field[1], player, True, self.index[player])
            self.index[player] += 1
            return True


    def set_end(self, q_res, superpositions):
        print(superpositions)
        for i in range(len(superpositions)-1,0, -1):
            index = int(q_res[i])
            pos = superpositions[i][index]
            player = self.superpositions_map[i]
            self.numbers[pos] = player
        for i in range(len(self.numbers)):
            if isinstance(self.numbers[i], int):
                self.numbers[i] = ""
            elif "X_" in self.numbers[i] or "O_" in self.numbers[i]:
                self.numbers[i] = ""

    def check_full(self, player):
        if all(isinstance(x, str) for x in self.numbers):
            print(self.superpositioncounter[player])
            if self.superpositioncounter[player] == 2:

                self.game_full = True
                self.final()
            else:
                pass

    def final(self):
        Q = QiskitCircuitMaker()
        circ, superpositions = Q.set_qiskit_superpos_circ(self.superpositions)
        res = Q.measure(circ)
        self.set_end(res, superpositions)
        self.print_table()
        winner = self.check_for_win(False, True)
        print(self.interface_numbers)
        return winner



    def end(self, winner):
        if winner:
            print(f"Player {winner} has won!")
            if winner == "X":
                return 1
            elif winner == "O":
                return -1
        else:
            print("Its a tie!")
            return 0

    def main(self):
        self.print_table()
        for i in range(5):

            machine = False
            # machine = isMachine()
            if machine:
                # fields, type = getAction(1, 1)
                # M.executeMachineTurn(fields, "X" , type)
                self.print_table()
            else:
                selectedType = self.select_type("X")
                self.executeTurn(selectedType, "X")
            self.check_full("X")
            winner = self.check_for_win("X")
            if winner is not False:
                sys.exit()
            if i == 4:
                break
            if machine:
                # fields, type = getAction(1, 1)
                # M.executeMachineTurn(fields, "O", type)
                self.print_table()
            else:
                selectedType = self.select_type("O")
                self.executeTurn(selectedType, "O")
            winner = self.check_for_win("O")
            if winner is not False:
                sys.exit()
            self.check_full("O")
        winner = self.final()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.main()


