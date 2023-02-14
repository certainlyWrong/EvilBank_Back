from ..controllers.bank_controller import BankController


def searchAccounts(data, bank: BankController) -> dict:
    name = data['accountName']

    accounts = []

    accountsModels = bank.accountsByStringInName(name)

    for accountModel in accountsModels:
        accounts.append(accountModel.toDict())

    return {'accounts': accounts}
