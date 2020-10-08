from learning.NeuralNetwork import NeuralNetwork
from learning.NeuralNetwork import NeuralNetworkTrainer
import Interface
import numpy as np


class LearningEntry:
    def __init__(self, playerID, state, actionID, qValue):
        self.playerID = playerID
        self.state = state
        self.actionID = actionID
        self.qValue = qValue

    def compileFeature(self):
        return np.concatenate((self.state, [self.actionID, self.playerID]))


class QLearner:
    def __init__(self, playerID):
        self.playerID = playerID
        self.discountFactor = 0.5
        self.learningRate = 0.5
        self.neuralNet = NeuralNetwork()
        self.explorationT = 200
        self.learningEntries = []

    def Qvalue(self, actionID):
        return self.neuralNet.predict(LearningEntry(self.playerID, Interface.getCurrentState(), actionID, 0).compileFeature())

    def maximumReward(self, state):
        rewards = np.zeros(Interface.actions)
        for actionID in range(Interface.actions):
            rewards[actionID] = self.Qvalue(actionID)
        return np.max(rewards)

    def maximumFutureReward(self, actionID):
        return self.maximumReward(Interface.getStateAfterAction(self.playerID, actionID))

    def newQValue(self, actionID):
        return (1 - self.learningRate) * self.Qvalue(actionID) \
               + self.learningRate * (Interface.getReward(self.playerID,
                                                          actionID) + self.discountFactor * self.maximumFutureReward(actionID))

    def saveAction(self, actionID):
        self.learningEntries.append(LearningEntry(self.playerID, Interface.getCurrentState(), actionID, self.newQValue(actionID)))

    def refit(self):
        features = [le.compileFeature() for le in self.learningEntries]
        labels = [le.qValue for le in self.learningEntries]
        nnt = NeuralNetworkTrainer(self.neuralNet, features, labels)
        nnt.train()

    def nextAction(self):  # Maxwell Boltzmann Exploration
        expProbabilities = np.zeros(Interface.actions)
        probabilities = np.zeros(Interface.actions)
        for actionID in range(Interface.actions):
            expProbabilities[actionID] = np.exp(self.Qvalue(actionID) / self.explorationT)
        for actionID in range(Interface.actions):
            probabilities[actionID] = expProbabilities[actionID] / np.sum(expProbabilities)
        cumProbs = np.cumsum(probabilities)
        rand = np.random.rand()
        for i in range(Interface.actions - 1):
            if cumProbs[i] < rand < cumProbs[i + 1]:
                self.saveAction(i)
                return i
        return 0
