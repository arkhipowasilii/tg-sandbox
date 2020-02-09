from datetime import datetime
from typing import Callable, List
from telegram import Update
from telegram.ext import CallbackQueryHandler
import logging

from core import Core
from modes.abs_mode_handler import AbsModeHandler
from config import path_history
from service.messagefilters import MessageFilters

# ToDo Keyboard Builder ; KeyboardMode ; Made save button click history in base: t_id, timestamp, button
from service.db import HistoryDatabaseHandler
from service.keyboard_builder import KeyboardBuilder


class KeyboardMode(AbsModeHandler):
    def __init__(self, dispatcher, core: Core):
        super().__init__(dispatcher, core)
        self._db = HistoryDatabaseHandler(path_history)

    def connect_handlers(self):
        self.add_query_handlers()
        self.add_message_handlers()

    def _get_message_handlers(self):
        return ((MessageFilters.text, self.greeting_callback),)

    @classmethod
    def command(cls):
        return "kb"

    def wrapper(self, func) -> str:
        return func.__name__

    def dewrapper(self, func: str) -> Callable:
        pass

    def greeting_callback(self, update, context):
        kb = KeyboardBuilder().elements_in_line(1)
        kb.button("1", self.callback, args=(1, 3, 4, 9))\
            .button("2", self.callback, args=(2,))\
            .button("3", self.callback, args=(3,))\
            .button("show", self.show_callback)\
            .button("delete history", self.delete_history_callback)\

        update.message.reply_text('Please choose:', reply_markup=kb.get())

    def button_callback(self, update: Update, context):
        func, args = KeyboardBuilder.deserialize(self, update.callback_query.data)
        if func is not None:
            func(update, context, args)
        else:
            logging.basicConfig(format=f"RAW DATA={update.callback_query.data} | DS DATA={func, args}")
            # ToDo Add logging for wrong callback

    def callback(self, update: Update, context, nums: List[int]):
        self.edit_message(update, context, f"Last chosen\n {nums} Please choose: ")
        self._db.insert(update.effective_user.id, datetime.now(), nums)

    def show_callback(self, update: Update, context, *args):
        # ToDo Show history from db with inline keyboard
        raw = self._db.get_history(update.effective_user.id)
        self.send_message(update, context, '\n'.join(f"b:{bt}, {dt.minute}:{dt.second}" for dt, bt in raw))

    def delete_history_callback(self, update: Update, context, *args):
        self._db.delete_history(update.effective_user.id)
        self.send_message(update, context, "Your history of clicks has been deleted")

    def add_query_handlers(self):
        handler = CallbackQueryHandler(self.button_callback)
        self.current_handlers.append(handler)
        self.dispatcher.add_handler(handler)
