from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
from telegram.ext import Filters
from my_filters import My_filters
from core import Core

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Bot:
    def __init__(self, token: str, core: Core):
        self._core = core
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher.add_handler(MessageHandler(My_filters.text, self.message_callback))
        self.dispatcher.add_handler(MessageHandler(My_filters.add, self.message_add_word))
        self.dispatcher.add_handler(CommandHandler("start", self.start_callback))

    @property
    def dispatcher(self):
        return self.updater.dispatcher

    def start_callback(self, update: Update, context):
        self.send_message(update, context, 'bot started')

    def message_callback(self, update: Update, context):
        result = self._core.find_anagram(update.message.text)

        if result is None:
            msg = "No anagram"
        else:
            msg = f"your word - {result}"

        self.send_message(update, context, msg)

    def message_add_word(self, update: Update, context):
        words = update.message.text[3:]
        words = words.split()
        self._core.update_dict(words)

        self.send_message(update, context, f"words: {words} successfully added")

    def start_polling(self):
        self.updater.start_polling()

    @staticmethod
    def send_message(update: Update, context, msg: str):
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def main(token):
    bot = Bot(token, Core(("one", "two")))
    bot.start_polling()


if __name__ == '__main__':
    main('701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys')
