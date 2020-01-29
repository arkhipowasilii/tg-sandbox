from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup, KeyboardButton
from typing import Callable, Any, Tuple, List, Optional
from math import ceil


class KeyboardBuilder:
    def __init__(self):
        self._buttons = [List[List[Button]]] = [[]]
        self._inline_count = None

    def elements_in_line(self, count: int) -> [[Button]]:
        self._inline_count = count
        return self

    def button(self, data: Any, callback):
        current_button = Button(text=data, callback_data=callback,)
        for line in self._buttons:
            if len(line) >= self._inline_count:
                self._buttons.append([])
            self._buttons[-1].append(current_button)

        return self

    def get(self) -> Markup:
        buttons = [self._buttons[self._inline_count * line: self._inline_count * (line + 1)]
                   for line in range(ceil(len(self._buttons) // self._inline_count))]

        return Markup(buttons)
