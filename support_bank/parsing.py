"""
Functions which support the parsing of transactions from raw formats.
"""

from collections import namedtuple
import csv
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
import json
import logging
from xml.etree import ElementTree

from support_bank.bank import Transaction

_CSV_DATE_HEADER = 'Date'
_CSV_FROM_ACCOUNT_HEADER = 'From'
_CSV_TO_ACCOUNT_HEADER = 'To'
_CSV_NARRATIVE_HEADER = 'Narrative'
_CSV_AMOUNT_HEADER = 'Amount'
_CSV_DATE_FORMAT = '%d/%m/%Y'

_JSON_DATE_FIELD = 'date'
_JSON_FROM_ACCOUNT_FIELD = 'fromAccount'
_JSON_TO_ACCOUNT_FIELD = 'toAccount'
_JSON_NARRATIVE_FIELD = 'narrative'
_JSON_AMOUNT_FIELD = 'amount'
_JSON_DATE_FORMAT = '%Y-%m-%d'

_XML_NARRATIVE_ELEMENT = 'Description'
_XML_AMOUNT_ELEMENT = 'Value'
_XML_PARTIES_ELEMENT = 'Parties'
_XML_FROM_ELEMENT = 'From'
_XML_TO_ELEMENT = 'To'
_XML_DATE_ATTRIBUTE = 'Date'

class FailedTransaction(namedtuple('FailedTransaction', 'error index')):
    """
    A transaction that failed parsing or validation.
    """

# Top-level conversion functions

def read_transactions_from_file(file):
    """
    Read and parse the transactions from the given file. Returns a list of successful transactions,
    and a list of failures.
    """

    if (file.endswith('.csv')):
        return _parse_transactions(_get_rows_from_csv_file(file), _convert_csv_row_to_transaction)
    elif file.endswith('.json'):
        return _parse_transactions(_get_objects_from_json_file(file), _convert_json_object_to_transaction)
    elif file.endswith('.xml'):
        return _parse_transactions(_get_elements_from_xml_file(file), _convert_xml_element_to_transaction)
    else:
        raise Exception('Unrecognised file type')

def _parse_transactions(transactions, conversion_func):
    successful_transactions, failed_transactions = [], []
    for (index, transaction) in enumerate(transactions):
        try:
            successful_transactions.append(conversion_func(transaction))
        except Exception as error:
            failed_transactions.append(FailedTransaction(error=error, index=index))
    return successful_transactions, failed_transactions

# CSV parsing helpers

def _get_rows_from_csv_file(file):
    logging.info(f'Reading CSV file: {file}')
    with open(file, 'r') as csvfile:
        return list(csv.DictReader(csvfile))


def _convert_csv_row_to_transaction(csv_row):
    logging.debug(f'Converting CSV record:{csv_row}')
    return Transaction(
        date=_get_date_from_string(csv_row[_CSV_DATE_HEADER], _CSV_DATE_FORMAT),
        from_account=csv_row[_CSV_FROM_ACCOUNT_HEADER],
        to_account=csv_row[_CSV_TO_ACCOUNT_HEADER],
        narrative=csv_row[_CSV_NARRATIVE_HEADER],
        amount=_get_amount_from_string(csv_row[_CSV_AMOUNT_HEADER])
    )

# JSON parsing helpers

def _get_objects_from_json_file(file):
    logging.info(f'Reading JSON file: {file}')
    with open(file, 'r') as jsonfile:
        return json.load(jsonfile)

def _convert_json_object_to_transaction(json_object):
    logging.debug(f'Converting JSON object: {json_object}')
    return Transaction(
        date=_get_date_from_string(json_object[_JSON_DATE_FIELD], _JSON_DATE_FORMAT),
        from_account=json_object[_JSON_FROM_ACCOUNT_FIELD],
        to_account=json_object[_JSON_TO_ACCOUNT_FIELD],
        narrative=json_object[_JSON_NARRATIVE_FIELD],
        amount=_get_amount_from_string(json_object[_JSON_AMOUNT_FIELD])
    )

# XML parsing helpers

def _get_elements_from_xml_file(file):
    logging.info(f'Reading XML file: {file}')
    with open(file, 'r') as xmlfile:
        return ElementTree.parse(xmlfile).getroot()

def _convert_xml_element_to_transaction(xml_element):
    logging.debug(f'Converting XML element: {ElementTree.tostring(xml_element)}')

    parties = xml_element.find(_XML_PARTIES_ELEMENT)

    from_account = parties.find(_XML_FROM_ELEMENT).text
    to_account = parties.find(_XML_TO_ELEMENT).text
    narrative = xml_element.find(_XML_NARRATIVE_ELEMENT).text
    amount = _get_amount_from_string(xml_element.find(_XML_AMOUNT_ELEMENT).text)
    date = _parse_ole_automation_date(xml_element.attrib[_XML_DATE_ATTRIBUTE])

    return Transaction(
        date=date, from_account=from_account, to_account=to_account, narrative=narrative, amount=amount
    )


# Common parsing helpers

def _get_date_from_string(date_string, format):
    return datetime.strptime(date_string, format).date()

def _get_amount_from_string(amount_string):
    try:
        return Decimal(amount_string)
    except InvalidOperation:
        raise Exception(f'Invalid amount: {amount_string}')

def _parse_ole_automation_date(ole_date):
    base_date = date(1899, 12, 30)
    return base_date + timedelta(int(ole_date))
