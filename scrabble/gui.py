import tkinter as tk
from tkinter import messagebox, simpledialog
import io
import sys

import tiles as tl
import utils
import scoring as sc
import lexicon as lx
from board import Board
import player as pl
import main as gamecore


class ScrabbleGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Scrabble")

        # Données du jeu
        self.dico_lettres = utils.get_values()
        self.mots_fr = set(w.upper() for w in lx.get_words())

        self.board = Board()
        # Même ordre que dans main.main()
        self.board.init_bonus()
        self.board.init_jetons()
        self.bag = tl.Pick()

        self.players: list[pl.Player] = []
        self.current_player_index: int = 0
        self.passes_in_a_row: int = 0
        self.last_word_player_index: int | None = None
        self.game_over: bool = False

        # Interface
        self._build_widgets()

        # Demande des joueurs une fois l'UI prête
        self._setup_players()
        self._refresh_all()

    # ---------- Initialisation joueurs ----------

    def _setup_players(self) -> None:
        while True:
            try:
                nb = simpledialog.askinteger(
                    "Joueurs",
                    "Nombre de joueurs :",
                    minvalue=1,
                    parent=self.root,
                )
                if nb is None:
                    # Fermeture si annulation
                    self.root.destroy()
                    return
                if nb >= 1:
                    break
            except tk.TclError:
                self.root.destroy()
                return

        for i in range(nb):
            name = simpledialog.askstring(
                "Nom du joueur",
                f"Nom du joueur {i + 1} :",
                parent=self.root,
            )
            if not name:
                name = f"Joueur {i + 1}"
            self.players.append(pl.Player(name, self.bag))

    # ---------- Construction UI ----------

    def _build_widgets(self) -> None:
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Plateau
        board_frame = tk.Frame(main_frame)
        board_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 5))

        self.cell_labels: list[list[tk.Label]] = []
        for i in range(15):
            row_labels: list[tk.Label] = []
            for j in range(15):
                lbl = tk.Label(
                    board_frame,
                    text="",
                    width=3,
                    height=1,
                    relief=tk.RIDGE,
                    borderwidth=1,
                    font=("Courier", 10),
                )
                lbl.grid(row=i, column=j, padx=0, pady=0)
                row_labels.append(lbl)
            self.cell_labels.append(row_labels)

        # Informations joueur courant
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.player_info_var = tk.StringVar()
        self.rack_var = tk.StringVar()
        self.bag_var = tk.StringVar()

        tk.Label(right_frame, textvariable=self.player_info_var, anchor="w").pack(
            fill=tk.X
        )
        tk.Label(right_frame, textvariable=self.rack_var, anchor="w").pack(fill=tk.X)
        tk.Label(right_frame, textvariable=self.bag_var, anchor="w").pack(fill=tk.X)

        # Zone de saisie de coup
        move_frame = tk.LabelFrame(right_frame, text="Coup")
        move_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(move_frame, text="Mot :").grid(row=0, column=0, sticky="e")
        self.word_entry = tk.Entry(move_frame, width=15)
        self.word_entry.grid(row=0, column=1, columnspan=3, sticky="w")

        tk.Label(move_frame, text="Ligne (1-15) :").grid(row=1, column=0, sticky="e")
        self.row_entry = tk.Entry(move_frame, width=4)
        self.row_entry.grid(row=1, column=1, sticky="w")

        tk.Label(move_frame, text="Colonne (1-15) :").grid(row=1, column=2, sticky="e")
        self.col_entry = tk.Entry(move_frame, width=4)
        self.col_entry.grid(row=1, column=3, sticky="w")

        tk.Label(move_frame, text="Direction :").grid(row=2, column=0, sticky="e")
        self.dir_var = tk.StringVar(value="H")
        tk.Radiobutton(
            move_frame, text="Horizontal", variable=self.dir_var, value="H"
        ).grid(row=2, column=1, sticky="w")
        tk.Radiobutton(
            move_frame, text="Vertical", variable=self.dir_var, value="V"
        ).grid(row=2, column=2, sticky="w")

        play_btn = tk.Button(move_frame, text="Placer le mot", command=self.play_move)
        play_btn.grid(row=3, column=0, columnspan=4, pady=(5, 0), sticky="ew")

        # Actions simples
        actions_frame = tk.LabelFrame(right_frame, text="Actions")
        actions_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            actions_frame, text="Échanger des lettres", command=self.exchange_tiles
        ).pack(fill=tk.X)
        tk.Button(actions_frame, text="Passer", command=self.pass_turn).pack(fill=tk.X)
        tk.Button(actions_frame, text="Fin de partie", command=self.end_game).pack(
            fill=tk.X
        )

        # Scores globaux
        scores_frame = tk.LabelFrame(right_frame, text="Scores")
        scores_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.scores_text = tk.Text(scores_frame, height=8, width=30, state=tk.DISABLED)
        self.scores_text.pack(fill=tk.BOTH, expand=True)

        # Mise en forme grille principale
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)

    # ---------- Mise à jour affichage ----------

    def _refresh_board(self) -> None:
        stdout_board = self.board.prepare_sdout()
        for i in range(15):
            for j in range(15):
                val = stdout_board[i][j]
                if val is None:
                    val = ""
                self.cell_labels[i][j]["text"] = val

    def _refresh_player_info(self) -> None:
        if not self.players:
            return
        joueur = self.players[self.current_player_index]
        self.player_info_var.set(
            f"Joueur courant : {joueur.name}  |  Score : {joueur.score}"
        )
        self.rack_var.set(f"Main : {joueur.get_rack_as_str()}")
        self.bag_var.set(f"Jetons restants dans le sac : {len(self.bag)}")

        # Scores de tous les joueurs
        self.scores_text.configure(state=tk.NORMAL)
        self.scores_text.delete("1.0", tk.END)
        for p in self.players:
            self.scores_text.insert(tk.END, f"{p.name} : {p.score} points\n")
        self.scores_text.configure(state=tk.DISABLED)

    def _refresh_all(self) -> None:
        self._refresh_board()
        self._refresh_player_info()

    # ---------- Gestion du tour ----------

    @property
    def current_player(self) -> pl.Player:
        return self.players[self.current_player_index]

    def _next_player(self) -> None:
        if not self.players:
            return
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self._refresh_all()

    # ---------- Actions ----------

    def play_move(self) -> None:
        if self.game_over:
            return

        mot = self.word_entry.get().strip().upper()
        if not mot:
            messagebox.showerror("Erreur", "Vous devez saisir un mot.")
            return

        try:
            i = int(self.row_entry.get().strip()) - 1
            j = int(self.col_entry.get().strip()) - 1
        except ValueError:
            messagebox.showerror("Erreur", "Coordonnées invalides.")
            return

        if not (0 <= i < self.board.size and 0 <= j < self.board.size):
            messagebox.showerror("Erreur", "Coordonnées hors du plateau.")
            return

        direction = self.dir_var.get().upper()
        if direction not in ("H", "V"):
            messagebox.showerror("Erreur", "Direction invalide.")
            return

        joueur = self.current_player

        # Capture des messages de placer_mot (pour réutiliser les textes existants)
        old_stdout = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            ok, score_coup = gamecore.placer_mot(
                self.board,
                joueur,
                mot,
                i,
                j,
                direction,
                self.dico_lettres,
                self.mots_fr,
            )
        finally:
            sys.stdout = old_stdout

        log = buffer.getvalue().strip()

        if not ok:
            if log:
                messagebox.showerror("Coup invalide", log)
            else:
                messagebox.showerror("Coup invalide", "Le coup n'est pas valide.")
            return

        # Coup accepté
        joueur.add_points(score_coup)
        self.last_word_player_index = self.current_player_index
        self.passes_in_a_row = 0

        # Repioche
        manque = 7 - len(joueur.rack)
        if gamecore.fin_de_partie(self.bag, manque):
            # plus assez de jetons pour compléter : fin automatique
            messagebox.showinfo(
                "Fin de partie",
                "Plus assez de jetons dans le sac pour compléter la main.",
            )
            self.end_game()
            return

        if manque > 0:
            joueur.rack.add_elts(self.bag.draw(manque))

        self.word_entry.delete(0, tk.END)
        self._refresh_all()
        self._next_player()

    def exchange_tiles(self) -> None:
        if self.game_over:
            return

        joueur = self.current_player
        tiles_str = simpledialog.askstring(
            "Échange",
            "Lettres à échanger (ex: AE?) :",
            parent=self.root,
        )
        if tiles_str is None or tiles_str.strip() == "":
            return

        tiles_str = tiles_str.strip().upper()

        ok = joueur.exchange_tiles(tiles_str, self.bag)
        if not ok:
            messagebox.showerror(
                "Échange impossible",
                "Échange non valide (lettres manquantes ou sac insuffisant).",
            )
            return

        # Un tour sans jouer de mot compte comme "passe" pour la logique simple
        self.passes_in_a_row += 1
        self._refresh_all()
        self._next_player()

    def pass_turn(self) -> None:
        if self.game_over:
            return

        self.passes_in_a_row += 1
        # Règle simple : si tout le monde passe deux fois de suite, on peut proposer de finir
        seuil = 2 * len(self.players)
        if self.passes_in_a_row >= seuil:
            if messagebox.askyesno(
                "Fin possible",
                "Beaucoup de passes consécutives.\nVoulez-vous terminer la partie ?",
            ):
                self.end_game()
                return

        self._next_player()

    # ---------- Fin de partie ----------

    def end_game(self) -> None:
        if self.game_over:
            return
        self.game_over = True

        if not self.players:
            self.root.destroy()
            return

        # Calcul des malus
        malus_par_joueur = {
            j: gamecore.calcul_malus_joueur(j, self.dico_lettres) for j in self.players
        }
        total_malus = sum(malus_par_joueur.values())

        # Application des malus
        for joueur, malus in malus_par_joueur.items():
            joueur.score -= malus

        # Bonus pour le dernier joueur ayant posé un mot
        if self.last_word_player_index is not None:
            dernier = self.players[self.last_word_player_index]
            dernier.score += total_malus
            last_name = dernier.name
        else:
            last_name = "Aucun"

        self._refresh_all()

        # Résumé final
        lines = []
        lines.append(f"Dernier joueur à avoir joué un mot : {last_name}\n")
        lines.append("Scores finaux :")
        max_score = max(j.score for j in self.players)
        winners = [j.name for j in self.players if j.score == max_score]
        for j in self.players:
            lines.append(f"- {j.name} : {j.score} points")

        if len(winners) == 1:
            lines.append(f"\nGagnant : {winners[0]}")
        else:
            lines.append("\nÉgalité entre : " + ", ".join(winners))

        messagebox.showinfo("Fin de partie", "\n".join(lines))

    # ---------- Boucle principale ----------


def main() -> None:
    root = tk.Tk()
    app = ScrabbleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
