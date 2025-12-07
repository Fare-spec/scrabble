import tiles
import player


def test_player_init_and_refill_rack():
    bag = tiles.Pick()
    total_before = len(bag)

    p = player.Player("Alice", bag)
    assert p.name == "Alice"
    assert p.score == 0
    assert 0 < len(p.rack) <= 7
    # Conservation du nombre total de tuiles
    assert len(p.rack) + len(bag) == total_before


def test_player_refill_rack_tops_up_to_seven():
    bag = tiles.Pick()
    p = player.Player("Bob", bag)

    initial_rack_size = len(p.rack)
    initial_bag_size = len(bag)

    removed = min(3, initial_rack_size)
    for _ in range(removed):
        p.rack.remove_elt(next(iter(p.rack)))

    rack_before_refill = len(p.rack)
    bag_before_refill = len(bag)

    p.refill_rack(bag)

    assert len(p.rack) <= 7

    drawn = len(p.rack) - rack_before_refill
    assert drawn >= 0

    assert bag_before_refill - len(bag) == drawn

    assert len(p.rack) == min(7, rack_before_refill + bag_before_refill)


def test_exchange_tiles_delegates_to_exchange():
    bag = tiles.Pick()
    p = player.Player("Carol", bag)

    rack_str = "".join(list(p.rack))
    if rack_str:
        first_tile = rack_str[0]
        ok = p.exchange_tiles(first_tile, bag)
        assert isinstance(ok, bool)


def test_add_points_and_str_and_get_rack_as_str():
    bag = tiles.Pick()
    p = player.Player("Dave", bag)

    p.add_points(10)
    p.add_points(5)
    assert p.score == 15

    rack_str = p.get_rack_as_str()
    assert isinstance(rack_str, str)
    assert "".join(sorted(list(p.rack))) == rack_str

    s = str(p)
    assert "Dave" in s
    assert "15" in s
