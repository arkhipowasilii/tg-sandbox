import logging

from bot import Bot
from core import Core

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def main(token):
    bot = Bot(token, Core(("one", "two")))
    bot.start_polling()


if __name__ == '__main__':
    main('701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys')
