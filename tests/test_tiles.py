import tiles
import utils


def test_rack_add_and_remove():
    rack = tiles.Rack()
    rack.add_elt("A")
    rack.add_elts(["B", "C"])
    assert len(rack) == 3

    rack.remove_elt("B")
    assert list(rack) == ["A", "C"]

    rack.remove_elts(["A", "C"])
    assert len(rack) == 0


def test_pick_initial_size_and_counts():
    dico = utils.get_values()
    expected_total = sum(v["occ"] for v in dico.values())

    bag = tiles.Pick()
    assert len(bag) == expected_total

    # Vérifie que le multiensemble correspond au dictionnaire
    for letter, info in dico.items():
        assert list(bag).count(letter) == info["occ"]


def test_pick_draw_reduces_bag():
    bag = tiles.Pick()
    initial = len(bag)

    drawn = bag.draw(7)
    assert len(drawn) == 7
    assert len(bag) == initial - 7

    # Pas de crash sur la présence des tuiles tirées (invariant simple)
    for t in drawn:
        assert list(bag).count(t) >= 0


def test_exchange_success_and_failure():
    bag = tiles.Pick()
    rack = tiles.Rack()
    rack.add_elts(["A", "B", "C", "D", "E", "F", "G"])

    # Suffisamment de tuiles dans le sac et toutes présentes dans la main
    ok = tiles.exchange("AB", rack, bag)
    assert ok is True
    assert len(rack) == 7

    # Tenter de changer une tuile absente de la main
    nok = tiles.exchange("Z", rack, bag)
    assert nok is False


def test_echanger_wrapper():
    bag = tiles.Pick()
    rack = tiles.Rack()
    rack.add_elts(["A", "B", "C", "D", "E", "F", "G"])

    ok = tiles.echanger("AB", rack, bag)
    assert isinstance(ok, bool)


def test_pick_and_piocher():
    bag = tiles.Pick()
    initial = len(bag)

    drawn1 = tiles.pick(bag, 3)
    drawn2 = tiles.piocher(bag, 4)

    assert len(drawn1) == 3
    assert len(drawn2) == 4
    assert len(bag) == initial - 7


def test_init_pioche_alea_matches_pick_contents():
    bag = tiles.Pick()
    lst = tiles.init_pioche_alea()

    assert isinstance(lst, list)
    assert len(lst) == len(bag)
    assert sorted(lst) == sorted(list(bag))


def test_frequencies_percent_simple():
    freq = tiles.frequencies_percent(["A", "A", "B"])
    assert set(freq.keys()) == {"A", "B"}
    assert abs(freq["A"] - 2 / 3 * 100) < 1e-6
    assert abs(freq["B"] - 1 / 3 * 100) < 1e-6
