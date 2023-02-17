
def register(data: dict, bank):
    """
    Register a new account

    Parameters:
        data (dict): Data from the request

        bank (BankController): Bank controller

    Returns:
        dict: Response data

    """

    result = {'status': 'error'}

    if (
        'firstName' in data and
        'lastName' in data and
        'passWord' in data and
        'age' in data and
        'cpf' in data and
            'accountName' in data):
        account = bank.createAccount(
            data['firstName'],
            data['lastName'],
            data['age'],
            data['cpf'],
            data['accountName'],
            data['passWord'],
            0,
            1000,
            commit=True,
        )

        if account:
            result = {'status': 'success', 'account': account.toDict()}

    return result
