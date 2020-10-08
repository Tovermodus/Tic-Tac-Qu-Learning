#!/usr/bin/env python3

import numpy as np
import scipy.optimize as sopt
import scipy.special as ssp
import matplotlib.pyplot as plt
from qiskit import Aer
from quantumlayer import activation_function
from sklearn.neural_network import MLPRegressor

inputs = 7
firstLayerNodes = 6
secondLayerNodes = 6
thirdLayerNodes = 6
outputs = 1

def sigmoid(inputVector):
    return ssp.expit(inputVector)  # 1./(1+np.exp(-inputVector))


class QuantumNeuralNetwork:
    def __init__(self):
        self.k = 0
        self.inputWeights = np.random.rand(firstLayerNodes, inputs)
        self.firstLayerWeights = np.random.rand(secondLayerNodes, firstLayerNodes)
        self.secondLayerWeights = np.random.rand(thirdLayerNodes, secondLayerNodes)
        self.outputWeights = np.random.rand(outputs, thirdLayerNodes)
        self.simulator = Aer.get_backend('qasm_simulator')
        self.quantumLayer = activation_function(secondLayerNodes, lambda x: np.linalg.norm(x)*np.pi)
        # print(self.inputWeights.shape, self.firstLayerWeights.shape, self.secondLayerWeights.shape,
        # self.outputWeights.shape)

    def predict(self, features):  # jede Zeile ist ein feature
        if len(features.shape) == 1:
            features = np.array([features])
        firstLayerVector = sigmoid(np.matmul(self.inputWeights, features.T))
        secondLayerVector = np.zeros((firstLayerNodes, features.shape[0]))
        for i in range(features.shape[0]):
            feature = firstLayerVector[:,i]
            qresult = self.quantumLayer.run(np.dot(self.firstLayerWeights, feature), self.simulator, 1000)
            secondLayerVector[:,i] = qresult
        print(secondLayerVector.shape, self.k)
        self.k = self.k + 1
        #secondLayerVector = self.quantumLayer.run(np.matmul(self.firstLayerWeights, firstLayerVector), self.simulator, 1000)
        thirdLayerVector = sigmoid(np.matmul(self.secondLayerWeights, secondLayerVector))
        print(secondLayerVector.shape, thirdLayerVector.shape)
        # print(firstLayerVector.shape, secondLayerVector.shape, thirdLayerVector.shape)
        return np.matmul(self.outputWeights, thirdLayerVector)

    def updateWeights(self, inputWeights, firstLayerWeights, secondLayerWeights, outputWeights):
        self.inputWeights = inputWeights
        self.firstLayerWeights = firstLayerWeights
        self.secondLayerWeights = secondLayerWeights
        self.outputWeights = outputWeights

    # print(self.inputWeights.shape, self.firstLayerWeights.shape,self.secondLayerWeights.shape, self.outputWeights.shape)

    def evaluateError(self, features, labels):  # jede Zeile ist ein feature oder ein label
        nFeatures = features.shape[0]
        if nFeatures != labels.shape[0]:
            print("ERROR IN SHAPES")
        predictions = self.predict(features)
        return np.sum(np.square(predictions - labels))


class NeuralNetworkTrainer:
    def __init__(self, neuralNetwork, features, labels):
        self.labels = labels
        self.features = features
        self.neuralNetwork = neuralNetwork

    def optimizedFunction(self, flatWeights):
        splittedWeights = self.splitFlatWeights(flatWeights)
        self.neuralNetwork.updateWeights(splittedWeights[0], splittedWeights[1], splittedWeights[2], splittedWeights[3])
        return self.neuralNetwork.evaluateError(self.features, self.labels)

    def optimizationInitValue(self):
        flatWeights = np.concatenate(
            (self.neuralNetwork.inputWeights.flatten(), self.neuralNetwork.firstLayerWeights.flatten(),
             self.neuralNetwork.secondLayerWeights.flatten(), self.neuralNetwork.outputWeights.flatten()))
        return flatWeights

    def splitFlatWeights(self, flatWeights):
        startIndex = 0
        endIndex = inputs * firstLayerNodes
        flatInputWeights = flatWeights[startIndex:endIndex]
        startIndex = endIndex
        endIndex = endIndex + firstLayerNodes * secondLayerNodes
        flatFirstLayerWeights = flatWeights[startIndex:endIndex]
        startIndex = endIndex
        endIndex = endIndex + thirdLayerNodes * secondLayerNodes
        flatSecondLayerWeights = flatWeights[startIndex:endIndex]
        startIndex = endIndex
        endIndex = endIndex + outputs * thirdLayerNodes
        flatOutputWeights = flatWeights[startIndex:endIndex]
        inputWeights = np.reshape(flatInputWeights, (firstLayerNodes, inputs))
        firstLayerWeights = np.reshape(flatFirstLayerWeights, (secondLayerNodes, firstLayerNodes))
        secondLayerWeights = np.reshape(flatSecondLayerWeights, (thirdLayerNodes, secondLayerNodes))
        outputWeights = np.reshape(flatOutputWeights, (outputs, thirdLayerNodes))
        return inputWeights, firstLayerWeights, secondLayerWeights, outputWeights

    def train(self):
        splittedWeights = self.splitFlatWeights(sopt.minimize(self.optimizedFunction, self.optimizationInitValue(), method='trust-constr', options={ 'maxiter': 100}).x)
        self.neuralNetwork.updateWeights(splittedWeights[0], splittedWeights[1], splittedWeights[2], splittedWeights[3])


def trainedFunction(features):
    return np.sin(10 * features[:, 5] ** 2 + features[:, 1])


trainingSample = 100
feats = np.random.rand(trainingSample, 7)  # np.zeros((trainingSample, 7))#
labels = trainedFunction(feats)
nn = QuantumNeuralNetwork()
nnt = NeuralNetworkTrainer(nn, feats, labels)
mlp = MLPRegressor(random_state=1, max_iter=500).fit(feats, labels)

x = np.random.rand(trainingSample, 7)
x[:, 5] = np.linspace(0, 1, trainingSample)
print(nn.evaluateError(x, trainedFunction(x)))
nnt.train()
print(nn.evaluateError(x, trainedFunction(x)))

x = np.zeros((trainingSample, 7))
x[:, 5] = np.linspace(0, 1, trainingSample)
# plt.scatter(feats[:, 5], nn.predict(feats))
# plt.scatter(feats[:, 5], labels)
plt.scatter(x[:, 5], trainedFunction(x))
plt.scatter(x[:, 5], nn.predict(x))
plt.show()

plt.scatter(x[:, 5], trainedFunction(x))
plt.scatter(x[:, 5], mlp.predict(x))
plt.show()
#!/usr/bin/env python3
