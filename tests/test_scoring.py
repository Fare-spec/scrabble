import scoring
import utils


def test_word_value_simple_and_bonus_length():
    dico = utils.get_values()

    assert scoring.word_value("A", dico) == 1
    assert scoring.word_value("JEU", dico) == 10  # J=8,E=1,U=1

    # Mot de longueur >= 8 : bonus 50
    base = sum(dico[ch]["val"] for ch in "ABCDEFGH")
    assert scoring.word_value("ABCDEFGH", dico) == base + 50


def test_word_value_on_board_bonus_and_bounds():
    dico = utils.get_values()

    # Centre (7,7) : MD -> double mot
    v_center = scoring.word_value_on_board("JEU", dico, 7, 7, "H")
    assert v_center == 20

    # Coin (0,0) : MT -> triple mot
    v_corner = scoring.word_value_on_board("JEU", dico, 0, 0, "H")
    assert v_corner == 30

    # Case "neutre" : (7,8)
    v_plain = scoring.word_value_on_board("JEU", dico, 7, 8, "H")
    assert v_plain == 10

    # Sortie du plateau -> 0
    assert scoring.word_value_on_board("JEU", dico, 14, 13, "H") == 0


def test_best_word_single_and_multiple():
    dico = utils.get_values()

    # Lexique restreint artificiel
    mots = ["A", "KI", "JEU"]
    letters = list("JEU")
    best = scoring.best_word(mots, letters, dico)
    assert best == "JEU"

    # Deux mots avec même score
    mots2 = ["AB", "AC"]
    letters2 = list("ABC")
    best_list = scoring.best_word(mots2, letters2, dico, multiple=True)
    assert sorted(best_list) == ["AB", "AC"]


def test_meilleur_mot_and_meilleurs_mots_wrappers():
    dico = utils.get_values()
    mots = ["AB", "AC"]
    letters = list("ABC")

    m = scoring.meilleur_mot(mots, letters, dico)
    assert isinstance(m, str)

    ml = scoring.meilleurs_mots(mots, letters, dico)
    assert isinstance(ml, list)
    assert all(isinstance(x, str) for x in ml)
