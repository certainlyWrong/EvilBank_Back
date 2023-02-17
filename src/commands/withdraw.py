
def withdraw(data, bank):
    """
    Withdraw money from the bank account

    Parameters:
        data (dict): Data from the request

        bank (BankController): Bank controller

    Returns:
        dict: Response data

    """
    result = False
    account = bank.loggedAccount
    if account:
        result = bank.withdraw(account, data['value'])
    return {'status': 'success' if result else 'failed'}
