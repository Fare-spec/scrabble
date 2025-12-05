import tiles as tl
import utils
import scoring as sc
import lexicon as lx
from board import Board, extract_coords


def asking(question: str) -> str:
    return input(question)


def tour_joueur(board):
    """
    Manage: Displaying the board at the right moment,
    asking which option to pick,
    return the result
    """

    board.affiche_jetons()
    answered = False
    answers = ("P", "E", "S")
    question = (
        f"What would you like to do ? [{'/'.join(answers)}] pass, exchange, suggest"
    )
    while not answered:
        answer = asking(question).strip().upper()
        answered = True if answer in answers else False
        if not answered:
            print("Please input P or E or S to select an action")

        if answer == answers[0]:
            pass
        elif answer == answers[1]:
            pass
        else:
            pass


def debug():
    board = Board()
    board.init_bonus()
    board.init_jetons()
    tour_joueur(board)


if __name__ == "__main__":
    debug()
