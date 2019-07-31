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


class ImportFileCommand(namedtuple('ImportFileCommand', 'file')):
    """
    A representation of the command to import a file of transactions.
    """


class ExitCommand(namedtuple('ExitCommand', '')):
    """
    A representation of the command to exit the program.
    """


def get_parsed_command():
    """
    Prompt the user for a command and parse it.
    """
    
    raw_command = _prompt_for_command()
    if raw_command.lower() == 'list all':
        return ListAllCommand()
    elif raw_command.lower().startswith('list '):
        return ListAccountCommand(account=raw_command[5:])
    elif raw_command.lower().startswith('import file '):
        return ImportFileCommand(file=raw_command[12:])
    elif raw_command.lower() == 'exit':
        return ExitCommand()
    else:
        return None

def _prompt_for_command():
    print('\nAvailable commands:')
    print('  - List All')
    print('  - List <Account>')
    print('  - Import File <File Path>')
    print('  - Exit')
    return input('\nPlease enter your command: ')