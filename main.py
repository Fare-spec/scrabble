import scrabble as scr
import engine


def questions():
    print(scr.init_bonus())


def gen_display_board():
    scrabble = engine.Board(5)
    scrabble.init_jetons()
    scrabble.affiche_jetons()


if __name__ == "__main__":
    gen_display_board()


def main():
    print("Hello from scrable!")


if __name__ == "__main__":
    main()
