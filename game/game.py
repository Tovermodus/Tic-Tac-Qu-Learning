#!/usr/bin/env python3
numbers = [["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"]]
def print_table(numbers):

    print("     ")
    print("  {:^5} | {:^5} | {:^5} ".format(''.join(numbers[0]), ''.join(numbers[1]), ''.join(numbers[2])))
    print("  ______ ______ ______")
    print("  {:^5} | {:^5} | {:^5} ".format(''.join(numbers[3]), ''.join(numbers[4]), ''.join(numbers[5])))
    print("  ______ ______ ______")
    print("  {:^5} | {:^5} | {:^5} ".format(''.join(numbers[6]), ''.join(numbers[7]), ''.join(numbers[8])))
    print("     ")
    print(" ")


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
            print("Pick correct number")

def select_field():
    selected = False
    while not selected:
        try:
            selectedNumber = str(input("Select available field"))
            if [selectedNumber] not in numbers:
                pass
            else:
                return selectedNumber
        except:
            print("Pick correct number")

def set_field(selectedfield, player, superposition, superpositionnumber=1):
    if superposition:
        if isinstance(numbers[selectedfield], str):
            numbers[selectedfield] = [numbers[selectedfield]]
            numbers[selectedfield].append(player + f"_{superpositionnumber}")
        else:
            numbers[selectedfield] = player + f"_{superpositionnumber}"
    else:
        numbers[selectedfield] = player




def main():
    end = False
    player_1 = "X"
    player_2 = "O"
    i1 = 1
    i2 = 1
    while not end:
        print_table(numbers)
        selectedType = select_type()
        if selectedType == 1:
            field = select_field()
            set_field(field, player_1, False)
        else:

            field_1 = select_field()
            field_2 = select_field()
            set_field(field_1, player_1, True, i1)
            set_field(field_2, player_1, True, i1)
            i1 += 1

        print_table(numbers)
        selectedType = select_type()
        if selectedType == 1:

            field = select_field()
            set_field(field, player_2, False)

        else:
            field_1 = select_field()
            field_2 = select_field()
            set_field(field_1, player_2, True, i2)
            set_field(field_2, player_2, True, i2)
            i2 += 1

main()