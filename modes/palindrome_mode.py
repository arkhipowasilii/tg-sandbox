from telegram import Update

from modes.abs_mode_hanbler import AbsModeHandler
from service.messagefilters import MessageFilters


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