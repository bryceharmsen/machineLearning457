import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import linear,sigmoid
import matplotlib.pyplot as plt
import numpy as np
import random
import math

def pltData(train,test):
    fig = plt.figure()

def input_data(arr_size): #returns 2D array
    input_d = []
    for i in range(arr_size):
        x = random.random()*100+1
        y = random.random()*100+1
        input_d.append([x,y])
    return input_d

def target(data):
    targets = []
    for i in data:
        x = i[0]
        y = i[1]
        targets.append(math.sin(math.pi * 10 * x + 10 / (1 + y ** 2)) + math.log(x ** 2 + y ** 2))
    return targets

def ration_acc(total,correct):
    if total >= correct:
        return correct/total
    return total/correct
size = 1000
x_train = input_data(size)
y_train = target(x_train)

x_test = input_data(size)
y_test = target(x_test)

model = Sequential()
model.add(Dense(19,input_dim = 2, activation=sigmoid)) #first hidden layer with 19 neurons and 2 dimensions (x,y)
model.add(Dense(19,activation=sigmoid)) #hidden layer
model.add(Dense(1,activation=linear)) #output layer

model.compile(optimizer="adam",loss="mse") #adam is backpropogation

model.fit(x_train,y_train,epochs=500)

correct = 0
total = 0

#uses model with wieghts to predict
predictions = model.predict(x_test)
for i in range(size):
    print("Actual, Predictions", y_test[i],predictions.flatten()[i])
    correct += predictions.flatten()[i]
    total += y_test[i]

print("Total: ", total)
print("Correct: ", correct)

print("Total accuracy of this model is ", round(ration_acc(total,correct),2), "%")
