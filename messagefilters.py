from telegram.ext import BaseFilter


# CamelCase
# snake_case
# Shit_case

class MessageFilters(object):
    class _Text(BaseFilter):
        name = 'MessageFilters.text'

        def filter(self, message):
            return bool(message.text and not message.text.startswith('/') and not message.text.startswith('$add'))

    text = _Text()

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
