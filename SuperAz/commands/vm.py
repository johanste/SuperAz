from command_builder.builder import CommandTable

def load_command_table():
    return command_table

command_table = CommandTable()

@command_table.option('--vm-name -name', dest='vm_name')
@command_table.command('vm list-all')
def vm_list_command(self):
    print('vm list command:')
    print(self)

