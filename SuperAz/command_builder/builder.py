from collections import defaultdict

class Command(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.func = kwargs.pop('func', None)
        self.options = kwargs.pop('options', [])

class Option(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.help = kwargs.pop('help', None)
        self.type = kwargs.pop('type', None)
        self.action= kwargs.pop('action', None)
        self.dest = kwargs.pop('dest', None)
        self.default = kwargs.pop('default', None)

class CommandTable(dict):

    def __init__(self):
        super(CommandTable, self).__init__(self)

    def command(self, name, **kwargs):
        def wrapper(func):
            self[func] = Command(name=name, **kwargs)
            return func
        return wrapper

    def option(self, name, **kwargs):
        def wrapper(func):
            self[func].options.append(Option(name, **kwargs))
            return func
        return wrapper
