from ship import SHIPS_TYPES
from utils import sum_list, code_to_index
from board import valide_code
import string


def show_ship_types(user_ships: list[int]):
    """
    Print all ship type with data
    :param user_ships: User ships
    """
    print("                                           Vos bateaux :")
    for ship_type in range(len(SHIPS_TYPES)):
        ship = SHIPS_TYPES[ship_type]
        if user_ships[ship_type] != 0:
            print("                         - [{0}] {1} ({2}) - {3} case{4} - {5} diponible{6}".format(
                ship_type,
                ship.name,
                ship.symbol,
                ship.size,
                "" if ship.size <= 1 else "s",
                user_ships[ship_type],
                "" if user_ships[ship_type] <= 1 else "s"
            ))


def ask_ship_type(user_ships: list[int]) -> int:
    """
    Ask user for a ship type
    :param user_ships: User ships
    :return: The ship type
    """
    show_ship_types(user_ships)
    ship_type = input("                           Entrez un type de bateau (son identifiant) :\n"
                      "                                                ")
    if ship_type not in [str(i) for i in range(len(SHIPS_TYPES))]:
        print("                                           Type inconnu")
        return ask_ship_type(user_ships)
    ship_type = int(ship_type)
    if user_ships[ship_type] == 0:
        print("                                   Ce bateau n'est pas dispobile")
        return ask_ship_type(user_ships)
    return ship_type


def ask_orient() -> bool:
    """
    Ask user for the orientation of the ship
    :return: True = Vertical / False = Horizontal
    """
    orient = input("                             Entrez l'orientation du bateau (H/V) :\n"
                   "                                                ").upper()
    if orient == "H":
        return False
    if orient == "V":
        return True
    return ask_orient()


def ask_code() -> str:
    """
    Ask user for the coords of the ship
    :return: Coords x and y
    """
    code = input("                             Entrez un position sous forme de code :\n"
                 "                                                ").upper()
    if len(code) < 2 or len(code) > 3:
        print("                                       Coordonnées inconnues")
        return ask_code()
    if code[0] not in string.ascii_uppercase or not code[1:].isnumeric():
        print("                                      Coordonnées incorrectes")
        return ask_code()
    if not valide_code(code):
        print("                                       Coordonnées invalides")
        return ask_code()
    return code


def ask_ship(user_ships: list[int]) -> tuple[int, bool, int, int]:
    """
    Ask user for a ship data
    :param user_ships: User ships
    :return: A tuple with the ship type, the orientation and the coords x and y
    """
    # ship TYPE
    if sum_list(user_ships) == 1:
        ship_type = user_ships.index(1)
    else:
        ship_type = ask_ship_type(user_ships)
    # ship COORDS
    x, y = code_to_index(ask_code())
    # ship ORIENTATION
    if SHIPS_TYPES[ship_type].size != 1:
        orient = ask_orient()
    else:
        orient = False
    # RETURN
    return ship_type, orient, x, y
