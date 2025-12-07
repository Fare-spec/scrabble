import random as rng
import utils


class Rack:
    def __init__(self) -> None:
        self.rack = list()

    def add_elt(self, elt: str) -> None:
        self.rack.append(elt)

    def add_elts(self, elts: list[str]) -> None:
        for elt in elts:
            self.add_elt(elt)

    def remove_elt(self, elt: str) -> None:
        self.rack.remove(elt)

    def remove_elts(self, elts: list[str]) -> list[str]:
        for elt in elts:
            self.remove_elt(elt)
        return elts

    def __len__(self) -> int:
        return len(self.rack)

    def __iter__(self):
        return iter(self.rack)


class Pick:
    def __init__(self) -> None:
        pick_dico = utils.get_values()
        self.init_pick(pick_dico)

    def init_pick(self, dico: dict[str, dict[str, int]]) -> None:
        pick = list()
        for letter, occ in dico.items():
            for _ in range(occ["occ"]):
                pick.append(letter)
        self.pick = pick

    def add_elt(self, elt: str) -> None:
        self.pick.append(elt)

    def add_elts(self, elts: list[str]) -> None:
        for elt in elts:
            self.add_elt(elt)

    def draw(self, quantity: int) -> list[str]:
        return self.remove_elts(rng.sample(self.pick, k=quantity))

    def remove_elts(self, elts: list[str]) -> list[str]:
        for tiles in elts:
            self.pick.remove(tiles)
        return elts

    def __iter__(self):
        return iter(self.pick)

    def __len__(self) -> int:
        return len(self.pick)


def exchange(tiles: str, rack: Rack, bag: Pick):
    change_size = len(tiles)
    l_tiles = [tile for tile in tiles]
    # We first verify if all tiles are in the rack and that there are enough tiles into the bag
    if all(elt in rack for elt in tiles) and change_size <= len(bag):
        # first we remove tiles from the rack
        rack.remove_elts(l_tiles)
        # then we pick tiles from the rack
        rack.add_elts(bag.draw(change_size))
        # then we put back those we wanted to exchange
        bag.add_elts(l_tiles)
        return True
    return False


def echanger(jetons: str, main: Rack, sac: Pick):
    return exchange(jetons, main, sac)


def complete_rack(rack: Rack, bag: Pick) -> None:
    missing = 7 - len(rack)
    pick_size = len(bag)
    if pick_size != 0:
        if pick_size >= missing:
            pick(bag, missing)
        else:
            pick(bag, pick_size)


def completer_main(main: Rack, sac: Pick) -> None:
    complete_rack(main, sac)


def pick(bag: Pick, x: int) -> list[str]:
    return bag.draw(x)


def piocher(sac: Pick, x: int) -> list[str]:
    return pick(sac, x)


def init_pioche_alea() -> list:
    return list(Pick())


# Debug functions
# Were usefull until we changed the pick function at Q4.21
def frequencies_percent(lst):
    """
    Allow us to verify that the previous function is truly random and no error were committed
    """
    total = len(lst)
    unique = set(lst)
    return {x: lst.count(x) / total * 100 for x in unique}


def display_frequencies(lst):
    """
    Simply display the frequencies in percent
    """

    freq = frequencies_percent(lst)
    for k, v in sorted(freq.items(), key=lambda x: -x[1]):
        print(f"{k}: {v:.2f}%")


if __name__ == "__main__":
    liste = init_pioche_alea()
    display_frequencies(liste)
