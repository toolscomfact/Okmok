from Omok import Omok, Replay

import os

def clearScreen():
    os.system("cls")

clearScreen()
boardLength = 7

game = Omok(boardLength)
game.showBoard()

history = Replay(boardLength)

stone = 1

while True:
    while True:
        cmd = input()
        
        splits = cmd.split(",")
        x = int(splits[0])
        y = int(splits[1])

        setResult = game.setStone(x, y, stone)
        
        if (setResult):
            stone = stone == 1 and 2 or 1
            break

    history.addBoard(game.getBoard())
            
    clearScreen()
    game.showBoard()

    gameResult, winner = game.checkIsEnd()
    print(gameResult, winner)

    if (gameResult):
        print("Game Done. Winner :", winner == 1 and "Black" or (winner == 2 and "White" or "무승부"))
        
        print(history.getBatch())
        break