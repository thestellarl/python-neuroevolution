import math
import numpy as np

class NN:
    def __init__(self, w1 = None, w2 = None):
        if(w1 == None and w2 == None):
            self.weights1 = (np.random.rand(3, 4) - .5) * 2
            self.weights2 = (np.random.rand(4, 2) - .5) * 2
        else:
            self.weights1 = w1
            self.weights2 = w2
        self.output = np.zeros((2, 1))

    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))

    def sigmoid_derivative(x):
        return x * (1.0 - x)

    def feedforward(self, x):
        self.input = x
        #print(self.input[3])
        self.layer1 = self.sigmoid(np.dot(self.input, self.weights1))
        self.output = self.sigmoid(np.dot(self.layer1, self.weights2))

    # def backprop(self, y):
    #     # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
    #     d_weights2 = np.dot(self.layer1.T, (2 * (self.y - self.output) * self.sigmoid_derivative(self.output)))
    #     d_weights1 = np.dot(self.input.T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output),
    #                                               self.weights2.T) * self.sigmoid_derivative(self.layer1)))
    #     # update the weights with the derivative (slope) of the loss function
    #     self.weights1 += d_weights1
    #     self.weights2 += d_weights2
