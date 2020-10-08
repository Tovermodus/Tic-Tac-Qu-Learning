from learning.NeuralNetwork import NeuralNetwork
import Interface
import numpy as np



class QLearner:
    def __init__(self, playerID):
        self.playerID = playerID
        self.discountFactor = 0.5
        self.learningRate = 0.5
        self.neuralNet = NeuralNetwork()
        self.explorationT = 200


    def Qvalue(self, actionID):
        return self.neuralNet.predict(np.concatenate((Interface.getCurrentState(),[actionID])))

    def maximumReward(self, state):
        rewards = np.zeros(Interface.actions)
        for actionID in range(Interface.actions):
            rewards[actionID] = self.Qvalue(actionID)
        return np.max(rewards)

    def maximumFutureReward(self, actionID):
        return self.maximumReward(Interface.getStateAfterAction(self.playerID, actionID))

    def newQValue(self, actionID):
        return (1-self.learningRate)*self.Qvalue(actionID) \
               + self.learningRate*(Interface.getReward(self.playerID, actionID) + self.discountFactor*self.maximumFutureReward(actionID))



    def nextAction(self): #Maxwell Boltzmann Exploration
        expProbabilities = np.zeros(Interface.actions)
        probabilities = np.zeros(Interface.actions)
        for actionID in range(Interface.actions):
            expProbabilities[actionID] = np.exp(self.Qvalue(actionID)/self.explorationT)
        for actionID in range(Interface.actions):
            probabilities[actionID] = expProbabilities[actionID]/np.sum(expProbabilities)
        cumProbs = np.cumsum(probabilities)
        rand = np.random.rand()
        for i in range(Interface.actions-1):
            if(rand>cumProbs[i] && rand < cumProbs[i+1])
                return i
        return 0
