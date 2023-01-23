
from ..controllers.bank_controller import BankController


def deposit(data, bank: BankController):
    result = False
    account = bank.loggedAccount
    if account:
        result = bank.deposit(account, data['value'])
    return {'status': 'success' if result else 'fail'}
