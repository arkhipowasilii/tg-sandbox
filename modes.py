from enum import Enum

from greeting_mode import GreetingMode
from palindrome_mode import PalindromeMode
from anagram_mode import AnagramMode


class Modes(Enum):
    Anagram = AnagramMode
    Palindrome = PalindromeMode
    Greeting = GreetingMode

    @property
    def command(self) -> str:
        return self.value.command()

    @property
    def handler(self):
        return self.value