import string


def sum_list(lst: list) -> int:
    """
    Calcul the somme of the list
    :param lst: A list of integer
    :return: The sum
    """
    res = 0
    for e in lst:
        res += e
    return res


def code_to_index(code: str) -> tuple[int, int]:
    """
    Transform a code to 2D list index
    :param code: The code
    :return: The index
    """
    letters = string.ascii_uppercase
    return int(code[1:]) - 1, letters.index(code[0])


def index_to_code(x: int, y: int) -> str:
    """
    Transform 2D list index to code
    :param x: x coord
    :param y: y coord
    :return: The code
    """
    letters = string.ascii_uppercase
    return letters[y] + str(x + 1)
