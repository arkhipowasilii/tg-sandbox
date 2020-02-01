from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup, KeyboardButton
from typing import Callable, Any, Tuple, List, Optional
from math import ceil


class KeyboardBuilder:
    def __init__(self):
        self._buttons: List[List[Button]] = [[]]
        self._inline_count = None

    def elements_in_line(self, count: int) -> [[Button]]:
        self._inline_count = count
        return self

    @classmethod
    def _serialize(csl, callback: Callable, args: Tuple[int]) -> str:
        return f"{callback.__name__}|{','.join(tuple(map(str, args)))}"

    @staticmethod
    def deserialize(owner, raw: str) -> (Optional[Callable], Tuple):
        raw = raw.split("|")
        assert len(raw) in (1, 2)
        func, args = raw[0], tuple()

        if len(raw) > 1:
            args = raw[1]
            args = args.split(",")

        return getattr(owner, func), args

    def button(self, data: Any, callback: Callable, args: Tuple[int]):
        if self._inline_count is None:
            self._inline_count = 1

        current_button = Button(text=data, callback_data=self._serialize(callback, args),)

        line = self._buttons[-1]
        if len(line) >= self._inline_count:
            self._buttons.append([current_button])
        else:
            self._buttons[-1].append(current_button)
        return self

    def get(self) -> Markup:
        #buttons = [self._buttons[self._inline_count * line: self._inline_count * (line + 1)]
        #          for line in range(ceil(len(self._buttons) // self._inline_count))]
        return Markup(self._buttons)
