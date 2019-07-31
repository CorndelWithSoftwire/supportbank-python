"""
Functions which support the parsing of transactions from raw formats.
"""

import csv
from datetime import datetime
from decimal import Decimal

from support_bank.bank import Transaction

_CSV_DATE_HEADER = 'Date'
_CSV_FROM_ACCOUNT_HEADER = 'From'
_CSV_TO_ACCOUNT_HEADER = 'To'
_CSV_NARRATIVE_HEADER = 'Narrative'
_CSV_AMOUNT_HEADER = 'Amount'

def read_transactions_from_csv_file(file):
    """
    Read the given CSV file and return a list of Transactions that appear in the file
    """

    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(map(_convert_csv_row_to_transaction, reader))

def _convert_csv_row_to_transaction(csv_row):
    return Transaction(
        date=datetime.strptime(csv_row[_CSV_DATE_HEADER], '%d/%m/%Y').date(),
        from_account=csv_row[_CSV_FROM_ACCOUNT_HEADER],
        to_account=csv_row[_CSV_TO_ACCOUNT_HEADER],
        narrative=csv_row[_CSV_NARRATIVE_HEADER],
        amount=Decimal(csv_row[_CSV_AMOUNT_HEADER])
    )
