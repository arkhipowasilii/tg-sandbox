from telegram.ext import BaseFilter


# CamelCase
# snake_case
# Shit_case

class MessageFilters(object):
    class _Text(BaseFilter):
        name = 'MyFilters.text'

        def filter(self, message):
            return bool(message.text and not message.text.startswith('/') and not message.text.startswith('$add'))

    text = _Text()

    class _Add(BaseFilter):
        name = 'MyFilters.add'

        def filter(self, message):
            return bool(message.text and message.text.startswith('$add'))

    add = _Add()

    class _YesNo(BaseFilter):
        name = 'MeFilters.YesNo'

        def filter(self, message):
            return bool(message.text and message.text == 'yes' or message.text == "no")

    yesno = _YesNo
