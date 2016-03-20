from .parser import AzCliCommandParser
from .builtin_commands import load_command_table as builtin_command_table
import commands.vm
import json
import argcomplete
import logging
import _event_dispatcher

class Session(_event_dispatcher.EventDispatcher):
    
    def __init__(self):
        super(Session, self).__init__()
        self.log = logging.getLogger('az')
        
    def command_loader(self, argv):
        pass

class Application(object):

    def __init__(self, session=None):
        self.session = session or Session()
        self.session.register('GlobalParser.Created', self._register_builtin_arguments)
        
    def execute(self, argv):   
        global_parser = AzCliCommandParser(add_help=False)
        self.session.raise_event('GlobalParser.Created', global_parser)
        
        parser = AzCliCommandParser(parents = [global_parser])
        self.session.raise_event('CommandParser.Created', parser)
        
        parser.load_command_table(self.session, builtin_command_table())
        parser.load_command_table(self.session, commands.vm.load_command_table())

        self.session.raise_event('CommandParser.Loaded', parser)
        argcomplete.autocomplete(parser)
        try:
            args = parser.parse_args(argv)
            args.func(args)
        except Exception as e:
            print(e)
            
    def _register_builtin_arguments(self, name, parser):  
        parser.add_argument('--subscription', dest='subscription_id')
        parser.add_argument('--query', dest='_jmespath_query', metavar='QUERY STRING')
        parser.add_argument('--output', dest='_output_format', choices=['table', 'json'], action=OutputFormatAction(self.session))
