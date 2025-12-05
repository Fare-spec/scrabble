from tiles import Pick, Rack, exchange


class Player:
    def __init__(self, name: str, bag: Pick) -> None:
        """
        Create a player with a name, an empty rack and 0 score.
        The rack is immediately filled up to 7 tiles from the bag.
        """
        self.name = name
        self.rack = Rack()
        self.score = 0
        self.refill_rack(bag)

    def refill_rack(self, bag: Pick) -> None:
        """
        Draw tiles from the bag so that the rack contains at most 7 tiles.
        Does nothing if the bag is empty.
        """
        missing = 7 - len(self.rack)
        if missing <= 0 or len(bag) == 0:
            return

        to_draw = min(missing, len(bag))
        self.rack.add_elts(bag.draw(to_draw))

    def has_tiles(self, tiles: str) -> bool:
        """
        Return True if the player has all tiles in `tiles` in their rack
        (taking multiplicity into account).
        """
        temp = list(self.rack)
        for t in tiles:
            if t in temp:
                temp.remove(t)
            else:
                return False
        return True

    def play_tiles(self, tiles: str) -> bool:
        """
        Remove the given tiles from the rack if possible.
        Return True on success, False otherwise.
        """
        if not self.has_tiles(tiles):
            return False
        self.rack.remove_elts(list(tiles))
        return True

    def exchange_tiles(self, tiles: str, bag: Pick) -> bool:
        """
        Use the existing `exchange` logic from tiles.py.
        Return True if the exchange was successful.
        """
        return exchange(tiles, self.rack, bag)

    def add_points(self, points: int) -> None:
        """Increase the player's score by `points`."""
        self.score += points

    def get_rack_as_str(self) -> str:
        """Return the rack as a sorted string of tiles (for display)."""
        return "".join(sorted(self.rack))

    def __str__(self) -> str:
        return f"{self.name} ({self.score} pts) : {self.get_rack_as_str()}"
