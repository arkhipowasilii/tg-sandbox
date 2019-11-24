from typing import Optional, List


class Core:
    def __init__(self, dictionary: tuple):
        self._dict = set(dictionary)

    def find_anagram(self, string: str) -> Optional[str]:
        for word in self._dict:
            if len(word) == len(string):
                for char in string:
                    if char not in word:
                        break
                    else:
                        return word

    def update_dict(self, new_words: List[str]) -> int:
        for word in new_words:
            self._dict.add(word)
