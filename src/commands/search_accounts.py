
def searchAccounts(data, bank) -> dict:
    """
    Search accounts by string in name

    Parameters:
        data (dict): Data from the request

        bank (BankController): Bank controller

    Returns:
        dict: Response data

    """
    name = data['accountName']

    accounts = []

    accountsModels = bank.accountsByStringInName(name)

    for accountModel in accountsModels:
        accounts.append(accountModel.toDict())

    return {'accounts': accounts}
