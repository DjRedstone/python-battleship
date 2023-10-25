from ship import SHIPS_TYPES, Ship
from utils import code_to_index
import string
from copy import copy

BOARD_HEIGHT = 10
BOARD_WIDTH = 10
MISS_CAR = "o"
HIT_CAR = "X"


def valide_coords(x: int, y: int) -> bool:
    """
    Check if coords are correct in the grid
    :param x: X coord
    :param y: Y coord
    :return: True / False
    """
    return 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH


def valide_code(code: str) -> bool:
    """
    Check if code are correct in the grid
    :param code: The code
    :return: True / False
    """
    x, y = code_to_index(code)
    return valide_coords(x, y)


def show_grid(grid: list[list[str]]):
    """
    Show a simple grid
    :param grid: A grid
    """
    tab = 25
    print(" " * tab + "     " + "   ".join(string.ascii_uppercase[:BOARD_WIDTH]))
    print(" " * tab + "   ╒" + "╤".join(["═══" for _ in range(BOARD_WIDTH)]) + "╕")
    n = 1
    for row in grid:
        print(" " * tab + (" " + str(n) if n < 10 else str(n)) + " │ " + " │ ".join(row) + " │")
        if n != BOARD_HEIGHT:
            print(" " * tab + "   ╞" + "═╪".join(["══" for _ in range(BOARD_WIDTH)]) + "═╡")
        else:
            print(" " * tab + "   ╘" + "═╧".join(["══" for _ in range(BOARD_WIDTH)]) + "═╛")
        n += 1


def show_grids(grid1: list[list[str]], name1: str, grid2: list[list[str]], name2: str):
    """
    Show two grid side by side
    :param grid1: The first grid
    :param name1: The first grid name
    :param grid2: The second grid
    :param name2: The second grid name
    """
    gap = 8
    print(" " * (BOARD_WIDTH * 2) + name1 + " " * ((BOARD_WIDTH * 2) + (gap * 3)) + name2)
    print(" " * ((BOARD_WIDTH * 2) - 1) + "‾" * (len(name1) + 2)
          + " " * ((BOARD_WIDTH * 2) + (gap * 3) - 2) + "‾" * (len(name2) + 2))
    print("     " + "   ".join(string.ascii_uppercase[:BOARD_WIDTH])
          + " " * (gap + 2)
          + "     " + "   ".join(string.ascii_uppercase[:BOARD_WIDTH]))
    print("   ╒" + "╤".join(["═══" for _ in range(BOARD_WIDTH)]) + "╕"
          + " " * gap
          + "   ╒" + "╤".join(["═══" for _ in range(BOARD_WIDTH)]) + "╕")
    n = 1
    for i in range(BOARD_WIDTH):
        row1 = grid1[i]
        row2 = grid2[i]
        print((" " + str(n) if n < 10 else str(n)) + " │ " + " │ ".join(row1) + " │"
              + " " * gap
              + (" " + str(n) if n < 10 else str(n)) + " │ " + " │ ".join(row2) + " │")
        if n != BOARD_HEIGHT:
            print("   ╞" + "═╪".join(["══" for _ in range(BOARD_WIDTH)]) + "═╡"
                  + " " * gap
                  + "   ╞" + "═╪".join(["══" for _ in range(BOARD_WIDTH)]) + "═╡")
        else:
            print("   ╘" + "═╧".join(["══" for _ in range(BOARD_WIDTH)]) + "═╛"
                  + " " * gap
                  + "   ╘" + "═╧".join(["══" for _ in range(BOARD_WIDTH)]) + "═╛")
        n += 1


class Board:
    """
    The classs for a board (including public [visible] and private [for ships])
    """

    def __init__(self, player_name: str):
        """
        Init
        :param player_name: The player's name
        """
        self.public_board = [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.private_board = [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.ships = []
        self.player_name = player_name

    def show_grid(self):
        """
        Print the public grid
        """
        show_grid(self.public_board)

    def get_public_by_coords(self, x: int, y: int) -> str:
        """
        Get value in public grid from coords
        :param x: X coord
        :param y: Y coord
        :return: The value
        """
        if valide_coords(x, y):
            return self.public_board[x][y]

    def get_public_by_code(self, code: str) -> str:
        """
        Get value in public grid from code
        :param code: The code
        :return: The value
        """
        if valide_code(code):
            x, y = code_to_index(code)
            return self.public_board[x][y]

    def set_public_by_coords(self, x: int, y: int, value: str):
        """
        Set value in public grid from coords
        :param x: X coord
        :param y: Y coord
        :param value: The new value
        """
        if valide_coords(x, y):
            self.public_board[x][y] = value

    def set_public_by_code(self, code: str, value: str):
        """
        Set value in public grid from code
        :param code: The code
        :param value: The new value
        """
        if valide_code(code):
            x, y = code_to_index(code)
            self.public_board[x][y] = value

    def show_ships(self):
        """
        Print the private grid
        """
        show_grid(self.private_board)

    def get_private_by_coords(self, x: int, y: int) -> str:
        """
        Get value in private grid from coords
        :param x: X coord
        :param y: Y coord
        :return: The value
        """
        if valide_coords(x, y):
            return self.private_board[x][y]

    def get_private_by_code(self, code: str) -> str:
        """
        Get value in private grid from code
        :param code: The code
        :return: The value
        """
        if valide_code(code):
            x, y = code_to_index(code)
            return self.private_board[x][y]

    def set_private_by_coords(self, x: int, y: int, value: str):
        """
        Set value in private grid by coords
        :param x: X coord
        :param y: Y coord
        :param value: The new value
        """
        if valide_coords(x, y):
            self.private_board[x][y] = value

    def set_private_by_code(self, code: str, value: str):
        """
        Set value in private grid from code
        :param code: The code
        :param value: The new value
        """
        if valide_code(code):
            x, y = code_to_index(code)
            self.private_board[x][y] = value

    def can_place_ship(self, ship_type: int, orient: bool, x: int, y: int) -> bool:
        """
        Check if we can place a ship at the selected coords
        :param ship_type: The ship type (check ship.py)
        :param orient: The orientation of the ship (True = vertical | False = horizontal)
        :param x: X coord
        :param y: Y coord
        :return: True / False
        """
        if not valide_coords(x, y):
            return False
        ship_size = SHIPS_TYPES[ship_type].size
        if orient:
            for i in range(ship_size):
                if not valide_coords(x + i, y):
                    return False
                elif self.get_private_by_coords(x + i, y) != " ":
                    return False
            return True
        else:
            for i in range(ship_size):
                if not valide_coords(x, y + i):
                    return False
                elif self.get_private_by_coords(x, y + i) != " ":
                    return False
            return True

    def place_ship(self, ship_type: int, orient: bool, x: int, y: int):
        """
        Place a ship at the selected place
        :param ship_type: The ship type (check ship.py)
        :param orient: The orientation of the ship (True = vertical | False = horizontal)
        :param x: X coord
        :param y: Y coord
        """
        if self.can_place_ship(ship_type, orient, x, y):
            ship = copy(SHIPS_TYPES[ship_type])
            if orient:
                ship.apply_coords([(x + i, y) for i in range(ship.size)])
                self.ships.append(ship)
                for i in range(ship.size):
                    self.set_private_by_coords(x + i, y, ship.symbol)
            else:
                ship.apply_coords([(x, y + i) for i in range(ship.size)])
                self.ships.append(ship)
                for i in range(ship.size):
                    self.set_private_by_coords(x, y + i, ship.symbol)

    def hit(self, code: str) -> str:
        """
        Hit a cell by code, if there is a ship, return True
        :param code: The cell code
        :return: True / False
        """
        if valide_code(code):
            cell = self.get_private_by_code(code)
            if cell == " ":
                self.set_public_by_code(code, MISS_CAR)
                return "miss"
            else:
                self.set_public_by_code(code, HIT_CAR)
                self.destroy_part(code)
                sinked = self.check_sinked_ships()
                return "hit" + (f"-{sinked}-sink" if sinked >= 1 else "")

    def destroy_part(self, code: str):
        """
        Destroy ship part from the code
        :param code: The code
        """
        for ship in self.ships:
            ship.destroy_part(code)

    def check_sinked_ships(self) -> int:
        """
        Return the number of sinked ship
        :return: The number
        """
        sinked = 0
        for ship in self.ships:
            if len(ship.coords) == 0:
                sinked += 1
                self.ships.remove(ship)
        return sinked

    def check_lose(self):
        """
        Check if there is no more ship on the grid
        :return: True / False
        """
        return len(self.ships) == 0

    def get_ships_clean(self) -> list[Ship]:
        """
        Return the list of ships but whitout the coords
        :return: The list of ships
        """
        res = []
        for ship in self.ships:
            ship_clean = ship.copy()
            ship_clean.coords = None
            res.append(ship_clean)
        return res
