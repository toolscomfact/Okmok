import tensorflow as tf
import numpy as np
import math
import time
import os
import random
from Omok import Omok, Replay, Inverse

boardLength = 10

class Textbook:
    def __init__(self):
        self.Xdata = np.zeros((0, boardLength * boardLength))
        self.Ydata = np.zeros((0, boardLength * boardLength))

    def addData(self, x, y):
        self.Xdata = np.vstack([self.Xdata, x])
        self.Ydata = np.vstack([self.Ydata, y])

    def getBatch(self, size):
        index = random.randint(0, len(self.Xdata)-size)
        return self.Xdata[index:index+size], self.Ydata[index:index+size]

    def getSize(self):
        return len(self.Xdata)

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(
        input_shape=(100)
    ),
    tf.keras.layers.Dense(
        121, 
        activation=tf.keras.activations.relu
    ),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(
        144, 
        activation=tf.keras.activations.relu
    ),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(
        121, 
        activation=tf.keras.activations.relu
    ),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(
        100, 
        activation=tf.keras.activations.softmax
    )
])

modelOptimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

model.compile(
    optimizer=modelOptimizer,
    loss=tf.keras.losses.MeanSquaredError(),
    metrics=["accuracy"]
)

print(model.summary())

print("Learn by Tensorflow")
stone = 1
turn = 0

repeat = 0

while True:
    currentGame = Omok(boardLength)
    currentReplay = Replay(boardLength)

    print("--------------------")
    print(currentGame.getBoard())
    print()
    print()

    while True:
        if (stone == 1):
            currentBoard = currentGame.getBoard()
        else:
            currentBoard = currentGame.getInverseBoard()

        currentBoard = currentBoard.reshape((1, boardLength*boardLength))
        prohibitBoard = currentGame.getProhibit()

        predictRaw = model.predict(x=currentBoard)
        predictRaw = tf.subtract(predictRaw, prohibitBoard)
        predictRaw = tf.argmax(predictRaw, 1)

        xx = predictRaw % boardLength
        yy = math.floor(predictRaw / boardLength)

        setres, reward = currentGame.setStone(xx, yy, stone)
        currentReplay.addBoard(currentGame.getBoard(), reward)

        os.system("cls")
        print("------\t",turn,"번 턴\t---------")
        print(stone == 1 and "흑" or "백", "(",xx,",",yy,"착수)")
        turn += 1
        currentGame.showBoard()
        print()
        print()

        stone = stone == 1 and 2 or 1

        result, winner = currentGame.checkIsEnd()

        if (result):
            print("Game End, Win -", winner == 1 and "흑" or "백")

            textBook = Textbook()

            boards = currentReplay.getBatch()
            rewards = currentReplay.getRewardBatch()

            for i, reward in enumerate(rewards):
                #Turn - i, Reward - reward

                for _ in range(int(pow(reward, 2)*2)):
                    if (i%2 == 0): # 흑일때 착수
                        textBook.addData(boards[i-1], boards[i])
                    else: # 백일때 착수
                        textBook.addData(
                            Inverse(boards[i-1]), 
                            Inverse(boards[i]))

            print("학습 데이터 준비완료. 학습데이터 크기 -", textBook.getSize())
        
            XData, YData = textBook.getBatch(textBook.getSize())
            print(XData.shape, YData.shape)
            model.fit(XData, YData, batch_size=int(textBook.getSize()/2), epochs=512)

            repeat += 1
            break
        if (repeat == 200):
            time.sleep(1)

    if (repeat == 200):
        break