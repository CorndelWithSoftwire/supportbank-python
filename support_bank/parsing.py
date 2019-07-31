"""
Functions which support the parsing of transactions from raw formats.
"""

import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
import logging

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

    logging.info(f'Loading CSV transactions from {file}')
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(filter(None.__ne__, map(_convert_csv_row_to_transaction, reader)))

def _convert_csv_row_to_transaction(csv_row):
    logging.debug(f'Converting CSV record:{csv_row}')

    try:
        date = _get_date_from_csv_string(csv_row[_CSV_DATE_HEADER])
        amount = _get_amount_from_csv_string(csv_row[_CSV_AMOUNT_HEADER])
        
        return Transaction(
            date=date,
            from_account=csv_row[_CSV_FROM_ACCOUNT_HEADER],
            to_account=csv_row[_CSV_TO_ACCOUNT_HEADER],
            narrative=csv_row[_CSV_NARRATIVE_HEADER],
            amount=amount
        )
    except Exception as error:
        logging.error(f'Skipping transaction due to the following error: {error}')
        return None

def _get_date_from_csv_string(csv_date_string):
    return datetime.strptime(csv_date_string, '%d/%m/%Y').date()

def _get_amount_from_csv_string(csv_amount_string):
    try:
        return Decimal(csv_amount_string)
    except InvalidOperation:
        raise Exception(f'Invalid amount: {csv_amount_string}')