from board import Board, MISS_CAR, HIT_CAR, show_grids
from ship import SHIPS_TYPES, SHIPS_NB
from utils import sum_list, index_to_code


class Game:
    """
    A game
    """

    def __init__(self, player1: object, player2: object):
        self.player1 = player1
        self.player2 = player2

    def start(self) -> dict:
        """
        Start a game
        :return: Game results
        """
        print("\n" * 3)
        player1_board = Board(self.player1.name)
        player2_board = Board(self.player2.name)
        # PLAYER 1 PLACE SHIPS
        ships_to_place = SHIPS_NB.copy()
        while sum_list(ships_to_place) != 0:
            if not self.player1.is_a_bot:
                player1_board.show_ships()
            ship_type, orient, x, y = self.player1.ask_ship(ships_to_place)
            if not player1_board.can_place_ship(ship_type, orient, x, y):
                if not self.player1.is_a_bot:
                    print("                                       Placement impossible")
            else:
                player1_board.place_ship(ship_type, orient, x, y)
                ships_to_place[ship_type] -= 1
                ship = SHIPS_TYPES[ship_type]
                if not self.player1.is_a_bot:
                    print("       Le bateau \"{0}\" de taille {1} a été positionné aux coordonnées {2} à {3}".format(
                        ship.name,
                        ship.size,
                        index_to_code(x, y),
                        "la vertical" if orient else "l'horizontal"
                    ))
        # PLAYE 2 PLACE SHIPS
        print("\n" * 5)
        ships_to_place = SHIPS_NB.copy()
        while sum_list(ships_to_place) != 0:
            if not self.player2.is_a_bot:
                player2_board.show_ships()
            ship_type, orient, x, y = self.player2.ask_ship(ships_to_place)
            if not player2_board.can_place_ship(ship_type, orient, x, y):
                if not self.player2.is_a_bot:
                    print("                                       Placement impossible")
            else:
                player2_board.place_ship(ship_type, orient, x, y)
                ships_to_place[ship_type] -= 1
                ship = SHIPS_TYPES[ship_type]
                if not self.player2.is_a_bot:
                    print("       Le bateau \"{0}\" de taille {1} a été positionné aux coordonnées {2} à {3}".format(
                        ship.name,
                        ship.size,
                        index_to_code(x, y),
                        "la vertical" if orient else "l'horizontal"
                    ))
        # START GAME
        print("\n" * 5)
        player1_turn = True
        game_result = {
            "nb_rounds": 0,
            "player1_rounds": 0,
            "player2_rounds": 0
        }
        while not player1_board.check_lose() and not player2_board.check_lose():
            game_result["nb_rounds"] += 1
            if self.player1.update_data:
                self.player1.update_data(player2_board.public_board, player2_board.ships)
            if self.player2.update_data:
                self.player2.update_data(player1_board.public_board, player1_board.ships)
            if player1_turn:
                print(f"                                    C'est au tour de {self.player1.name} !\n")
                game_result["player1_rounds"] += 1
                show_grids(player2_board.public_board, self.player1.name, player1_board.public_board, self.player2.name)
                while True:
                    code = self.player1.ask_code()
                    if player2_board.get_public_by_code(code) not in [MISS_CAR, HIT_CAR]:
                        break
                    else:
                        if not self.player1.is_a_bot:
                            print("                                    Vous avez déjà tenté cette case")
                print("                                              > " + code + " <")
                res = player2_board.hit(code)
                if res.startswith("hit"):
                    if res.endswith("sink"):
                        sinked = res.split("-")[1]
                        print(f"{(' ' * 43) if sinked != 1 else (' ' * 28)}"
                              f"Touché coulé ! {'' if sinked != 1 else f'({sinked} bateaux en un seul coup !)'}")
                    else:
                        print("                                             Touché !")
                else:
                    print("                                              Loupé !")
                    player1_turn = False
                if self.player1.update_last_res:
                    self.player1.update_last_res(code, res)
            else:
                print(f"                                    C'est au tour de {self.player2.name} !\n")
                game_result["player2_rounds"] += 1
                show_grids(player1_board.public_board, self.player2.name, player2_board.public_board, self.player1.name)
                while True:
                    code = self.player2.ask_code()
                    print(code)
                    if player1_board.get_public_by_code(code) not in [MISS_CAR, HIT_CAR]:
                        break
                    else:
                        if not self.player2.is_a_bot:
                            print("                                    Vous avez déjà tenté cette case")
                print("                                              > " + code + " <")
                res = player1_board.hit(code)
                if res.startswith("hit"):
                    if res.endswith("sink"):
                        sinked = res.split("-")[1]
                        print(f"{(' ' * 43) if sinked != 1 else (' ' * 28)}"
                              f"Touché coulé ! {'' if sinked != 1 else f'({sinked} bateaux en un seul coup !)'}")
                    else:
                        print("                                             Touché !")
                else:
                    print("                                              Loupé !")
                    player1_turn = True
                if self.player2.update_last_res:
                    self.player2.update_last_res(code, res)
            print()
        winner = ""
        if player1_board.check_lose():
            print(f"                                         {self.player2.name} a gagné !\n")
            winner = self.player2.name
        else:
            print(f"                                         {self.player1.name} a gagné !\n")
        game_result["winner"] = winner
        return game_result


print("""
                                        ╒════════════════╕
                                        │   BATTLESHIP   │
                                        ╘════════════════╛

                                            Bienvenue !
""")
input("                                 Appuyez sur entrer pour continuer\n"
      "                                                 ")
