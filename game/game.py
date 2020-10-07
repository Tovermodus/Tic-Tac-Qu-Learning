#!/usr/bin/env python3

import sys
import qiskit as qs

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
winning_combs = [[0, 1, 2], [0, 3, 6], [0, 4, 8], [1, 4, 7], [2, 5, 8], [6, 7, 8], [3, 4, 5], [2, 4, 6]]

superpositions_map = {"X": [], "O": []}
superpositions = []

def print_table(numbers):

    print("     ")
    for i in range(0, 8, 3):
        print("  {:^7} | {:^7} | {:^7} ".format(numbers[i], numbers[i+1], numbers[i+2]))
        if i > 4:
            print("     ")
            continue
        print("  ________ ________ ________")


def select_type():
    selected = False
    while not selected:
        try:
            selectedType = int(input("Select 1 for classical or 2 for quantum move."))
            if selectedType not in [1, 2]:
                pass
            else:
                return selectedType
        except:
            print("Pick correct number!")

def select_field():
    selected = False
    while not selected:
        try:
            selectedNumber = int(input("Select available field"))
            if isinstance(numbers[selectedNumber], str):
                if "_" in numbers[selectedNumber]:
                    if not len(str(numbers[selectedNumber])) > 6:
                        return selectedNumber
                    else:
                        print("Field already filled to maximum.")

            else:
                return selectedNumber
        except:
            print("Pick correct number!")

def set_field(selectedfield, player, superposition, superpositionnumber=1):
    if superposition:
        if isinstance(numbers[selectedfield], str):

            numbers[selectedfield] = f"{numbers[selectedfield]} {player}_{superpositionnumber}"
        else:
            numbers[selectedfield] = player + f"_{superpositionnumber}"
    else:
        numbers[selectedfield] = player



def set_superposition(super1, super2, player):
    superpositions_map[player].append([super1, super2])
    superpositions.append([super1, super2])


def check_for_win(player):
    win = False
    for winning_comb in winning_combs:
        for i in winning_comb:
            if numbers[i] != player:
                win = False
                break
            else:
                win = True
        if win:
            end(player)

def end(winner):
    print(f"Player {winner} has won")
    sys.exit()



def select_and_set_field(player, superpos, super_iter):
    if superpos:
        field_1 = select_field()
        field_2 = select_field()
        set_superposition(field_1, field_2, player)
        set_field(field_1, player, True, super_iter)
        set_field(field_2, player, True, super_iter)
    else:
        field = select_field()
        set_field(field, player, False)


def set_qiskit_super():
    length = len(superpositions)
    circ = qs.QuantumCircuit(length, length)
    circ.h(0)
    initial_state = [0, 1]


def measure():
    pass


def main():
    i1 = 1
    i2 = 1
    for i in range(5):
        print_table(numbers)
        selectedType = select_type()
        if selectedType == 1:
            select_and_set_field("X", False, False)
        else:

            select_and_set_field("X", True, i1)
            i1 += 1

        print_table(numbers)

        check_for_win("X")

        selectedType = select_type()
        if selectedType == 1:

            select_and_set_field("O", False, False)

        else:
            select_and_set_field("O", True, i2)
            i2 += 1

        check_for_win("O")


if __name__ == "__main__":
    main()