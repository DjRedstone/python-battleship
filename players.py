import random
from board import BOARD_WIDTH, BOARD_HEIGHT, valide_coords
from user_interaction import ask_ship, ask_code
from utils import index_to_code, code_to_index
from ship import Ship


def generate_ship_placement(computer_ships: list[int]) -> tuple[int, bool, int, int]:
    """
    Generate a random ship placement
    :param computer_ships: The ships to place
    :return: The placement data (type | orientation | x | y)
    """
    possible_ships = [ship_type for ship_type in range(len(computer_ships)) if computer_ships[ship_type] != 0]
    return (random.choice(possible_ships),
            bool(random.getrandbits(1)),
            random.randint(0, BOARD_HEIGHT - 1),
            random.randint(0, BOARD_WIDTH - 1)
            )


class Player:
    """
    A player
    """
    def __init__(self, name: str):
        """
        Init
        :param name: The player name
        """
        self.name = name
        self.is_a_bot = False

    @staticmethod
    def ask_ship(ships: list[int]) -> tuple[int, bool, int, int]:
        """
        Ask player for ship placement
        :param ships: Avaible ships by id
        :return: ship placement data (id, orientation, coords x and y)
        """
        return ask_ship(ships)

    @staticmethod
    def ask_code() -> str:
        """
        Ask player for code
        :return: A code
        """
        return ask_code()


class Bot:
    """
    A bot
    """

    def generate_code_dif0(self) -> str:
        while True:
            coords = (random.randint(0, BOARD_HEIGHT - 1), random.randint(0, BOARD_WIDTH - 1))
            if coords not in self.hits:
                self.hits.add(coords)
                return index_to_code(coords[0], coords[1])

    def generate_code_dif1(self) -> str:
        if "ship_size" not in self.chasing_ship.keys():
            current_ship_size = 2
            for ship in self.ships:
                if ship.size > current_ship_size:
                    current_ship_size = ship.size
            self.chasing_ship["ship_size"] = current_ship_size
        else:
            current_ship_size = self.chasing_ship["ship_size"]
            if current_ship_size < 2:
                current_ship_size = 2
        if not self.chasing_ship["is"]:
            current_i = 0
            i, j = 0, 0
            other_side = False
            while True:
                if (i, j) not in self.hits and valide_coords(i, j):
                    break
                if not other_side:
                    if i > 0:
                        i -= 1
                        j += 1
                    else:
                        current_i += (current_ship_size - 1)
                        if current_i >= BOARD_HEIGHT:
                            other_side = True
                            i = current_i - BOARD_HEIGHT + 1
                            j = BOARD_WIDTH - 1
                        else:
                            i = current_i
                            j = 0
                else:
                    if (i, j) not in self.hits and valide_coords(i, j):
                        break
                    if i < (BOARD_HEIGHT - 1):
                        i += 1
                        j -= 1
                    else:
                        current_i += (current_ship_size - 1)
                        i = current_i - BOARD_HEIGHT + 1
                        j = BOARD_WIDTH - 1
                    if current_i >= BOARD_HEIGHT * 2:
                        self.chasing_ship["ship_size"] -= 1
                        return self.generate_code_dif1()
            self.hits.add((i, j))
            return index_to_code(i, j)
        else:
            x, y = self.chasing_ship["coords"]
            if not self.chasing_ship["dir"]:
                if "last_dir" not in self.chasing_ship.keys():
                    self.chasing_ship["last_dir"] = "up"
                    if valide_coords(x - 1, y) and (x - 1, y) not in self.hits:
                        self.hits.add((x - 1, y))
                        return index_to_code(x - 1, y)
                    else:
                        return self.generate_code_dif1()
                else:
                    if self.chasing_ship["last_dir"] == "up" and valide_coords(x, y + 1) and (x, y + 1) not in self.hits:
                        self.chasing_ship["last_dir"] = "right"
                        self.hits.add((x, y + 1))
                        return index_to_code(x, y + 1)
                    elif self.chasing_ship["last_dir"] == "right" and valide_coords(x + 1, y) and (x + 1, y) not in self.hits:
                        self.chasing_ship["last_dir"] = "down"
                        self.hits.add((x + 1, y))
                        return index_to_code(x + 1, y)
                    elif self.chasing_ship["last_dir"] == "down" and valide_coords(x, y - 1) and (x, y - 1) not in self.hits:
                        self.chasing_ship["last_dir"] = "left"
                        self.hits.add((x, y - 1))
                        return index_to_code(x, y - 1)
                    else:
                        self.chasing_ship["is"] = False
                        self.chasing_ship["coords"] = None
                        self.chasing_ship["dir"] = None
                        self.chasing_ship["coords"] = None
                        self.chasing_ship["other_side"] = False
                        self.chasing_ship["ship_size"] -= 1
                        return self.generate_code_dif1()
            else:
                i = 0
                while True:
                    print(self.chasing_ship)
                    if self.chasing_ship["dir"] in ["up", "down"]:
                        if self.chasing_ship["other_side"]:
                            if (x + i, y) not in self.hits:
                                if not valide_coords(x + i, y):
                                    self.chasing_ship["is"] = False
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["dir"] = None
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["other_side"] = False
                                    return self.generate_code_dif1()
                                self.hits.add((x + i, y))
                                return index_to_code(x + i, y)
                            i += 1
                        else:
                            if (x - i, y) not in self.hits:
                                if not valide_coords(x - i, y):
                                    self.chasing_ship["is"] = False
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["dir"] = None
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["other_side"] = False
                                    return self.generate_code_dif1()
                                self.hits.add((x - i, y))
                                return index_to_code(x - i, y)
                            i -= 1
                    if self.chasing_ship["dir"] in ["left", "right"]:
                        if self.chasing_ship["other_side"]:
                            if (x, y + i) not in self.hits:
                                if not valide_coords(x, y + i):
                                    self.chasing_ship["is"] = False
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["dir"] = None
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["other_side"] = False
                                    return self.generate_code_dif1()
                                self.hits.add((x, y + i))
                                return index_to_code(x, y + i)
                            i += 1
                        else:
                            if (x, y + i) not in self.hits:
                                if not valide_coords(x, y + i):
                                    self.chasing_ship["is"] = False
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["dir"] = None
                                    self.chasing_ship["coords"] = None
                                    self.chasing_ship["other_side"] = False
                                    return self.generate_code_dif1()
                                self.hits.add((x, y + i))
                                return index_to_code(x, y + i)
                            i -= 1

    def __init__(self, name: str, dificulty: int):
        """
        Init
        :param name: The bot name
        :param dificulty: The dificulty of the bot
        """
        self.is_a_bot = True
        self.name = name
        self.generate_code_functions = {
            0: self.generate_code_dif0,
            1: self.generate_code_dif1
        }
        assert dificulty in self.generate_code_functions.keys(), "Dificulty doesn't exist"
        self.dificulty = dificulty
        self.hits = set()
        self.ships = []
        self.grid = []
        self.chasing_ship = {"is": False, "dir": None, "other_side": False}

    @staticmethod
    def ask_ship(ships: list[int]) -> tuple[int, bool, int, int]:
        """
        Generate ship placement
        :param ships: Avaible ships by id
        :return: ship placement data (id, orientation, coords x and y)
        """
        return generate_ship_placement(ships)

    def ask_code(self) -> str:
        """
        Generate a code
        :return: A code
        """
        return self.generate_code_functions[self.dificulty]()
    
    def update_data(self, grid: list[list[str]], ships: list[Ship]):
        """
        Update data
        :param grid: A grid
        :param ships: Ships
        """
        self.grid = grid
        self.ships = ships

    def update_last_res(self, code: str, res: str):
        """
        Update last result from hit
        :param code: The code of the hit
        :param res: The result
        """
        if res.startswith("hit"):
            if res.endswith("sink"):
                self.chasing_ship["is"] = False
                self.chasing_ship["coords"] = None
                self.chasing_ship["dir"] = None
                self.chasing_ship["coords"] = None
                self.chasing_ship["other_side"] = False
                if "ship_size" in self.chasing_ship.keys():
                    del self.chasing_ship["ship_size"]
            else:
                if not self.chasing_ship["is"]:
                    self.chasing_ship["is"] = True
                    self.chasing_ship["coords"] = code_to_index(code)
                    self.chasing_ship["dir"] = None
                else:
                    if not self.chasing_ship["dir"]:
                        coords = code_to_index(code)
                        if self.chasing_ship["coords"][0] - 1 == coords:
                            self.chasing_ship["dir"] = "up"
                        elif self.chasing_ship["coords"][1] + 1 == coords:
                            self.chasing_ship["dir"] = "right"
                        elif self.chasing_ship["coords"][0] + 1 == coords:
                            self.chasing_ship["dir"] = "down"
                        else:
                            self.chasing_ship["dir"] = "left"
        else:
            if self.chasing_ship["dir"]:
                self.chasing_ship["other_side"] = True
