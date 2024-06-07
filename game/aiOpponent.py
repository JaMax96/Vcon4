import numpy as np

class EasyAI():

    def getTurn(self,gamestate):
        return np.random.randint(7,size=1)


class MediumAI():
    
    def getTurn(gamestate):
        pass

class HardAI():
    
    def getTurn(gamestate):
        pass