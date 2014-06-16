
class FormatterUnavailable(Exception):
    pass


class FormatterBase(object):
    def filter(self, text, **kwargs):
        return text
    
    def process(self, text, **kwargs):
        return text


def get_formatter(name):
    from importlib import import_module
    try:
        mod = import_module(self.formatter)
        formatter = mod.Formatter
        return formatter
    except:
        raise FormatterUnavailable(self.formatter)

