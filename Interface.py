import game.game as game
import learning.qLearning as learning
import numpy as np

learner1 = learning.QLearner(0)
learner2 = learning.QLearner(1)
actions = 30
statusVariables = 20



def gameBoardStatusToLearningBoardStatus(gameBoardStatus):
    print()

def gameResultToLearningReward(gameResult):
    print()

def learningActionToGameAction(learningAction):
    print()

def sendResult(gameResult):
    print()

def getReward(playerId, actionID):
    print()

def getAction(playerId, state): #Die Hauptspielschleife fragt ab was die KI tut
    print()

    #return [0],1    #klassischer Zug links oben
    #return [0,1],2  #Superposition links oben, mitte oben
def sendReward():


def getCurrentBordState():
    return np.zeros(statusVariables)

def getStateAfterAction(playerId, actionID):
    print()