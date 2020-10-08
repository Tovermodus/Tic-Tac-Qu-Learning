import game.game as game
import learning.qLearning as learning
import numpy as np
import conversions
from copy import deepcopy

actions = 30
statusVariables = 20
ql1 = learning.QLearner(0)
ql2 = learning.QLearner(1)
g = game.Game()
statusVariables = 20


def main():
    for i in range(5):
        g.print_table()
        machine = False
        # machine = isMachine()
        allowed = True
        win = 0
        if isMachine("X"):
            fields, type = getAction(0)
            allowed = g.executeMachineTurn(fields, "X", type)
            g.print_table()
            g.check_full()
            win = g.check_for_win("X")
            sendResult(0,[allowed, win])
        else:
            selectedType = g.select_type("X")
            g.executeTurn(selectedType, "X")
            g.check_full()
            g.check_for_win("X")

        if i == 4:
            break
        if machine:
            fields, type = getAction(1)
            allowed = g.executeMachineTurn(fields, "O", type)
            g.print_table()
            g.check_full()
            win = g.check_for_win("X")
            sendResult(1,[allowed, win])
        else:
            selectedType = g.select_type("O")
            g.executeTurn(selectedType, "O")
        g.check_for_win("O")
        g.check_full()
    g.final()


def sendResult(playerID, gameResult):
    reward = conversions.gameResultToLearningReward(gameResult)
    if playerID == 0:
        ql1.saveLearningEntry(reward)
    elif playerID == 1:
        ql2.saveLearningEntry(reward)


def isMachine(playerName):
    return False


def getAction(playerID):
    actionID = 0
    if playerID == 0:
        actionID = ql1.nextAction()
    elif playerID == 1:
        actionID = ql2.nextAction()
    return conversions.learningActionToGameAction(actionID)


    #return [0],1    #klassischer Zug links oben
    #return [0,1],2  #Superposition links oben, mitte oben


def getCurrentBoardState():
    return g.get_board_state()


def getStateAfterAction(playerID, actionID):
    fields, type = conversions.learningActionToGameAction(actionID)
    copygame = deepcopy(g)
    if playerID == 0:
        copygame.executeMachineTurn(fields, "X", type)
    elif playerID == 1:
        copygame.executeMachineTurn(fields, "X", type)
    return copygame.get_board_state()


if __name__ == "__main__":
    main()
