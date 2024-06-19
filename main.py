from game.gamestate import Gamestate
from controllers.cli_controller import CLIController
from controllers.gui_controller import GuiController
from utils import MenuItem
from game.aiOpponent import EasyAI

controller = GuiController()
game = Gamestate() 

def runOnePlayerMode():  

    print("Please Choose a difficulty")    
    opponent = EasyAI()

    print("Game Starting") 
    while True:
        print(f"Player {game.getPlayer()}, please do your turn")
        
        move = controller.getMove(game)
        game.put(move)
        game.printBoard()

        if game.checkWon():
            print(f"Player {game.getPlayer()} has won: Wohoohoohoho")
            controller.getWinningWindow(1)           
            game.clearBoard()
            break

        print("Opponents turn")
        move = opponent.getTurn(game.board)
        game.put(move)
        game.printBoard()

        if game.checkWon():
            print(f"AI has won: Oh No")
            controller.getWinningWindow(2)          
            game.clearBoard()
            break

def runTwoPlayerMode():
    run = True

    
    print("Game Starting")
    while run:
        print(f"Player {game.getPlayer()}, please do your turn")
        
        move = controller.getMove(game)
        game.put(move)

        game.printBoard()


        if game.checkWon():
            print(f"Player {game.getPlayer()} has won: Wohoohoohoho")
            controller.getWinningWindow(game.getPlayer())    
            run = False
            game.clearBoard()
        
        

def runGame():
    run = True

    menuItem = None
    while run:
        print("Menu Item Selection")
        menuItem = controller.getMenuItem()

        print(menuItem)

        match menuItem:      
                
            case MenuItem.OnePlayer.name:
                runOnePlayerMode()


            case MenuItem.TwoPlayer.name:
                runTwoPlayerMode()

            case MenuItem.Highscore.name:
                print("Not implemented yet")
                run = False

            case MenuItem.Exit.name:
                run = False

    print("Thanks for playing Vcon4")

runGame()

            