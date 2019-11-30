from abc import abstractmethod
from collections import Callable
from enum import Enum
from typing import Dict

from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler

from core import Core
from messagefilters import MessageFilters


# Принцип единичной ответственности

class AbsModeHandler:
    @abstractmethod
    def connect_handlers(self, dispatcher):
        raise NotImplementedError

    @abstractmethod
    def disconnect_handlers(self, dispatcher):
        raise NotImplementedError


class AnagramMode(AbsModeHandler):
    pass


class PalindromMode(AbsModeHandler):
    pass


class Modes(Enum):
    Anagram = "anagram"
    Palindrome = "palindrome"

    @property
    def command(self):
        return self.value

    @property
    def handler(self):
        if self.Anagram:
            return AnagramMode
        if self.Palindrome:
            return PalindromMode


class Bot:
    def __init__(self, token: str, core: Core, mode: Modes):
        self._core = core
        self._mode = mode
        self._modes = {mode: mode.handler() for mode in Modes}

        self.updater = Updater(token=token, use_context=True)
        if self._mode is Modes.Anagram:
            self.dispatcher.add_handler(MessageHandler(MessageFilters.text, self.message_callback))
            self.dispatcher.add_handler(MessageHandler(MessageFilters.add, self.message_add_callback))

        self.add_command_handlers({"start": self.start_callback,
                                   Modes.Anagram.command: self.start_callback,
                                   Modes.Palindrome.command: self.palindrome_callback})

    @property
    def dispatcher(self):
        return self.updater.dispatcher

    def add_command_handlers(self, callbacks: Dict[str, Callable]):
        tuple(self.dispatcher.add_handler(CommandHandler(command, func)) for command, func in callbacks.items())

    def palindrome_callback(self, update, context):
        self._mode = Modes.Palindrome

    def start_callback(self, update: Update, context):
        self.send_message(update, context, 'bot started')

    def message_callback(self, update: Update, context):
        result = self._core.find_anagram(update.message.text)

        if result is None:
            msg = "No anagram"
        else:
            msg = f"your word - {result}"

        self.send_message(update, context, msg)

    def message_add_callback(self, update: Update, context):
        words = update.message.text[4:]
        words = words.split()
        self._core.update_dict(words)

        self.send_message(update, context, f"words: {words} successfully added")

    def start_polling(self):
        self.updater.start_polling()

    @staticmethod
    def send_message(update: Update, context, msg: str):
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
