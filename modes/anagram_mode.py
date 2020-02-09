from telegram import Update

from modes.abs_mode_handler import AbsModeHandler
from service.messagefilters import MessageFilters


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
