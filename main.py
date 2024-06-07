from game.gamestate import Gamestate
from controllers.cli_controller import CLIController
from utils import MenuItem

controller = CLIController()
game = Gamestate() 

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
                print("Not implemented yet")
                run = False

            case MenuItem.TwoPlayer.name:
                runTwoPlayerMode()

            case MenuItem.Highscore.name:
                print("Not implemented yet")
                run = False

            case MenuItem.Exit.name:
                run = False

    print("Thanks for playing Vcon4")

runGame()

            