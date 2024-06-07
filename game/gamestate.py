import numpy as np

MAX_HEIGHT = 5
MAX_WIDTH = 6
MIN = 0

class Gamestate:

    def __init__(self):
        self.width = 7
        self.height = 6
        self.board = None
        self.player = None
        self.clearBoard()
        

    def clearBoard(self):
        self.board = np.full([self.height,self.width],0,dtype=int)
        self.player = 1

    def put(self,column):
        for i in range(self.width):
            if self.board[i][column] == 0:
                self.board[i][column] = self.player                
                return True
        return False
    
    
    
    def checkWon(self):
        for i in range(3):
            for j in range(self.width):
                if self.board[i][j] == self.player:
                    if self.checkVerticalWon(i,j) or self.checkHorizontalWon(i,j) or self.checkDiagonalWon(i,j):
                        return True
        
        self.changePlayer()
        return False

    def checkVerticalWon(self,row,column):
        return self.checkUp(0,row,column) or self.checkDown(0,row,column)
    
    def checkHorizontalWon(self,row,column):
        return self.checkLeft(0,row,column) or self.checkRight(0,row,column)
    
    def checkDiagonalWon(self,row,column):
        return self.checkLeftUp(0,row,column) or self.checkLeftDown(0,row,column) or self.checkRightUp(0,row,column) or self.checkRightDown(0,row,column)
    
    def checkLeftUp(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True
        

        if column == MIN:
            return False
        if row == MAX_HEIGHT:
            return False
        return self.checkLeftUp(count,row+1,column-1)

    def checkLeftDown(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True
        
        if column == MIN:
            return False
        if row == MIN:
            return False
        return self.checkLeftDown(count,row-1,column-1)
    
    def checkRightUp(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True
        
        if column == MAX_WIDTH:
            return False
        if row == MAX_HEIGHT:
            return False
        return self.checkRightUp(count,row+1,column+1)
    
    def checkRightDown(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True
        
        if column == MAX_WIDTH:
            return False
        if row == MIN:
            return False
        return self.checkRightDown(count,row-1,column+1)
    
    def checkDown(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True        
        if row == MIN:
            return False        
        return self.checkDown(count,row-1,column)
    
    def checkUp(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True        
        if row == MAX_HEIGHT:
            return False        
        return self.checkUp(count,row+1,column)
    
    def checkLeft(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True
        
        if column == MIN:
            return False
        return self.checkLeft(count,row,column-1)
    
    def checkRight(self,count,row,column):
        if self.board[row][column] != self.player:
            return False
        count += 1
        if count == 4:
            return True
        
        if column == MAX_WIDTH:
            return False       
        return self.checkRight(count,row,column+1)

    def printBoard(self):
        print("_______________")
        for i in range(self.height-1,-1,-1):
            line = "|"
            for j in range(self.width):
                line = line + f"{self.board[i][j]}|"
            print(line)
        print("_______________")
    
    def changePlayer(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
    
    def getPlayer(self):
        return self.player