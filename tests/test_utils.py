import utils


def test_symetrise_liste_basic():
    lst = [1, 2, 3, 4]
    utils.symetrise_liste(lst)
    assert lst == [1, 2, 3, 4, 3, 2, 1]


def test_init_bonus_shape_and_symmetry():
    board = utils.init_bonus()
    assert len(board) == 15
    assert all(len(row) == 15 for row in board)

    for i in range(15):
        assert board[i] == board[14 - i]

    for j in range(15):
        col = [board[i][j] for i in range(15)]
        assert col == list(reversed(col))

    assert board[7][7] == "MD"


def test_generer_dictfr_non_empty_and_upper():
    words = utils.generer_dictfr()
    assert len(words) > 1000
    assert all(w == w.upper() for w in words[:100])


def test_generer_dico_and_get_values_equivalence():
    d1 = utils.generer_dico()
    d2 = utils.get_values()
    assert d1 == d2
    assert d1["A"]["val"] == 1 and d1["A"]["occ"] == 9
    assert d1["E"]["val"] == 1 and d1["E"]["occ"] == 15
    assert d1["?"]["val"] == 0 and d1["?"]["occ"] == 2
    assert len(d1) == 27
