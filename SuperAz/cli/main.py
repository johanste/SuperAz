import argparse
import builtin_commands
import commands.vm
import json
import argcomplete

class AzCliCommandParser(argparse.ArgumentParser):

    def __init__(self, **kwargs):
        super(AzCliCommandParser, self).__init__(**kwargs)
        self.subparsers = {}

    def load_command_table(self, command_table):
        if not self.subparsers:
            self.subparsers = {(): self.add_subparsers()}

        for handler, metadata in command_table.items():
            subparser = self._get_subparser(metadata.name.split())
            command_parser = subparser.add_parser(metadata.name.split()[-1])
            for arg in metadata.options:
                command_parser.add_argument(*arg.name.split(),
                                            type=arg.type or str,
                                            dest=arg.dest or arg.name.split()[0],
                                            action=arg.action,
                                            default=arg.default(arg) if callable(arg.default) else arg.default
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

def run():
    parser = AzCliCommandParser()
    parser.load_command_table(builtin_commands.command_table)
    parser.load_command_table(commands.vm.command_table)
    argcomplete.autocomplete(parser)
    try:
        args = parser.parse_args('vm login --fuansdkl'.split())
        args.func(args)
    except Exception as e:
        print(e)
