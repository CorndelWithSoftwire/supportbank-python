"""
The SupportBank application.
"""

import logging
from operator import attrgetter
from sys import exit

from support_bank.bank import Bank
from support_bank.commands import get_parsed_command, ListAllCommand, ListAccountCommand, ExitCommand
from support_bank.parsing import read_transactions_from_csv_file

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

def display_banner():
    print('\nWelcome to SupportBank!')
    print('=========================')

def process_command(bank):
    command = get_parsed_command()
    logging.info(f'Processing command: {command}')
    if isinstance(command, ListAllCommand):
        list_all_accounts(bank)
    elif isinstance(command, ListAccountCommand):
        list_single_account(bank, command.account)
    elif isinstance(command, ExitCommand):
        exit(0)
    else:
        print('Sorry, I didn\'t understand you')

def list_all_accounts(bank):
    print('\nAll accounts:')
    for account in bank.accounts.values():
        balance = account.balance
        print(f'  {account.owner} {"owes" if balance < 0 else "is owed"} £{balance.copy_abs()}')

def list_single_account(bank, account_name):
    try:
        account = bank.accounts[account_name]

        # Get the transactions sorted in date order
        transactions = account.incoming_transactions + account.outgoing_transactions
        transactions.sort(key=attrgetter('date'))

        # Display the transactions
        print(f'\nAccount {account_name}')
        for transaction in transactions:
            print(f'{transaction.date} - {transaction.from_account} paid {transaction.to_account} £{transaction.amount:.2f} for {transaction.narrative}')

    except KeyError:
        print(f'There is no account known in the name of {account_name}')

def main():
    logging.info('Support Bank starting up')
    logging.info('About to begin processing transactions')

    transactions2014 = read_transactions_from_csv_file('transactions/Transactions2014.csv')
    transactions2015 = read_transactions_from_csv_file('transactions/DodgyTransactions2015.csv')
    bank = Bank.from_transactions(transactions2014, transactions2015)

    display_banner()
    while True:
        process_command(bank)