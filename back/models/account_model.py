import json
from uuid import uuid4

from ..entities.account_entity import AccountEntity


class AccountModel:

    def __init__(
        self,
        accountId: str,
        personId: str,
        accountName: str,
        accountHash: str,
        balance: float,
        limit: float,
    ):
        self.__accountId = accountId
        self.__personId = personId
        self.__accountName = accountName
        self.__hashAccount = accountHash
        self.__balance = balance
        self.__limit = limit

    @classmethod
    def factoryAccountModel(
        cls,
        clientId: str,
        accountName: str,
        accountHash: str,
        balance: float,
        limit: float,
    ):
        result = None

        if accountName.isalpha():
            if not accountHash.isalpha():
                if balance >= 0:
                    if limit >= balance:
                        result = cls(
                            str(uuid4()),
                            clientId,
                            accountName,
                            accountHash,
                            balance,
                            limit,
                        )

        return result

    @classmethod
    def empty(cls) -> 'AccountModel':
        return cls(
            str(uuid4()),
            str(uuid4()),
            '',
            '',
            0.0,
            1000,
        )

    @classmethod
    def fromEntity(cls, accountEntity: AccountEntity) -> 'AccountModel':

        return cls(
            accountEntity.account_id,  # type: ignore
            accountEntity.person_id,  # type: ignore
            accountEntity.account_name,  # type: ignore
            accountEntity.account_hash,  # type: ignore
            accountEntity.account_balance,  # type: ignore
            accountEntity.account_limit,  # type: ignore
        )

    def toEntity(self) -> AccountEntity:
        return AccountEntity(
            account_id=self.accountId,
            person_id=self.personId,
            account_name=self.accountName,
            account_hash=self.hashAccount,
            account_balance=self.balance,
            account_limit=self.limit,
        )

    def toDict(self) -> dict:
        return {
            'accountId': self.accountId,
            'personId': self.personId,
            'accountName': self.accountName,
            'hashAccount': self.hashAccount,
            'balance': self.balance,
            'limit': self.limit,
        }

    def toJson(self) -> str:
        return json.dumps(self.toDict())

    def fromDict(self, data: dict):
        return AccountModel(
            data['accountId'],
            data['personId'],
            data['accountName'],
            data['hashAccount'],
            data['balance'],
            data['limit'],
        )

    def fromJson(self, data: str):
        return self.fromDict(json.loads(data))

    @property
    def accountId(self) -> str:
        return self.__accountId

    @property
    def personId(self) -> str:
        return self.__personId

    @personId.setter
    def personId(self, personId: str) -> None:
        self.__personId = personId

    @property
    def accountName(self) -> str:
        return self.__accountName

    @accountName.setter
    def accountName(self, accountName: str) -> None:
        self.__accountName = accountName

    @property
    def hashAccount(self) -> str:
        return self.__hashAccount

    @hashAccount.setter
    def hashAccount(self, hashAccount: str) -> None:
        self.__hashAccount = hashAccount

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, balance: float) -> None:
        self.__balance = balance

    @property
    def limit(self) -> float:
        return self.__limit

    @limit.setter
    def limit(self, limit: float) -> None:
        self.__limit = limit
