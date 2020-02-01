from datetime import datetime
from typing import Callable

from core import Core
from modes.abs_mode_hanbler import AbsModeHandler


# ToDo Keyboard Builder ; KeyboardMode ; Made save button click history in base: t_id, timestamp, button
from service.db import HistoryDatabaseHandler
from service.keyboard_builder import KeyboardBuilder


class KeyboardMode(AbsModeHandler):
    def __init__(self, db: HistoryDatabaseHandler, dispatcher, core: Core):
        super().__init__(dispatcher, core)
        self._db = db

    @classmethod
    def command(cls):
        return "kb"

    def _get_message_handlers(self):
        pass

    def wrapper(self, func) -> str:
        return func.__name__

    def dewrapper(self, func: str) -> Callable:
        pass

    def greeting_callback(self, update, context):
        kb = KeyboardBuilder().elements_in_line(1)
        kb.button("1", self.callback, arg=(1,))\
            .button("2", self.callback, arg=(2,))\
            .button("3", self.callback, arg=(3,))\
            .button("show", self.show_callback)\

        update.message.reply_text('Please choose:', reply_markup=kb.get())

    def button_callback(self, update, context):
        func, args = KeyboardBuilder.deserialize(self, update.callback_query.data)
        if func is not None:
            func(update, context, *args)
        else:
            # ToDo Add logging for wrong callback
            pass

    def callback(self, update, context, num: int):
        self._db.insert(update.telegram_id, datetime.now(), num)

    def show_callback(self, update, context):
        # ToDo Show history from db with inline keyboard
        self._db.get_history(update.telegram_id)
