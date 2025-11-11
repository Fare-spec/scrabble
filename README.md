# Structure du projet Scrabble

## Arborescence

```

scrabble/
├─ pyproject.toml
├─ README.md
├─ docs/
│  └─ questions.md            ← énoncés, variantes, pistes bonus (hors exécutable)
├─ data/
│  ├─ littre.txt
│  └─ lettres.txt
├─ scrabble/                  ← paquet exécutable
│  ├─ **init**.py
│  ├─ main.py                 ← point d’entrée CLI (boucle de jeu complète)
│  ├─ board.py                ← plateau: bonus, grille, placements (Items 1, 29–33)
│  ├─ tiles.py                ← pioche, main, échanges (Items 7–11, 20–21)
│  ├─ lexicon.py              ← chargement dictionnaire, filtres (Items 12–14)
│  ├─ rack_words.py           ← jouabilité main + jokers (Items 15–18, 23–24)
│  ├─ scoring.py              ← valeur lettres/mots, Scrabble, bonus de cases (Items 22, 32–33)
│  ├─ player.py               ← modèle joueur : nom, score, main, actions (Items 25–28, 34–35)
│  ├─ game.py                 ← moteur : tours, fin de partie, ordre joueurs (Items 25–28, 34–35)
│  ├─ io_cli.py               ← I/O textuels : lecture coords, affichages (Items 3–6, 25, 29)
│  ├─ ui_gui.py               ← façade optionnelle GUI (bonus)
│  └─ utils.py                ← helpers : validation, erreurs, constantes
└─ tests/
├─ test_board.py
├─ test_tiles.py
├─ test_lexicon.py
├─ test_rack_words.py
├─ test_scoring.py
├─ test_game.py
└─ test_player.py

```

## Rôle des répertoires

- **docs/** — contient les textes du sujet, les variantes et les questions non exécutables.
- **data/** — fichiers externes nécessaires au jeu (dictionnaire, valeurs des lettres).
- **scrabble/** — cœur du programme Python, organisé en modules indépendants.
- **tests/** — tests unitaires pour chaque composant du projet.

## Description des modules

| Fichier | Rôle principal |
|----------|----------------|
| `__init__.py` | marque le dossier comme package importable |
| `main.py` | point d’entrée, boucle de jeu principale |
| `board.py` | gestion du plateau, des bonus et du placement des mots |
| `tiles.py` | pioche, échanges, gestion de la main |
| `lexicon.py` | lecture du dictionnaire et filtres simples |
| `rack_words.py` | sélection des mots jouables avec une main donnée |
| `scoring.py` | calcul des valeurs de mots et bonus de placement |
| `player.py` | définition du joueur (nom, score, main, actions) |
| `game.py` | logique de partie à plusieurs joueurs |
| `io_cli.py` | interface textuelle : affichages, saisies |
| `ui_gui.py` | interface graphique (optionnelle, bonus) |
| `utils.py` | fonctions communes, constantes, validations |

## Dépendances entre modules

```

main.py   → game, io_cli
game.py   → board, tiles, lexicon, rack_words, scoring, player, io_cli, utils
player.py → tiles, rack_words, utils
board.py  → utils
tiles.py  → utils
lexicon.py→ utils
rack_words.py → lexicon, utils
scoring.py → board (bonus cases), utils
io_cli.py → board (affichage), utils

```
