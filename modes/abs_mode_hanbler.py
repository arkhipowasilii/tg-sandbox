from abc import abstractmethod

from telegram import Update
from telegram.ext import MessageHandler

from config import path
from core import Core
from service.db import DatabaseHandler


class AbsModeHandler:
    def __init__(self, dispatcher, core: Core):
        self._core = core
        self.dispatcher = dispatcher
        self.current_handlers = []

        self.db_handler = DatabaseHandler(path)
        self.current_table = "users"

    def connect_handlers(self):
        self.add_message_handlers()

    @classmethod
    @abstractmethod
    def command(cls):
        pass

    @abstractmethod
    def _get_message_handlers(self):
        pass

    def _get_handlers(self):
        return self._get_message_handlers()

    def disconnect_handlers(self):
        for handler in self.current_handlers:
            self.dispatcher.remove_handler(handler)

    @staticmethod
    def send_message(update: Update, context, msg: str, markup=None):
        if markup is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=markup)

    def add_message_handlers(self):
        for filter, callback in self._get_message_handlers():
            handler = MessageHandler(filter, callback)
            self.current_handlers.append(handler)
            self.dispatcher.add_handler(handler)