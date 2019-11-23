from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
from telegram.ext import Filters

from core import Core

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Bot:
    def __init__(self, token: str, core: Core):
        self._core = core
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_callback))

    @property
    def dispatcher(self):
        return self.updater.dispatcher

    def message_callback(self, update: Update, context):
        result = self._core.find_anagram(update.message.text)

        if result is None:
            msg = "No anagram"
        else:
            msg = f"your word - {result}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    def start_polling(self):
        self.updater.start_polling()


def main(token):
    bot = Bot(token, Core(("one", "two")))
    bot.start_polling()


if __name__ == '__main__':
    main('701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys')
