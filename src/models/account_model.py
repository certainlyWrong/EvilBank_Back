import json
from uuid import uuid4

from ..entities.account_entity import AccountEntity


class AccountModel:
    """
    Account model

    ...

    Parameters
    ----------
    accountId : str
        Account id
    personId : str
        Person id
    accountName : str
        Account name
    accountHash : str
        Account hash
    balance : float
        Account balance
    limit : float
        Account limit

    Methods
    -------
    factoryAccountModel(clientId: str, accountName: str, accountHash: str, balance: float, limit: float) -> AccountModel
        Factory method to create an account model
    empty() -> AccountModel
        Create an empty account model
    fromEntity(accountEntity: AccountEntity) -> AccountModel
        Create an account model from an account entity
    toDict() -> dict
        Create a dict from the account model
    toEntity() -> AccountEntity
        Create an account entity from the account model
    """

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
        """
        Factory method to create an account model

        Parameters
        ----------
        clientId : str
            Client id
        accountName : str
            Account name
        accountHash : str
            Account hash
        balance : float
            Account balance
        limit : float
            Account limit

        Returns
        -------
        AccountModel
            Account model
        """
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
        """
        Create an empty account model

        Returns
        -------
        AccountModel
            Account model

        """
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
        """
        Create an account model from an account entity

        Parameters
        ----------
        accountEntity : AccountEntity
            Account entity

        Returns
        -------
        AccountModel
            Account model

        """

        return cls(
            accountEntity.account_id,  # type: ignore
            accountEntity.person_id,  # type: ignore
            accountEntity.account_name,  # type: ignore
            accountEntity.account_hash,  # type: ignore
            accountEntity.account_balance,  # type: ignore
            accountEntity.account_limit,  # type: ignore
        )

    def toEntity(self) -> AccountEntity:
        """
        Create an account entity from the account model

        Returns
        -------
        AccountEntity
            Account entity
        """
        return AccountEntity(
            account_id=self.accountId,
            person_id=self.personId,
            account_name=self.accountName,
            account_hash=self.hashAccount,
            account_balance=self.balance,
            account_limit=self.limit,
        )

    def toDict(self) -> dict:
        """
        Create a dict from the account model

        Returns
        -------
        dict
            Account model as dict
        """
        return {
            'accountId': self.accountId,
            'personId': self.personId,
            'accountName': self.accountName,
            'hashAccount': self.hashAccount,
            'balance': self.balance,
            'limit': self.limit,
        }

    def toJson(self) -> str:
        """
        Create a json from the account model

        Returns
        -------
        str
            Account model as json
        """
        return json.dumps(self.toDict())

    def fromDict(self, data: dict):
        """
        Create an account model from a dict

        Parameters
        ----------
        data : dict
            Data to create the account model

        Returns
        -------
        AccountModel
            Account model
        """
        return AccountModel(
            data['accountId'],
            data['personId'],
            data['accountName'],
            data['hashAccount'],
            data['balance'],
            data['limit'],
        )

    def fromJson(self, data: str):
        """
        Create an account model from a json

        Parameters
        ----------
        data : str
            Data to create the account model

        Returns
        -------
        AccountModel
            Account model
        """
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
