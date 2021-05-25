import torch
import numpy as np
from const import *

def createDB():
    #generate distribution
    inputData = (DOMAIN_MAX - DOMAIN_MIN) * torch.rand(DATA_SIZE, INPUT_SIZE) + DOMAIN_MIN

    #calculate f(x1,x2) = sin(x1 + x2/pi) for each point
    outputData = []
    for data in inputData.numpy():
        outputData.append(np.sin(data[0] + data[1]/np.pi))
    outputDataAsTensor = torch.tensor(outputData)

    #return pairs
    return torch.column_stack((inputData,outputDataAsTensor))

def saveToDb():
    torch.save(createDB(),"mydataset.dat")