from telegram import Update
from keyboard_builder import KeyboardBuilder
from abs_mode_hanbler import AbsModeHandler
from messagefilters import MessageFilters


class GreetingMode(AbsModeHandler):
    @classmethod
    def command(cls):
        return "greeting"

    def _get_message_handlers(self):
        return ((MessageFilters.except_yesno, self.message_callback),
                (MessageFilters.yesno, self.adding_name_callback))

    def message_callback(self, update: Update, context):
        tg_user_data = update.effective_user
        user_id = tg_user_data["id"]

        user_name = self.db_handler.get_username(self.current_table, user_id)

        if user_name is None:
            user_name = tg_user_data["first_name"]
            self.send_message(update, context, f"Hi! Are you {user_name}?")
        else:
            self.greeting(update, context, user_name)

    def adding_name_callback(self, update: Update, context):
        user_data = update.effective_user

        user_id = user_data["id"]
        user_name = user_data["first_name"]
        message = update.effective_message["text"]

        if message.startswith("no "):
            user_name = message[3::]
        elif not message == "yes":
            self.send_message(update, context, f"Are you {user_name}? (Enter 'yes' or 'no ...')")
            return

        self.db_handler.insert(self.current_table, user_id, user_name)
        self.greeting(update, context, user_name)

    def greeting(self, update: Update, context, name: str):
        kb = KeyboardBuilder()
        kb.button("---", "1")
        msg = f"Hi, {name}! Enter '/palindrome' to find palindrome." \
            f" Enter '/anagram' to find anagram, use '$add ... to add some words"
        self.send_message(update, context, msg, reply_markup=kb.get())
