from ..controllers.bank_controller import BankController


def transfer(data, bank: BankController):
    result = False

    accountLogged = bank.loggedAccount
    accountName = data['accountName']
    value = data['value']
    if accountLogged:
        result = bank.transferByAccountName(accountLogged, accountName, value)

    return {'status': 'success' if result else 'fail'}
