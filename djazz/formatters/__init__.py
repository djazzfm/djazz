
class FormatterUnavailable(Exception):
    pass


class FormatterBase(object):
    def filter(self, text, **kwargs):
        return text
    
    def process(self, text, **kwargs):
        return text
    
    def __str__(self):
        return "%s.%s" % (self.__module__, self.__class__.__name__)


def get_formatter(path):
    from importlib import import_module
    try:
        splitted = path.split('.')
        module_path = ".".join(splitted[:-1])
        formatter_name = splitted[-1]

        mod = import_module(module_path)
        formatter = getattr(mod, formatter_name)
        return formatter
    except:
        raise FormatterUnavailable(path)
