# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F
from createdb import *
from trainmodel import *
from myModel import *

#generate input
#saveToDb()

#train data and save to file
#saveToFile()

#load model
ann = Net(INPUT_SIZE,HIDDEN_SIZE,OUTPUT_SIZE)
ann.load_state_dict(torch.load("myNetwork.pt"))
ann.eval()

#user input
while True:
    print("Write exit to stop.")
    x=input("x=")
    if x == "exit":
        break
    else:
        x=float(x)
    y=float(input("y="))
    inputTensor = torch.tensor([x, y])
    print(ann(inputTensor).item())

for name, param in ann.named_parameters():
    if param.requires_grad:
        print(name, param.data)
