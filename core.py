from typing import Optional, List
from multiset import Multiset


class Core:
    def __init__(self, dictionary: tuple):
        self._dict = {word: Multiset(word) for word in dictionary}

    def find_anagram(self, string: str) -> Optional[str]:
        string = Multiset(string)

        for word, letters in self._dict.items():
            if len(word) != len(string):
                continue

            if len(string) == len(letters.intersection(string)):
                return word

    def update_dict(self, new_words: List[str]):
        for word in new_words:
            self._dict[word] = Multiset(word)

    @staticmethod
    def check_palindrome(string: str) -> bool:
        if string == string[::-1]:
            return True
        else:
            return False


if __name__ == '__main__':
    words = ("asd", "qwe")
    core = Core(words)
    print(core.find_anagram("weq"))
    print(core.check_palindrome("tvvt"))
