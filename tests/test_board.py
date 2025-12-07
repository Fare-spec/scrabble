import board
import utils


def test_extract_coords_basic():
    b = [
        [1, 2],
        [3, 1],
    ]
    coords = board.extract_coords(b, 1)
    assert coords == {(0, 0), (1, 1)}
    assert board.extract_coords(b, 4) == set()


def test_board_init_jetons_and_bonus():
    bd = board.Board(size=5)
    bd.init_jetons()

    assert len(bd.board) == 5
    assert all(len(row) == 5 for row in bd.board)
    assert all(cell == "" for row in bd.board for cell in row)

    # init_bonus doit réutiliser utils.init_bonus()
    bd2 = board.Board()
    bd2.init_bonus()
    bonus = utils.init_bonus()
    assert bd2.board == bonus


def test_prepare_sdout_dimensions():
    bd = board.Board()
    bd.init_bonus()
    stdout_board = bd.prepare_sdout()

    assert len(stdout_board) == bd.size
    assert all(len(row) == bd.size for row in stdout_board)
