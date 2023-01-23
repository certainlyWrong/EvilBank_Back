from ..controllers.bank_controller import BankController


def login(data: dict, bank: BankController) -> dict:
    result = bank.login(data['accountName'], data['passWord'])
    return {'status': 'success'} if result else {'status': 'fail'}
