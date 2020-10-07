#!/usr/bin/env python3

import numpy as np

inputs = 17
firstLayerNodes = 10
secondLayerNodes = 5
thirdLayerNodes = 10
outputs = 1

def sigmoid(inputVector):
    return 1./(1+np.exp(-inputVector))

class NeuralNetwork:
    def __init__(self):
        self.inputWeights = np.random.rand(firstLayerNodes, inputs)
        self.firstLayerWeights = np.random.rand(secondLayerNodes, firstLayerNodes)
        self.secondLayerWeights = np.random.rand(thirdLayerNodes, secondLayerNodes)
        self.outputWeights = np.random.rand(outputs, thirdLayerNodes)

    def predict(self, features): #jede Zeile ist ein feature
        if(len(inputVector.shape) == 1)
           inputVector = np.array([inputVector])
        firstLayerVector = sigmoid(np.matmul(self.inputWeights,inputVector.T))
        secondLayerVector = sigmoid(np.matmul(self.firstLayerWeights,firstLayerVector))
        thirdLayerVector = sigmoid(np.matmul(self.secondLayerWeights,secondLayerVector))
        return np.matMul(self.outputWeights, thirdLayerVector).T

    def updateWeights(self, inputWeights, firstLayerWeights, secondLayerWeights, outputWeights):
        self.inputWeights = inputWeights
        self.firstLayerWeights = firstLayerWeights
        self.secondLayerWeights = secondLayerWeights
        self.outputWeights = outputWeights

    def evaluateError(self, features, labels):  #jede Zeile ist ein feature oder ein label
        n_features = features.shape[0]
        if(n_features != labels.shape[0]):
            print("ERROR IN SHAPES")
        predictions = predict(features)
        return np.sum(np.square(predictions - labels))

class NeuralNetworkTrainer:
    def __init__(self, neuralNetwork):
        self.neuralNetwork = neuralNetwork

    def initializeTrainingSet(self, features, labels):
        self.features = features
        self.labels = labels

    def optimizedFunction(self, flatweights):
