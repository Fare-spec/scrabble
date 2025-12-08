import lexicon as lx
import utils


def word_value(word: str, dico: dict[str, dict[str, int]]) -> int:
    value: int = 0 if len(word) < 8 else 50
    for letter in word.upper():
        # .upper because of the data contained in the dictionnary
        value += dico[letter]["val"]
    return value


def word_value_on_board(
    word: str,
    dico: dict[str, dict[str, int]],
    i: int,
    j: int,
    direction: str,
) -> int:
    """
    Compute value of a word depending of the state of the board

    """
    bonus_board = utils.init_bonus()
    taille = len(bonus_board)
    direction = direction.upper()
    word = word.upper()

    total_lettres = 0
    multiplicateur_mot = 1

    for k, ch in enumerate(word):
        lig = i + (direction == "V") * k
        col = j + (direction == "H") * k
        if not (0 <= lig < taille and 0 <= col < taille):
            return 0

        valeur_lettre = dico[ch]["val"]
        bonus = bonus_board[lig][col]

        if bonus == "LD":
            valeur_lettre *= 2
        elif bonus == "LT":
            valeur_lettre *= 3
        elif bonus == "MD":
            multiplicateur_mot *= 2
        elif bonus == "MT":
            multiplicateur_mot *= 3

        total_lettres += valeur_lettre

    total = total_lettres * multiplicateur_mot

    if len(word) >= 8:
        total += 50

    return total


def best_word(
    motsfr: list[str],
    ll: list[str],
    dico: dict[str, dict[str, int]],
    multiple=False,
) -> str | list[str]:
    """
    Search the maximum into the playable words... Would have been very interesting to make a BFS somehow
    We could enhanced this function because it calculate EACH times the best word instead we could do some 'memoisation' using a set or a dictionnary outside the function and give it in arg.
    """
    mots_jouables = lx.playable_words(motsfr, ll.copy())
    if not multiple:
        best = ""
        best_score = 0

        for w in mots_jouables:
            score = word_value(w, dico)
            if score > best_score:
                best = w
                best_score = score
            elif score == best_score and len(w) > len(best):  # Tie breaker
                best = w
        return best
    else:
        best = [""]
        best_score = 0

        for w in mots_jouables:
            score = word_value(w, dico)
            if score > best_score:
                best = [w]
                best_score = score
            elif score == best_score:
                best += [w]
        return best


def meilleur_mot(
    motsfr: list[str], ll: list[str], dico: dict[str, dict[str, int]]
) -> str:
    string = best_word(motsfr, ll, dico)

    if not isinstance(string, str):
        return str()
    return string


def meilleurs_mots(
    motsfr: list[str], ll: list[str], dico: dict[str, dict[str, int]]
) -> list[str]:
    liste = best_word(motsfr, ll, dico, multiple=True)

    if not isinstance(liste, list):
        return list()
    return liste


def test():
    words = ["COURIR", "PIED", "DEPIT", "TAPIR", "MARCHER"]
    ll = ["P", "I", "D", "E", "T", "A", "R"]
    dico = utils.get_values()
    assert best_word(words, ll, dico) == "DEPIT"
    words2 = lx.get_words()
    l2 = "AZDPEBT"
    l2 = l2.upper()
    ll2 = [letter for letter in l2]
    best = best_word(words2, ll2, dico, multiple=True)
    score = [word_value(word, dico) for word in best]
    print(best, score)


if __name__ == "__main__":
    test()
