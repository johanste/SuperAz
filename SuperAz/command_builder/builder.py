class Command(object):

    def __init__(self, name, func, **kwargs):
        self.name = name
        self.func = func
        self.options = kwargs.pop('options', [])

class Option(dict):
    def __init__(self, name, **kwargs):
        super(Option, self).__init__()
        self.name = name
        self.update(kwargs)

class CommandTable(dict):

    def __init__(self):
        super(CommandTable, self).__init__(self)

    def command(self, name, **kwargs):
        def wrapper(func):
            self[func] = Command(name, func, **kwargs)
            return func
        return wrapper

    def option(self, name, **kwargs):
        def wrapper(func):
            self[func].options.append(Option(name, **kwargs))
            return func
        return wrapper
