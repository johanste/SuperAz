import argparse

class AzCliCommandParser(argparse.ArgumentParser):
    """ArgumentParser implementation specialized for the
    Azure CLI utility.
    """
    def __init__(self, **kwargs):
        super(AzCliCommandParser, self).__init__(**kwargs)
        self.subparsers = {}
        self.parents = kwargs.get('parents', None)

    def load_command_table(self, session, command_table):
        """Load a command table into our parser.
        """
        # If we haven't already added a subparser, we
        # better do it.
        if not self.subparsers:
            self.subparsers = {(): self.add_subparsers()}

        for handler, metadata in command_table.items():
            subparser = self._get_subparser(metadata.name.split())
            command_parser = subparser.add_parser(metadata.name.split()[-1], parents=self.parents)
            session.raise_event('AzCliCommandParser.SubparserCreated',
                                {'parser': command_parser, 'metadata': metadata})
            for arg in metadata.options:
                command_parser.add_argument(*arg.name.split(),
                                            **arg)
            command_parser.set_defaults(func=handler)

    def _get_subparser(self, path):
        """For each part of the path, walk down the tree of
        subparsers, creating new ones if one doesn't already exist.
        """
        for length in range(0, len(path)):
            parent_subparser = self.subparsers.get(tuple(path[0:length]), None)
            if not parent_subparser:
                # No subparser exists for the given subpath - create and register
                # a new subparser.
                # Since we know that we always have a root subparser (we created)
                # one when we started loading the command table, and we walk the
                # path from left to right (i.e. for "cmd subcmd1 subcmd2", we start
                # with ensuring that a subparser for cmd exists, then for subcmd1,
                # subcmd2 and so on), we know we can always back up one step and
                # add a subparser if one doesn't exist
                grandparent_subparser = self.subparsers[tuple(path[0:length - 1])]
                new_parser = grandparent_subparser.add_parser(path[length - 1])
                parent_subparser = new_parser.add_subparsers()
                self.subparsers[tuple(path[0:length])] = parent_subparser
        return parent_subparser

    def error(self, message):
        # TODO: Do something more useful here...
        raise ValueError(message)
