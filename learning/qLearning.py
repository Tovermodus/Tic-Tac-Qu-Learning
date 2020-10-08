from learning.NeuralNetwork import NeuralNetwork
from learning.NeuralNetwork import NeuralNetworkTrainer
import Interface
import numpy as np


class LearningEntry:
    def __init__(self, playerID, boardState, actionID, qValue):
        self.playerID = playerID
        self.actionID = actionID
        self.qValue = qValue
        self.boardState = boardState
        self.lastActionID = 0

    def compileFeature(self):
        return np.concatenate((self.boardState, [self.actionID, self.playerID]))


class QLearner:
    def __init__(self, playerID):
        self.boardState = np.zeros(Interface.statusVariables)
        self.lastActionID = 0
        self.playerID = playerID
        self.discountFactor = 0.5
        self.learningRate = 0.5
        self.neuralNet = NeuralNetwork()
        self.explorationT = 200

        self.learningEntries = []

    def Qvalue(self, actionID):
        return self.neuralNet.predict(LearningEntry(self.playerID, self.boardState, actionID, 0).compileFeature())

    def maximumReward(self):
        rewards = np.zeros(Interface.actions)
        for actionID in range(Interface.actions):
            rewards[actionID] = self.Qvalue(actionID)
        return np.max(rewards)

    def maximumFutureReward(self):
        return self.maximumReward()

    def newQValue(self, actionID, reward):
        print(reward)
        return (1 - self.learningRate) * self.Qvalue(actionID) \
               + self.learningRate * (reward + self.discountFactor * self.maximumFutureReward())

    def saveLearningEntry(self, reward):
        self.learningEntries.append(LearningEntry(self.playerID, self.boardState, self.lastActionID, self.newQValue(self.lastActionID, reward)))

    def refit(self):
        features = [le.compileFeature() for le in self.learningEntries]
        labels = [le.qValue for le in self.learningEntries]
        nnt = NeuralNetworkTrainer(self.neuralNet, features, labels)
        nnt.train()

    def nextAction(self, interface):  # Maxwell Boltzmann Exploration
        self.boardState = interface.getCurrentBoardState()

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
                self.lastActionID = i
                return i
        self.lastActionID = 0
        return 0
