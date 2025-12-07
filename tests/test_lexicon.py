import lexicon as lx


def test_get_words_uses_littre():
    words = lx.get_words()
    assert len(words) > 50_000
    # Mot connu dans littre.txt
    assert "ABACA" in words


def test_words_starting_returns_only_matching_letter():
    words = ["ABACA", "BABA", "ABANDON", "TEST"]
    result = lx.words_starting(words, "A")

    assert set(result) == {"ABACA", "ABANDON"}
    assert all(w.startswith("A") for w in result)


def test_select_length_filters_by_length():
    words = ["A", "AB", "ABC", "ABCD"]
    result = lx.select_length(words, 2)
    assert result == ["AB"]

    result3 = lx.select_length(words, 3)
    assert result3 == ["ABC"]


def test_playable_word_basic_and_joker():
    assert lx.playable_word("ABACA", list("ABACA")) is True

    # Manque un C mais joker présent
    assert lx.playable_word("ABACA", list("ABA?A")) is True

    # Manque C et pas de joker
    assert lx.playable_word("ABACA", list("ABAAA")) is False


def test_playable_words_with_missing_on_board_letters():
    words = ["ABACA", "TEST", "ABA"]
    letters = list("ABA")

    playable = lx.playable_words(words, letters.copy(), missing=2)

    assert "ABA" in playable
    assert "ABACA" in playable
    # "TEST" impossible avec seulement A/B/jokers
    assert "TEST" not in playable
