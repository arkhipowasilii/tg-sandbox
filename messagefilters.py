from telegram.ext import BaseFilter


# CamelCase
# snake_case
# Shit_case
exception_strings = ['/', '$']


class MessageFilters(object):

    def decorator(self, func):
        def wrapper(self, message):
            for string in exception_strings:
                if message.text.startswith(string):
                    return False
            else:
                func(self, message)
        return wrapper

    class _Text(BaseFilter):
        name = 'MessageFilters.text'

        def filter(self, message):
            return bool(message.text and not message.text.startswith('/'))

    text = decorator(_Text.filter)

    class _Add(BaseFilter):
        name = 'MessageFilters.add'

        def filter(self, message):
            return bool(message.text and message.text.startswith('$add'))

    add = _Add()

    class _YesNo(BaseFilter):
        name = 'MessageFilters.YesNo'

        def filter(self, message):
            return bool(message.text and (message.text.startswith('yes') or message.text.startswith("no")))

    yesno = _YesNo()

    class _ExceptYesNO(BaseFilter):
        name = 'MessageFilters.ExceptYesNo'

        def filter(self, message):
            return bool(message.text and not message.text.startswith('yes') and not message.text.startswith("no"))

    except_yesno = _ExceptYesNO()

