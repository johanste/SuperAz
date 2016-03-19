from command_builder.builder import CommandTable

command_table = CommandTable()

@command_table.option('--account')
@command_table.command('logout')
def my_little_command():
    pass

@command_table.option('--user -u', dest='user_name')
@command_table.command('login')
def other_command(self):
    print('other command:')
    print(self)

