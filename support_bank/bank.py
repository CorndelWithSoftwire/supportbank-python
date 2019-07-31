"""
Classes relating to a bank and the individual accounts within it.
"""

from collections import namedtuple
from operator import attrgetter

class Transaction(namedtuple('Transaction', 'date from_account to_account narrative amount')):
    """
    A single transaction between two accounts.
    """


class Account:
    """
    A single account. Each account is owned by one person, and there should be 
    only one account for any given person.
    """

    def __init__(self, owner):
        self.owner = owner
        self.incoming_transactions = []
        self.outgoing_transactions = []

    def add_incoming_transaction(self, transaction):
        self.incoming_transactions.append(transaction)

    def add_outgoing_transaction(self, transaction):
        self.outgoing_transactions.append(transaction)

    @property
    def balance(self):
        credits = sum(map(attrgetter('amount'), self.incoming_transactions))
        debits = sum(map(attrgetter('amount'), self.outgoing_transactions))
        return credits - debits


class Bank:
    """
    A bank consists of a collection of accounts, and allows transactions to be
    carried out between the accounts.
    """

    def __init__(self):
        self.accounts = {}

    @staticmethod
    def from_transactions(transactions):
        bank = Bank()
        for transaction in transactions:
            bank.add_transaction(transaction)
        return bank

    def add_transaction(self, transaction):
        self._get_or_create_account(transaction.from_account).add_outgoing_transaction(transaction)
        self._get_or_create_account(transaction.to_account).add_incoming_transaction(transaction)

    def _get_or_create_account(self, owner):
        try:
            return self.accounts[owner]
        except KeyError:
            self.accounts[owner] = Account(owner)
            return self.accounts[owner]

