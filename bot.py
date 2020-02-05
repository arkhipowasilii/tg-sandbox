from collections.abc import Callable
from typing import Dict
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from config import path_tg
from core import Core

# Принцип единичной ответственности
from modes.modes import Modes

assert path_tg.exists()


class Bot:
    default_mode = Modes.Keyboard

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
                                        lambda upt, ctx: self._switch_to_mode_callback(upt, ctx, Modes.Anagram),
                                    Modes.Greeting.command:
                                        lambda upt, ctx: self._switch_to_mode_callback(upt, ctx, Modes.Greeting),
                                    Modes.Keyboard.command:
                                        lambda upt, ctx: self._switch_to_mode_callback(upt, ctx, Modes.Keyboard)})

        self._handlers = {}
        self._switch_to_mode(self.default_mode)

    @property
    def dispatcher(self):
        return self._updater.dispatcher

    def query_callback(self, update: Update, context):
        callback_data = update.callback_query.data
        for mode in Modes:
            if callback_data == str(mode.name):
                self._switch_to_mode_callback(update, context, mode)
    def _add_command_handlers(self, callbacks: Dict[str, Callable]):
        tuple(self.dispatcher.add_handler(CommandHandler(command, func)) for command, func in callbacks.items())

    def start_callback(self, update: Update, context):
        self.send_message(update, context, f"bot started{update.effective_message['text']}")

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
