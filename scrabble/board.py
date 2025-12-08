from typing import Any
import copy as cp
import utils


def extract_coords(board: list[list[Any]], elt: Any) -> set[tuple[int, int]]:
    """
    This function is use to get every coordinate of elt inside board return them inside a set (for performace)
    """
    elements = set()
    for i, rows in enumerate(board):
        for j, cell in enumerate(rows):
            if cell == elt:
                elements.add((i, j))

    return elements


class Board:
    def __init__(self, size: int = 15) -> None:
        """
        Allow to create the object Board with default size 15. It's not advised to change size because it will most likely break the code.
        """
        self.size = size

    def init_jetons(self) -> None:
        self.board = [["" for _ in range(self.size)] for _ in range(self.size)]

    def init_bonus(self) -> None:
        """
        Allow to initialize all the bonuses on the board
        """
        self.board = utils.init_bonus()

    def prepare_sdout(self) -> list[list[str]]:
        # In this function we will be using two lists the first one will be the object and the second will be a new bonus list the goal
        # here is to know which cell is a bonus and if we're using the first list we might at some point overwrite one of the bonus by a letter
        # the solutions are this one or using tuples inside the first list
        original_list = utils.init_bonus()
        copy = cp.deepcopy(self.board)
        bonuses = ("MT", "LD", "MD", "LT")
        mt_set = extract_coords(original_list, bonuses[0])
        ld_set = extract_coords(original_list, bonuses[1])
        md_set = extract_coords(original_list, bonuses[2])
        lt_set = extract_coords(original_list, bonuses[3])
        for coords in mt_set:
            element = copy[coords[0]][coords[1]] + "³"
            copy[coords[0]][coords[1]] = element

        for coords in ld_set:
            element = copy[coords[0]][coords[1]] + "2"
            copy[coords[0]][coords[1]] = element

        for coords in md_set:
            element = copy[coords[0]][coords[1]] + "²"
            copy[coords[0]][coords[1]] = element

        for coords in lt_set:
            element = copy[coords[0]][coords[1]] + "3"
            copy[coords[0]][coords[1]] = element
        return copy

    def affiche_jetons(self) -> None:
        # Column headers.
        board = self.prepare_sdout()
        print("    " + "  ".join(f"{i:02d}" for i in range(1, self.size + 1)))
        print("   " + "|---" * self.size + "|")
        sep = "   " + "|---" * self.size + "|"
        # Content of the board.
        for i in range(self.size):
            cells = []
            for j in range(self.size):
                v = board[i][j]
                v = "" if v is None else str(v)
                cells.append(v[:3].center(3))
            ligne = f"{i + 1:02d} |" + "|".join(cells) + "|"
            print(ligne)
            print(sep)


if __name__ == "__main__":
    board = Board()
    board.init_bonus()
    print("######################### CREATED BOARD #########################")
    board.affiche_jetons()
