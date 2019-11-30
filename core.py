from typing import Optional, List


# ToDo Set `set` too `multiset`

class Core:
    def __init__(self, dictionary: tuple):
        self._dict = {word: set(word) for word in dictionary}

    def find_anagram(self, string: str) -> Optional[str]:
        string = set(string)  # n*log(n)

        for word, letters in self._dict:  # m
            if len(word) != len(string):
                continue

            if len(string) == len(letters.intersection(string)):  # O(min(l), min(r))
                return word

    def update_dict(self, new_words: List[str]) -> int:
        for word in new_words:
            self._dict[word] = set(word)
