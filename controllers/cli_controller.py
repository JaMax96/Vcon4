from controllers.abstractController import AbstractController
from utils import MenuItem
import re

class CLIController(AbstractController):

    def getMenuItem(self):        
        while True:
            print("Please enter a menu item")
            x = input()
            if x in [e.name for e in MenuItem]:
                return x
            print(f"{x} is not a valid menu item, please enter one of these")
            print(list(MenuItem))        
    
    def getMove(self):
        while True:
            x = input()
            if re.search("[1-7]",x):
                return int(x)-1
            print(f"{x} is not a valid move please enter a column from 1-7 (left to right)")
