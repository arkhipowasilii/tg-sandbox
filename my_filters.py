from telegram.ext import BaseFilter


class My_filters(object):
    class _Text(BaseFilter):
        name = 'My_filters.text'

        def filter(self, message):
            return bool(message.text and not message.text.startswith('/') and not message.text.startswith('add'))

    text = _Text()

    class _Add(BaseFilter):
        name = 'My_filters.add'

        def filter(self, message):
            return bool(message.text and message.text.startswith('add'))

    add = _Add()
