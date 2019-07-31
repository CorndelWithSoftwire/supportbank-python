"""
Functions and classes to do with prompting for and parsing user commands.
"""

from collections import namedtuple

class ListAllCommand(namedtuple('ListAllCommand', '')):
    """
    A representation of the command to list all accounts.
    """


class ListAccountCommand(namedtuple('ListAccountCommand', 'account')):
    """
    A representation of the command to list a single account's transactions.
    """


def get_parsed_command():
    raw_command = _prompt_for_command()
    if raw_command.lower() == 'list all':
        return ListAllCommand()
    elif raw_command.lower().startswith('list '):
        return ListAccountCommand(account=raw_command[5:])
    else:
        return None

def _prompt_for_command():
    print('\nAvailable commands:')
    print('  - List All')
    print('  - List <Account>')
    return input('\nPlease enter your command: ')