from game.gamestate import Gamestate
from controllers.cli_controller import CLIController
from utils import MenuItem
from game.aiOpponent import EasyAI

controller = CLIController()
game = Gamestate() 

def runOnePlayerMode():  

    print("Please Choose a difficulty")    
    opponent = EasyAI()

    print("Game Starting") 
    while True:
        print(f"Player {game.getPlayer()}, please do your turn")
        
        move = controller.getMove()
        game.put(move)
        game.printBoard()

        if game.checkWon():
            print(f"Player {game.getPlayer()} has won: Wohoohoohoho")            
            game.clearBoard()
            break

        print("Opponents turn")
        move = opponent.getTurn(game.board)
        game.put(move)
        game.printBoard()

        if game.checkWon():
            print(f"AI has won: Oh No")            
            game.clearBoard()
            break

def runTwoPlayerMode():
    run = True

    
    print("Game Starting")
    while run:
        print(f"Player {game.getPlayer()}, please do your turn")
        
        move = controller.getMove()
        game.put(move)

        game.printBoard()


        if game.checkWon():
            print(f"Player {game.getPlayer()} has won: Wohoohoohoho")
            run = False
            game.clearBoard()
        
        

def runGame():
    run = True

    menuItem = None
    while run:
        menuItem = controller.getMenuItem()

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

            