# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable.
import numpy as np
import pandas as pd
import random

class DB:
    def __init__(self) -> None:
        self.path = "tictactoe.csv"
        try:
            self.df = pd.read_csv(self.path, index_col=0)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=[
                                   "Round",
                                   "Player1",
                                   "Player2",
                                   "Winner",
                                   ])
    
    def save(self) -> None: 
        self.df.to_csv(self.path)
    
    def length(self):
        return len(self.df)
    
    def store(self, player1, player2, winner):
         self.df.loc[len(self.df)] = {
                "Round": len(self.df) + 1,
                "Player1": player1,
                "Player2": player2,
                "Winner": winner,
            }


class Oneplayergame():
    def __init__(self):
        self.winner = None
        self.currentplayer = random.choice(['X', 'O'])
        self.player1 = self.currentplayer
        if self.currentplayer == 'O':
            self.player2 = 'X'
        else:
            self.player2 = 'O'
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.db = DB()


    def get_winner(self):
        """Determines the winner of the given board.
        Returns 'X', '0', or None."""
        if self.checkDig(self.board) or self.checkRow(self.board) or self.checkHorizon(self.board) :
            self.winner = self.currentplayer
            print(f"The winner is {self.winner}")
        if self.checkNoSpotLeft():
            self.winner = "Tie"
        return self.winner


    def other_player(self):
        """switch the global variable currentplayer """
        if self.currentplayer == "X":
            self.currentplayer = "O"
        elif self.currentplayer == "O":
            self.currentplayer = "X"
        else:
            print("player not X or O!")


    #take player input
    def playerInput(self,board):
        print(self.currentplayer, "Enter a number 0-8: ")
        position = int(input())
        if position >= 0 and position <= 8:
            currentSpot = board[position // 3][position - (position // 3) * 3]
            if currentSpot != None:
                print("This spot is aleady taken")
            else: board[position // 3][position - (position // 3) * 3] = self.currentplayer
            #printBoard(board)
        else:
            print("only input 0-8")
    
    def random_input(self,board):
        self.board = board
        X = random.randint(low=1, high=10)
        O = random.randint(low=1, high=10)
        while self.board[X][O] != None:
            X = random.randint(low=1, high=10)
            O = random.randint(low=1, high=10)
        self.board[X][O] = self.currentplayer
        return self.board

    #check for win or tie

    def checkRow(self,board):
        for i in range(3):
            if board[0][i] == None:
                return False
            player = board[0][i]
            if board[1][i] == player and board[2][i] == player:
                self.winner = player
                return True
        return False
  
    def checkHorizon(self,board): 
        for i in range(3):
            if board[i][0] == None:
                return False
            player = board[i][0] 
            if board[i][1] == player and board[i][2] == player:
                self.winner = player
                return True
        return False 

    def checkDig(self,board):
        if board[1][1] == None:
            return False
        if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
            self.winner = board[0][0]
            return True
        if board[0][2] == board[1][1] == board[2][0]:
            self.winner = board[0][2]
            return True
        return False
    
    def checkNoSpotLeft(self):
        for row in self.board:
            if None in row:
                return False
        return True
    
    #Check for win or tie again
    def run(self):
        player1 = input("Enter player1 name: ")
        player2 = input("Enter player2 name: ")
        while self.winner == None:
            self.printBoard()
            self.playerInput(self.board)
            self.winner = self.get_winner()
            self.other_player()
        
        self.printBoard()
        if self.winner == self.player1:
            # save player O
            self.db.store(player1, player2, player1) 
        elif self.winner == self.player2:
             # save player X
            self.db.store(player1, player2, player2) 
        else: 
            self.db.store(player1, player2, "tie") 
        

        self.db.save()

    #Printing the game board 
    def printBoard(self):
        print(str(self.board[0]) + "\n" + str(self.board[1]) + "\n" + str(self.board[2]))

