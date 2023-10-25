# Importing os lib and game components
import os
from game import Game
from players import Player, Bot

# Creating player 1 and 2
player1 = Player(os.getlogin())
player2 = Bot("mon robot", 1)
# Creating a game
game = Game(player1, player2)
# Starting a game
# Game results are saved in the return of the <start> function
game.start()
