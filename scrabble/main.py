import tiles as tl
import utils
import scoring as sc
import lexicon as lx
from board import Board
import player as pl


def asking(question: str) -> str:
    return input(question)


def fin_de_partie(bag: tl.Pick, needed: int) -> bool:
    """
    Vrai si le joueur voudrait piocher `needed` jetons mais
    qu'il n'en reste plus assez dans le sac.
    """
    return needed > 0 and len(bag) < needed


def prochain_joueur(index: int, nb_joueurs: int) -> int:
    """
    Retourne l'indice du joueur suivant (ordre circulaire).
    """
    return (index + 1) % nb_joueurs


def _cell_has_letter(cell: str) -> bool:
    """Vrai si la case contient au moins une lettre."""
    return any(c.isalpha() for c in cell)


def _cell_empty(cell: str) -> bool:
    """Vrai si la case ne contient aucune lettre (éventuellement juste des bonus 2,3,²,³)."""
    return not _cell_has_letter(cell)


def _cell_letter(cell: str) -> str:
    """Renvoie la lettre présente dans la case (en majuscule), ou '' s'il n'y en a pas."""
    for c in cell:
        if c.isalpha():
            return c.upper()
    return ""


def lire_coords(board: Board) -> tuple[int, int]:
    """Demande des coordonnées jusqu'à obtenir une case vide du plateau."""
    while True:
        entree = asking(
            "Coordonnées de départ du mot (ligne colonne, par ex. '8 8') : "
        ).strip()
        morceaux = entree.split()
        if len(morceaux) != 2:
            print("Veuillez entrer deux entiers séparés par un espace.")
            continue
        try:
            lig = int(morceaux[0]) - 1
            col = int(morceaux[1]) - 1
        except ValueError:
            print("Coordonnées invalides, recommencez.")
            continue
        if not (0 <= lig < board.size and 0 <= col < board.size):
            print("Coordonnées hors du plateau.")
            continue

        cell = board.board[lig][col]
        if not _cell_empty(cell):
            print("Case déjà occupée, choisissez une case vide.")
            continue
        return lig, col


def tester_placement(plateau, i: int, j: int, direction: str, mot: str):
    """Vérifie si `mot` est plaçable à partir de (i, j) dans `direction`.

    Renvoie la liste des lettres à ajouter (cases vides rencontrées) ou
    la liste vide si le placement est impossible.
    """
    n = len(mot)
    taille = len(plateau)
    direction = direction.upper()
    mot = mot.upper()

    if direction not in ("H", "V"):
        return []

    if direction == "H":
        if j + n > taille:
            return []
    else:
        if i + n > taille:
            return []

    lettres_a_placer = []

    for k, ch in enumerate(mot):
        lig = i + (direction == "V") * k
        col = j + (direction == "H") * k
        cell = plateau[lig][col]
        existing = _cell_letter(cell)

        if existing == "":
            lettres_a_placer.append(ch)
        elif existing == ch:
            continue
        else:
            return []

    if not lettres_a_placer:
        return []

    return lettres_a_placer


def plateau_vide(plateau) -> bool:
    return all(_cell_empty(case) for ligne in plateau for case in ligne)


def mot_au_contact(plateau, i: int, j: int, direction: str, mot: str) -> bool:
    """Vérifie que le mot est au contact d'au moins une lettre déjà posée."""
    if plateau_vide(plateau):
        return True

    taille = len(plateau)
    direction = direction.upper()
    mot = mot.upper()

    for k in range(len(mot)):
        lig = i + (direction == "V") * k
        col = j + (direction == "H") * k

        if _cell_has_letter(plateau[lig][col]):
            return True

        for dl, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nl, nc = lig + dl, col + dc
            if 0 <= nl < taille and 0 <= nc < taille:
                if _cell_has_letter(plateau[nl][nc]):
                    return True

    return False


def lettres_disponibles(necessaires, rack) -> bool:
    """Vérifie que les lettres nécessaires sont disponibles dans la main,
    en tenant compte des jokers.
    """
    temp = rack.copy()
    for ch in necessaires:
        if ch in temp:
            temp.remove(ch)
        elif utils.JOKER in temp:
            temp.remove(utils.JOKER)
        else:
            return False
    return True


def _extend_word(plateau, i: int, j: int, direction: str):
    """À partir de la case (i,j) contenant une lettre, étend dans les deux
    sens pour récupérer le mot complet dans `direction`.
    Renvoie (mot, start_i, start_j).
    """
    taille = len(plateau)
    direction = direction.upper()
    if direction == "H":
        dl, dc = 0, 1
    else:
        dl, dc = 1, 0

    l, c = i, j
    while True:
        nl, nc = l - dl, c - dc
        if 0 <= nl < taille and 0 <= nc < taille and _cell_has_letter(plateau[nl][nc]):
            l, c = nl, nc
        else:
            break

    start_i, start_j = l, c
    lettres = []
    while 0 <= l < taille and 0 <= c < taille and _cell_has_letter(plateau[l][c]):
        lettres.append(_cell_letter(plateau[l][c]))
        l += dl
        c += dc

    return "".join(lettres), start_i, start_j


def _simuler_coup(plateau, i: int, j: int, direction: str, mot: str, mots_fr):
    """Simule le coup sur une copie du plateau.

    Vérifie:
    - plaçabilité (tester_placement)
    - contact avec des lettres existantes
    - validité du mot principal
    - validité de tous les mots perpendiculaires créés

    Renvoie (ok, mots_formes, lettres_a_placer) avec
    mots_formes = [(mot, si, sj, dir), ...]
    """
    mot = mot.upper()
    direction = direction.upper()

    lettres_a_placer = tester_placement(plateau, i, j, direction, mot)
    if not lettres_a_placer:
        return False, [], []

    if not mot_au_contact(plateau, i, j, direction, mot):
        return False, [], []

    temp = [ligne[:] for ligne in plateau]

    for k, ch in enumerate(mot):
        lig = i + (direction == "V") * k
        col = j + (direction == "H") * k
        if not _cell_has_letter(temp[lig][col]):
            temp[lig][col] = ch

    mots_formes = []

    mot_principal, si, sj = _extend_word(temp, i, j, direction)
    if mot_principal not in mots_fr:
        return False, [], []

    mots_formes.append((mot_principal, si, sj, direction))

    dir_perp = "V" if direction == "H" else "H"
    for k, ch in enumerate(mot):
        lig = i + (direction == "V") * k
        col = j + (direction == "H") * k

        if _cell_has_letter(plateau[lig][col]):
            continue

        mot_perp, si_p, sj_p = _extend_word(temp, lig, col, dir_perp)
        if len(mot_perp) <= 1:
            continue

        if mot_perp not in mots_fr:
            return False, [], []

        mots_formes.append((mot_perp, si_p, sj_p, dir_perp))

    return True, mots_formes, lettres_a_placer


def placer_mot(
    board: Board,
    joueur: pl.Player,
    mot: str,
    i: int,
    j: int,
    direction: str,
    dico_lettres,
    mots_fr,
):
    """Tente de placer `mot` sur le plateau en partant de (i, j) dans `direction`.

    - utilise tester_placement
    - respecte les lettres déjà posées
    - impose le contact avec des lettres déjà posées (sauf premier mot)
    - vérifie la validité de tous les mots formés (principal + perpendiculaires)
    - calcule le score total avec les bonus

    Modifie le plateau et la main du joueur uniquement en cas de succès.
    Renvoie (réussi: bool, score_coup: int).
    """
    plateau = board.board
    mot = mot.upper()
    direction = direction.upper()

    lettres_a_placer = tester_placement(plateau, i, j, direction, mot)
    if not lettres_a_placer:
        return False, 0

    if not lettres_disponibles(lettres_a_placer, list(joueur.rack)):
        return False, 0

    ok, mots_formes, _ = _simuler_coup(plateau, i, j, direction, mot, mots_fr)
    if not ok:
        return False, 0

    for k, ch in enumerate(mot):
        lig = i + (direction == "V") * k
        col = j + (direction == "H") * k
        if not _cell_has_letter(plateau[lig][col]):
            plateau[lig][col] = ch

    for ch in lettres_a_placer:
        if ch in joueur.rack:
            joueur.rack.remove_elt(ch)
        elif utils.JOKER in joueur.rack:
            joueur.rack.remove_elt(utils.JOKER)

    score_total = 0
    for mot_f, si, sj, dir_f in mots_formes:
        score_total += sc.word_value_on_board(mot_f, dico_lettres, si, sj, dir_f)

    return True, score_total


def tour_joueur(
    board: Board,
    joueur: pl.Player,
    bag: tl.Pick,
    dico_lettres,
    mots_fr,
):
    """
    Gère le tour d'un joueur.
    Affiche le plateau, demande l'action (passer, échanger, proposer un mot)
    et applique l'action.
    Renvoie False si la partie doit se terminer (pas assez de lettres pour piocher),
    True sinon.
    """
    board.affiche_jetons()
    print()
    print(f"Au tour de {joueur.name} — score: {joueur.score}")
    print(f"Main : {joueur.get_rack_as_str()}")

    options = ("P", "E", "S")
    question = "Que voulez-vous faire ? [P]asser, [E]changer, [S]uggérer un mot : "

    answer = ""
    while answer not in options:
        answer = asking(question).strip().upper()
        if answer not in options:
            print("Réponse invalide. Tapez P, E ou S.")

    if answer == "P":
        return True

    if answer == "E":
        while True:
            lettres = (
                asking("Lettres à échanger (sans espaces, vide pour annuler) : ")
                .strip()
                .upper()
            )

            if lettres == "":
                return True

            if len(lettres) > 7:
                print("Vous ne pouvez pas échanger plus de 7 lettres.")
                continue

            if not joueur.has_tiles(lettres):
                print("Vous n'avez pas toutes ces lettres dans votre main.")
                continue

            if fin_de_partie(bag, len(lettres)):
                print("Plus assez de jetons dans le sac pour effectuer l'échange.")
                return False

            ok = joueur.exchange_tiles(lettres, bag)
            if not ok:
                print("Échange impossible (sac insuffisant).")
                return False

            print("Échange effectué.")
            print(f"Nouvelle main : {joueur.get_rack_as_str()}")
            return True

    while True:
        mot = asking("Mot proposé (vide pour annuler) : ").strip().upper()
        if mot == "":
            return True

        if mot not in mots_fr:
            print("Mot absent du dictionnaire, recommencez.")
            continue

        direction = ""
        while direction not in ("H", "V"):
            direction = (
                asking("Direction du mot [H]orizontale ou [V]erticale : ")
                .strip()
                .upper()
            )
            if direction not in ("H", "V"):
                print("Réponse invalide. Tapez H ou V.")

        i, j = lire_coords(board)

        reussi, score_coup = placer_mot(
            board, joueur, mot, i, j, direction, dico_lettres, mots_fr
        )
        if not reussi:
            print(
                "Placement impossible à cet endroit (lettres, contact ou mots perpendiculaires invalides)."
            )
            continue

        break

    print(f"Valeur du coup (tous mots) : {score_coup} points.")
    joueur.add_points(score_coup)

    board.affiche_jetons()

    manque = 7 - len(joueur.rack)
    if fin_de_partie(bag, manque):
        print("Plus assez de jetons dans le sac pour compléter la main.")
        return False

    if manque > 0:
        joueur.rack.add_elts(bag.draw(manque))

    print(f"Nouvelle main : {joueur.get_rack_as_str()}")
    return True


def calcul_malus_joueur(joueur: pl.Player, dico_lettres) -> int:
    """
    Somme des valeurs des jetons restants en main.
    """
    total = 0
    for t in joueur.rack:
        total += dico_lettres[t]["val"]
    return total


def main():
    dico_lettres = utils.get_values()
    mots_fr = lx.get_words()

    board = Board()
    board.init_bonus()
    board.init_jetons()
    bag = tl.Pick()

    nb = 0
    while nb <= 0:
        try:
            nb = int(asking("Nombre de joueurs : ").strip())
        except ValueError:
            nb = 0
        if nb <= 0:
            print("Entrez un entier strictement positif.")

    joueurs = []
    for i in range(nb):
        nom = asking(f"Nom du joueur {i + 1} : ").strip()
        if nom == "":
            nom = f"Joueur{i + 1}"
        joueurs.append(pl.Player(nom, bag))

    courant = 0
    partie_terminee = False
    indice_dernier = 0

    while not partie_terminee:
        joueur = joueurs[courant]
        indice_dernier = courant

        continue_game = tour_joueur(board, joueur, bag, dico_lettres, mots_fr)
        if not continue_game:
            partie_terminee = True
        else:
            courant = prochain_joueur(courant, nb)

    print("\nFin de partie.")
    dernier = joueurs[indice_dernier]

    for i, j in enumerate(joueurs):
        if i == indice_dernier:
            continue
        malus = calcul_malus_joueur(j, dico_lettres)
        if malus > 0:
            j.add_points(-malus)
            print(
                f"{j.name} perd {malus} points de malus "
                f"(lettres restantes : {j.get_rack_as_str()})."
            )

    print(f"\n{dernier.name} était le dernier à jouer.")

    print("\nScores finaux :")
    for j in joueurs:
        print(f"{j.name} : {j.score} points")

    max_score = max(j.score for j in joueurs)
    gagnants = [j.name for j in joueurs if j.score == max_score]

    if len(gagnants) == 1:
        print(f"Gagnant : {gagnants[0]}")
    else:
        print("Égalité entre : " + ", ".join(gagnants))


if __name__ == "__main__":
    main()
