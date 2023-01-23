from ..controllers.bank_controller import BankController


def loggedAccountInfos(data: dict, bank: BankController):

    result = {'status': 'failed'}

    if (bank.loggedAccount is not None and
        bank.loggedPerson is not None and
            bank.loggedAccountLogs is not None):

        logs = bank.loggedAccountLogs

        result = {
            'status': 'success',
            'account': bank.loggedAccount.toDict(),
            'person': bank.loggedPerson.toDict(),
            'logs': [log.toDict() for log in logs],
        }

    return result
