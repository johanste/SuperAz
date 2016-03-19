import argparse

class AzCliCommandParser(argparse.ArgumentParser):

    def __init__(self, **kwargs):
        super(AzCliCommandParser, self).__init__(**kwargs)
        self.subparsers = {}
        self.parents = kwargs.get('parents', None) 
        
    def load_command_table(self, command_table):
        if not self.subparsers:
            self.subparsers = {(): self.add_subparsers()}

        for handler, metadata in command_table.items():
            subparser = self._get_subparser(metadata.name.split())
            command_parser = subparser.add_parser(metadata.name.split()[-1], parents=self.parents)
            for arg in metadata.options:
                command_parser.add_argument(*arg.name.split(),
                                            **arg
                                            )
            command_parser.set_defaults(func=handler)

    def _get_subparser(self, path):
        for length in range(0, len(path)):
            parent_subparser = self.subparsers.get(tuple(path[0:length]), None)
            if not parent_subparser:
                parent_subparser = self.subparsers[tuple(path[0:length - 1])]
                new_parser = parent_subparser.add_parser(path[length - 1])
                parent_subparser  = new_parser.add_subparsers()
                self.subparsers[tuple(path[0:length])] = parent_subparser 
        return parent_subparser

    def error(self, message):
        raise ValueError(message)

