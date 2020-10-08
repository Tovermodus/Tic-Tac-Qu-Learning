import game.game as game
import learning.qLearning as learning
import numpy as np

actions = 30
statusVariables = 20
ql1 = learning.QLearner(0)
ql2 = learning.QLearner(1)
g = game.Game()
statusVariables = 20



def gameBoardStatusToLearningBoardStatus(gameBoardStatus):
    print()

def main(self):
    for i in range(5):
        g.print_table()
        machine = False
        # machine = isMachine()
        if machine:
            # fields, type = getAction(1, 1)
            # M.executeMachineTurn(fields, "X" , type)
            g.print_table()
        else:
            selectedType = g.select_type("X")
            g.executeTurn(selectedType, "X")
        g.check_full()
        g.check_for_win("X")
        if i == 4:
            break
        if machine:
            # fields, type = getAction(1, 1)
            # M.executeMachineTurn(fields, "O", type)
            g.print_table()
        else:
            selectedType = self.select_type("O")
            g.executeTurn(selectedType, "O")
        g.check_for_win("O")
        g.check_full()
    g.final()

def createGameFromStatus(status):
    print()
    #board = Board()
    #board.initialize()
def gameResultToLearningReward(gameResult):
    print()

def learningActionToGameAction(learningAction):
    print()

def sendResult(gameResult):
    print()



def isMachine():
    return False


def getAction(playerId, state): #Die Hauptspielschleife fragt ab was die KI tut
def getReward(playerId, actionID):
    print()

    #return [0],1    #klassischer Zug links oben
    #return [0,1],2  #Superposition links oben, mitte oben

def getCurrentState():
    return np.zeros(statusVariables)
def getAction(playerId, state): #Die Hauptspielschleife fragt ab was die KI tut
    print()

    #return [0],1    #klassischer Zug links oben
    #return [0,1],2  #Superposition links oben, mitte oben
def sendReward():


def getCurrentBoardState():
    return np.zeros(statusVariables)

def getStateAfterAction(playerId, actionID):
    print()
