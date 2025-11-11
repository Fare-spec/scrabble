from pathlib import Path


TAILLE_PLATEAU = 15
TAILLE_MARGE = 4
JOKER = "?"
# Permet d'aller chercher les fichiers dans ../data/*
DATA_DIR: Path = Path(__file__).resolve().parents[1] / "data"


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


def generer_dico():
    jetons = {}
    with Path("lettres.txt").open(encoding="utf_8") as lettres:
        for ligne in lettres:
            l, v, o = ligne.strip().split(";")
            jetons[l] = {"occ": int(o), "val": int(v)}
    return jetons
