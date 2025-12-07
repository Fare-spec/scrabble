from pathlib import Path


TAILLE_PLATEAU = 15
TAILLE_MARGE = 4
JOKER = "?"


def symetrise_liste(lst):
    copie_lst = list(lst)
    for i in range(2, len(copie_lst) + 1):
        lst.append(copie_lst[-i])


def init_bonus():
    plt_bonus = [
        ["MT", "", "", "LD", "", "", "", "MT"],
        ["", "MD", "", "", "", "LT", "", ""],
        ["", "", "MD", "", "", "", "LD", ""],
        ["LD", "", "", "MD", "", "", "", "LD"],
        ["", "", "", "", "MD", "", "", ""],
        ["", "LT", "", "", "", "LT", "", ""],
        ["", "", "LD", "", "", "", "LD", ""],
        ["MT", "", "", "LD", "", "", "", "MD"],
    ]
    for ligne in plt_bonus:
        symetrise_liste(ligne)
    symetrise_liste(plt_bonus)

    return plt_bonus


def generer_dictfr(nf="littre.txt"):
    mots = []
    with Path(nf).open(encoding="utf_8") as fich_mots:
        for line in fich_mots:
            mots.append(line.strip().upper())
    return mots


def generer_dico(
    nf: str = "lettres.txt",
):  # I allowed myself to add an arg to this function considering the architecture of the project
    jetons = {}
    with Path(nf).open(encoding="utf_8") as lettres:
        for ligne in lettres:
            l, v, o = ligne.strip().split(";")
            jetons[l] = {"occ": int(o), "val": int(v)}
    return jetons


# Student functions:


def get_values(path: str = "lettres.txt") -> dict[str, dict[str, int]]:
    dico = generer_dico(path)
    return dico
