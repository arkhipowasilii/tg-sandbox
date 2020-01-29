from collections.abc import Callable
from typing import Dict
from telegram import Update, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from telegram.ext import Updater, CommandHandler
from abs_mode_hanbler import AbsModeHandler
from config import path
from core import Core

# Принцип единичной ответственности
from modes import Modes

assert path.exists()

# ToDo Keyboard Builder ; KeyboardMode ; Made save button click history in base: t_id, timestamp, button


class KeyboardMode(AbsModeHandler):
    @classmethod
    def command(cls):
       return "kb"

    def _get_message_handlers(self):
        pass

    def wrapper(self, func) -> str:
        pass

    def dewrapper(self, func: str) -> Callable:
        pass

    def greeting_callback(self, update, context):
        keyboard = [[Button("Option 1", callback_data=self.wrapper(self.option_1_callback)),
                     Button("Option 2", callback_data='2')],
                    [Button("Option 3", callback_data='3')]]

        reply_markup = Markup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def button_callback(self, update, context):
        self.dewrapper(update.callback_query)(update, context)

    def option_1_callback(self, update, context):
        pass


class Bot:
    default_mode = Modes.Greeting

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
                                        lambda upt, ctx: self._switch_to_mode_callback(upt, ctx, Modes.Greeting)})
        self._handlers = {}
        self._switch_to_mode(self.default_mode)

    @property
    def dispatcher(self):
        return self._updater.dispatcher

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
