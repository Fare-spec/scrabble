import utils


def get_words(path: str = "data/b.txt") -> list[str]:
    return utils.generer_dictfr(path)


def words_starting(words: list[str], letter: str) -> list[str]:
    starting_with = list()
    for word in words:
        if word[0].lower() == letter.lower():
            starting_with.append(word)
    return starting_with


def select_length(words: list[str], length: int) -> list[str]:
    len_words = list()
    for word in words:
        if len(word) == length:
            len_words.append(word)
    return len_words


def playable_word(word: str, letters: list[str]) -> bool:
    temp = letters.copy()
    for ch in word:
        if ch in temp:
            temp.remove(ch)
        elif "?" in temp:
            temp.remove("?")  # Used as a wildcard
        else:
            return False
    return True


def playable_words(words: list[str], letters: list[str], missing: int = 0) -> list[str]:
    result = []
    letters += [
        "?" for _ in range(missing)
    ]  # Use to create a word with letters already on the board
    for w in words:
        if playable_word(w, letters):
            result.append(w)
    return result


# Tests


def tests():
    def verify_get_words():
        word_list = get_words()

        # assert len(word_list) == 73085, (
        #   "The length of the list does not match with the statement"
        # )
        u_starting = []
        for word in word_list:
            if word[0].lower() == "u":
                u_starting.append(word)
        # print(u_starting)

    verify_get_words()

    def verify_words_starting(words):
        words = words_starting(words, "y")
        # assert len(words) == 32, (
        #  "The number of words starting with y doesn't match the statement"
        # )

    def verify_select_length(words):
        len_19 = select_length(words, 19)
        # assert len(len_19) == 39
        # assert len(select_length(words, 23)) == 1

    words = get_words()
    verify_words_starting(words)
    verify_select_length(words)
