import hashlib
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from ..models.log_model import LogModel, LogEntity
from ..models.person_model import PersonModel, PersonEntity
from ..models.account_model import AccountModel, AccountEntity
from ..entities import Base


class BankController:

    def __init__(
        self,
        name: str,
        agency: str,
        engine: sa.engine.Engine,
    ):

        self.__name = name
        self.__agency = agency
        self.__engine = engine
        self.__connection = engine.connect()
        self.__session = sessionmaker(bind=self.__connection)()
        self.__loggedAccount = None
        self.__personLogged = None

    @classmethod
    def factorybankControllerWithNameAndAgency(cls, name: str, agency: str):

        dataBaseName = name.lower().replace(' ', '')

        engine = sa.create_engine(
            'mysql+mysqlconnector://root:123456@localhost:3306')
        engine.execute(f'CREATE DATABASE IF NOT EXISTS {dataBaseName}')
        engine = sa.create_engine(
            f'mysql+mysqlconnector://root:123456@localhost:3306/{dataBaseName}'
        )

        Base.metadata.create_all(engine)

        return cls(name, agency, engine)

    @classmethod
    def factorybankControllerWithEngine(
        cls,
        name: str,
        agency: str,
        engine: sa.engine.Engine
    ):
        Base.metadata.create_all(engine)

        return cls(name, agency, engine)

    def dispose(self):
        self.__engine.execute('DROP DATABASE IF EXISTS evilbanktest')
        self.__session.close()
        self.__connection.close()
        self.__engine.dispose()

    def createAccount(
        self,
        personFirstName: str,
        personLastName: str,
        age: int,
        cpf: str,
        accountName: str,
        accountPassword: str,
        accountBalance: float,
        accountLimit: float,
        commit: bool = False,
    ):
        result = None

        if (not personFirstName.isnumeric()
                and len(personFirstName + personLastName) > 10
                and len(personFirstName) < 255 and cpf.isnumeric()
                and len(cpf) == 11
                and self.checkAccountNameExists(accountName) is False):

            person = self.createPerson(
                personFirstName,
                personLastName,
                age,
                cpf,
                commit,
            )

            accountHash = hashlib.sha256(
                accountPassword.encode()).hexdigest()

            if person is not None:
                account = AccountModel.factoryAccountModel(
                    person.personId,
                    accountName,
                    accountHash,
                    accountBalance,
                    accountLimit,
                )

                if commit and account is not None:
                    saveResult = self.saveEntity(account.toEntity())

                    if saveResult:
                        result = account
                elif account is not None:
                    result = account

        return result

    def createPerson(self,
                     firstName: str,
                     lastName: str,
                     age: int,
                     cpf: str,
                     commit: bool = False):
        result = None

        if (cpf.isnumeric() and isinstance(age, int)):

            person = PersonModel.factoryPersonModel(
                firstName=firstName,
                lastName=lastName,
                age=age,
                cpf=cpf,
            )

            if commit and person is not None:
                personEntity = person.toEntity()
                saveResult = self.saveEntity(personEntity)
                if saveResult:
                    result = person
            elif person is not None:
                result = person

        return result

    def login(
        self,
        accountName: str,
        accountPassword: str,
    ) -> bool:
        result = False

        accountHash = hashlib.sha256(accountPassword.encode()).hexdigest()

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.account_name == accountName,
                AccountEntity.account_hash == accountHash,
            ).one()

            personResult = self.__session.query(PersonEntity).filter(
                PersonEntity.person_id == accountResult.person_id, ).one()

            self.__loggedAccount = AccountModel.fromEntity(accountResult)
            self.__personLogged = PersonModel.fromEntity(personResult)
            result = True
        except Exception as e:
            print(e)

        return result

    def accountById(self, accountId: str):
        result = None

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.account_id == accountId, ).one()

            result = AccountModel.fromEntity(accountResult)
        except Exception as e:
            print(e)

        return result

    # TODO: testar
    def personByCpf(self, cpf: str):
        result = None

        try:
            personResult = self.__session.query(PersonEntity).filter(
                PersonEntity.person_cpf == cpf, ).one()

            result = PersonModel.fromEntity(personResult)
        except Exception as e:
            print(e)

        return result

    # TODO: testar
    def accountByPersonId(self, personId: int):
        result = None

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.person_id == personId, ).one()

            result = AccountModel.fromEntity(accountResult)
        except Exception as e:
            print(e)

        return result

    # TODO: testar
    def accountByName(self, accountName: str):
        result = None

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.account_name == accountName, ).one()

            result = AccountModel.fromEntity(accountResult)
        except Exception as e:
            print(e)

        return result

    # TODO: Implementar conta que busque um usuário pelo CPF
    def accountByCPF(self, cpf: str) -> AccountModel:
        ...

    def checkAccountNameExists(self, accountName: str):
        result = False

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.account_name == accountName, ).one()

            if accountResult is not None:
                result = True
        except Exception as e:
            print(e)

        return result

    # TODO: testar
    def checkAccountNameExistsByPersonId(self, accountName: str):
        result = False

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.account_name == accountName, ).one()

            if accountResult is not None:
                result = True
        except Exception as e:
            print(e)

        return result

    def withdraw(self, account: AccountModel, value: float) -> bool:
        result = False

        if (account is not None and value > 0 and account.balance >= value):
            account.balance -= value
            result = self.updateEntity(account.toEntity())

            self.addLog(
                account,
                f'{value}',
                'Saque',
            )

        return result

    def deposit(self, account: AccountModel, value: float) -> bool:
        result = False

        if (account is not None and value > 0):
            account.balance += value
            result = self.updateEntity(account.toEntity())

            self.addLog(
                account,
                f'{value}',
                'Deposito',
            )

        return result

    def transfer(
        self,
        accountFrom: AccountModel,
        accountTo: AccountModel,
        value: float,
    ) -> bool:
        result = False

        if (accountFrom is not None and accountTo is not None and value > 0
                and accountFrom.balance >= value):
            accountFrom.balance -= value
            accountTo.balance += value
            result = self.updateEntity(accountFrom.toEntity())
            result = self.updateEntity(accountTo.toEntity())

            self.addLog(
                accountFrom,
                f"{value}",
                f'Transferencia: {accountTo.accountName}',
            )

            self.addLog(
                accountTo,
                f"{value}",
                f'Transferencia: {accountFrom.accountName}',
            )

        return result

    # TODO: testar
    def transferByAccountName(
        self,
        accountFrom: AccountModel,
        accountToName: str,
        value: float,
    ) -> bool:
        result = False

        if (accountFrom is not None and accountToName is not None and value > 0
                and accountFrom.balance >= value):
            accountTo = self.accountByName(accountToName)

            if accountTo is not None:
                result = self.transfer(accountFrom, accountTo, value)

        return result

    # TODO: testar
    def saveEntity(self, entity: Base) -> bool:
        result = False

        try:
            self.__session.add(entity)
            self.__session.commit()
            result = True
        except Exception as e:
            self.__session.rollback()
            print(e)

        return result

    # TODO: testar
    def updateEntity(self, entity: Base) -> bool:
        result = False

        try:
            self.__session.merge(entity)
            self.__session.commit()
            result = True
        except Exception as e:
            self.__session.rollback()
            print(e)

        return result

    # TODO: testar
    def deleteEntity(self, entity: Base) -> bool:
        result = False

        try:
            self.__session.delete(entity)
            self.__session.commit()
            result = True
        except Exception as e:
            self.__session.rollback()
            print(e)

        return result

    @property
    def isLogged(self) -> bool:
        return (self.__loggedAccount is not None
                and self.__personLogged is not None)

    @property
    def loggedAccount(self) -> AccountModel | None:
        return self.__loggedAccount

    @property
    def loggedPerson(self) -> PersonModel | None:
        return self.__personLogged

    def addLog(self, account: AccountModel, message: str, logType: str):
        log = LogModel.factoryLogModel(
            accountId=account.accountId,
            logMessage=message,
            logType=logType,
        )

        if log is not None:
            self.saveEntity(log.toEntity())

    def accountLogs(self, account: AccountModel) -> list[LogModel]:
        result = []

        try:
            logs = self.__session.query(LogEntity).filter(
                LogEntity.account_id == account.accountId, ).limit(10).all()

            logs.sort(
                key=lambda log: log.log_date,
                reverse=True,
            )

            for log in logs:
                result.append(LogModel.fromEntity(log))
        except Exception as e:
            print(e)

        return result

    @property
    def loggedAccountLogs(self) -> list[LogModel]:
        result = []

        if self.loggedAccount is not None:
            result = self.accountLogs(self.loggedAccount)

        return result

    def __repr__(self):
        return f'BankController(name={self.__name}, agency={self.__agency})'
