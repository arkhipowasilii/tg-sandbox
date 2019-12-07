from abc import abstractmethod, abstractproperty, abstractclassmethod
from collections.abc import Callable
from typing import Dict
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler
from core import Core
from messagefilters import MessageFilters
from enum import Enum


# Принцип единичной ответственности


class AbsModeHandler:
    def __init__(self, dispatcher, core: Core):
        self._core = core
        self.dispatcher = dispatcher
        self.current_handlers = []

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
    def send_message(update: Update, context, msg: str):
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    def add_message_handlers(self):
        for filter, callback in self._get_message_handlers():
            handler = MessageHandler(filter, callback)
            self.current_handlers.append(handler)
            self.dispatcher.add_handler(handler)


class AnagramMode(AbsModeHandler):

    @classmethod
    def command(cls):
        return "anagram"

    def _get_message_handlers(self):
        return ((MessageFilters.text, self.message_callback),
                (MessageFilters.add, self.message_add_callback))

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


class PalindromeMode(AbsModeHandler):
    @classmethod
    def command(cls):
        return "palindrome"

    def _get_message_handlers(self):
        return (MessageFilters.text, self.palindrome_message_callback),

    def palindrome_message_callback(self, update: Update, context):
        string = update.message.text
        msg = f"{string} is a palindrome" if self._core.check_palindrome(
            string) else f"{string} is NOT a palindrome"
        self.send_message(update, context, msg)


class Modes(Enum):
    Anagram = AnagramMode
    Palindrome = PalindromeMode

    @property
    def command(self) -> str:
        return self.value.command()

    @property
    def handler(self):
        return self.value


class Bot:
    default_mode = Modes.Palindrome

    def __init__(self, token: str, core: Core, mode: Modes = None):
        self._token = token
        self._core = core
        self._mode = mode or self.default_mode

        self._updater = Updater(token=token, use_context=True)
        self._disp = self._updater.dispatcher

        self._add_command_handlers({"start": self.start_callback,
                                    Modes.Palindrome.command:
                                       lambda upt, ctx: self._switch_to_mode_callback(upt, ctx, Modes.Palindrome),
                                    Modes.Anagram.command:
                                       lambda upt, ctx: self._switch_to_mode_callback(upt, ctx, Modes.Anagram)})
        self._handlers = {}
        self._switch_to_mode(self.default_mode)

    @property
    def dispatcher(self):
        return self._updater.dispatcher

    def _add_command_handlers(self, callbacks: Dict[str, Callable]):
        tuple(self.dispatcher.add_handler(CommandHandler(command, func)) for command, func in callbacks.items())

    def start_callback(self, update: Update, context):
        update.effective_chat.id
        self.send_message(update, context, 'bot started')

    def _switch_to_mode(self, mode):
        if self._mode in self._handlers:
            self._handlers[self._mode].disconnect_handlers()

        self._mode = mode

        if self._mode not in self._handlers:
            self._handlers[self._mode] = self._mode.handler(self._disp, self._core)

        self._handlers[self._mode].connect_handlers()

    def _switch_to_mode_callback(self, update: Update, context, mode):
        self._switch_to_mode(mode)
        self.send_message(update, context, f"{self._mode.name} has been activated!")

    @staticmethod
    def send_message(update: Update, context, msg: str):
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    def start_polling(self):
        self._updater.start_polling()
