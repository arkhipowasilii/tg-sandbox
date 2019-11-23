from typing import Optional, List


class Core:
    def __init__(self, dictionary: tuple):
        self._dict = set(dictionary)

    def find_anagram(self, string: str) -> Optional[List[str]]:
        result = []
        for word in self._dict:
            if len(word) == len(string):
                for char in string:
                    if char not in word:
                        break
                    else:
                        result.append(word)
        return result

    def update_dict(self, new_words: List[str]) -> int:
        for word in new_words:
            self._dict.add(word)
