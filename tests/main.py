import sys
import pytest


def run_all_tests():
    """
    Lance tous les tests pytest trouvés dans le projet.
    Retourne le code de sortie pytest (0 si tout passe).
    """
    # -q : mode "quiet"
    # -r a : affiche un résumé de tous les tests (succès / échecs / xfails, etc.)
    return pytest.main(["-q", "-r", "a"])


if __name__ == "__main__":
    exit_code = run_all_tests()

    if exit_code == 0:
        print("Tous les tests ont réussi.")
    else:
        print(f"Certains tests ont échoué (code de retour pytest = {exit_code}).")

    sys.exit(exit_code)
