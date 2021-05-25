
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
from myModel import *
from const import *

def train():
    #load data
    pairedData = torch.load("mydataset.dat")
    #print(pairedData)
    #first 2 columns
    inputData = pairedData.narrow(1, 0, 2)
    #last column
    outputData = pairedData.narrow(1, 2, 1)

    #split the tensors
    splitInput = torch.split(inputData, BATCH_SIZE)
    splitOutput = torch.split(outputData, BATCH_SIZE)

    # we set up the lossFunction as the mean square error
    lossFunction = torch.nn.MSELoss()

    # we create the ANN
    ann = Net(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE).double()

    # we use an optimizer that implements stochastic gradient descent
    optimizerBatch = torch.optim.SGD(ann.parameters(), LEARNING_RATE)

    # we memorize the losses for some graphics
    lossList = []

    batchCount = DATA_SIZE // BATCH_SIZE

    for epoch in range(EPOCH_SIZE):
        for batch in range(batchCount):
            #compute output for batch
            prediction = ann(splitInput[batch].double())

            #compute loss for batch
            loss = lossFunction(prediction, splitOutput[batch])
            lossList.append(loss)

            #set up the gradients for the weights to zero
            optimizerBatch.zero_grad()

            #compute automatically the variation for each weight (and bias) of the network
            loss.backward()

            #compute the new values for the weights
            optimizerBatch.step()

        #print loss for the dataset for each 10th epoch
        if epoch % 100 == 99:
            y_pred = ann(inputData.double())
            loss = lossFunction(y_pred, outputData)
            print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    return ann


def saveToFile():
    ann = train()
    torch.save(ann.state_dict(),"myNetwork.pt")