from enum import Enum

from modes.greeting_mode import GreetingMode
from modes.palindrome_mode import PalindromeMode
from modes.anagram_mode import AnagramMode
from modes.keyboard_mode import KeyboardMode


class Modes(Enum):
    Anagram = AnagramMode
    Palindrome = PalindromeMode
    Greeting = GreetingMode
    Keyboard = KeyboardMode

    @property
    def command(self) -> str:
        return self.value.command()

    @property
    def handler(self):
        return self.value