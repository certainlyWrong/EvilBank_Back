from ..controllers.bank_controller import BankController


def withdraw(data, bank: BankController):
    result = False
    account = bank.loggedAccount
    if account:
        result = bank.withdraw(account, data['value'])
    return {'status': 'success' if result else 'failed'}
