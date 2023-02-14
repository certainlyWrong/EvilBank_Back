from ..controllers.bank_controller import BankController


def login(data: dict, bank: BankController) -> dict:
    """
    Login to the bank

    Parameters:
        data (dict): Data from the request
        bank (BankController): Bank controller

    Returns:
        dict: Response data

    """
    result = bank.login(data['accountName'], data['passWord'])
    return {'status': 'success'} if result else {'status': 'failed'}
