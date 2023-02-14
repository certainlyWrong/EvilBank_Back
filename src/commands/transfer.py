from ..controllers.bank_controller import BankController


def transfer(data, bank: BankController):
    """
    Transfer money to another account

    Parameters:
        data (dict): Data from the request
        bank (BankController): Bank controller

    Returns:
        dict: Response data

    """
    result = False

    accountLogged = bank.loggedAccount
    accountName = data['accountName']
    value = data['value']
    if accountLogged:
        result = bank.transferByAccountName(accountLogged, accountName, value)

    return {'status': 'success' if result else 'failed'}
