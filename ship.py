from utils import code_to_index


class Ship:
    """
    Ship data
    """

    def __init__(self, name: str, size: int, symbol: str):
        """
        Init
        :param name: The name of the ship
        :param size: The size (in cell) of the ship
        :param symbol: The symbol (who will be show) of the ship
        """
        self.name = name
        self.size = size
        self.symbol = symbol
        self.coords = []

    def apply_coords(self, coords: list[tuple[int, int]]):
        """
        Apply coords to a ship
        :param coords: ships part as coords
        """
        self.coords = coords

    def destroy_part(self, code: str):
        """
        Destroy part of the ship from code
        :param code: The code
        """
        index = code_to_index(code)
        if index in self.coords:
            self.coords.remove(index)


SHIPS_TYPES = [
    Ship("Porte-avions", 5, "P"),
    Ship("Cuirassé", 4, "C"),
    Ship("Croiseur", 3, "c"),
    Ship("Torpileur", 2, "T"),
    Ship("Sous-marin", 2, "S"),
]

SHIPS_NB = [
    1,
    1,
    2,
    3,
    4
]
