from command_builder.builder import CommandTable

def load_command_table():
    return command_table

command_table = CommandTable()

@command_table.option('possie', metavar='da possie')
@command_table.option('--vm-name -name', dest='vm_name', nargs='+')
@command_table.option('--tags', dest='tags', nargs='+')
@command_table.option('--resourcegroup', dest='resource_group', help='This is the help for resource group')
@command_table.command('vm list-all')
def vm_list_command(self):
    print('vm list command:')
    print(self)
