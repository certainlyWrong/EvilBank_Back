import hashlib
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from ..models.log_model import LogModel, LogEntity
from ..models.person_model import PersonModel, PersonEntity
from ..models.account_model import AccountModel, AccountEntity
from ..entities import Base


class BankController:
    """
    A class used to represent a BankController

    ...

    Attributes
    ----------
    __name : str
        the name of the bank
    __agency : str
        the agency of the bank
    __engine : sa.engine.Engine
        the engine of the bank
    __connection : sa.engine.Connection
        the connection of the bank
    __session : sa.orm.session.Session
        the session of the bank
    __loggedAccount : AccountModel
        the logged account of the bank
    __loggedPerson : PersonModel
        the logged person of the bank

    Methods
    -------
    factoryWithNameAndAgency(name: str, agency: str)
        Creates a new BankController with a name and agency
    factoryWithEngine(name: str, agency: str, engine: sa.engine.Engine)
        Creates a new BankController with a name, agency and engine
    dispose()
        Disposes the BankController
    createAccount(personFirstName: str, personLastName: str, age: int, cpf: str, accountName: str, accountPassword: str, accountBalance: float, accountLimit: float, commit: bool = False)
        Creates a new account
    createPerson(firstName: str, lastName: str, age: int, cpf: str, commit: bool = False)
        Creates a new person
    login(accountName: str, accountPassword: str)
        Logs in the bank
    accountById(accountId: str)
        Gets an account by id
    personByCpf(cpf: str)
        Gets a person by cpf
    checkAccountNameExists(accountName: str)
        Checks if an account name exists
    checkPersonCpfExists(cpf: str)
        Checks if a person cpf exists
    saveEntity(entity: Base)
        Saves an entity
    saveLog(log: LogModel)
        Saves a log
    """

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
        self.__loggedPerson = None

    @classmethod
    def factoryWithNameAndAgency(cls, name: str, agency: str):
        """
        Creates a new BankController with a name and agency

        Parameters
        ----------
        name : str
            the name of the bank
        agency : str
            the agency of the bank

        Returns
        -------
        BankController
            the new BankController

        """

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
    def factoryWithEngine(
        cls,
        name: str,
        agency: str,
        engine: sa.engine.Engine
    ):
        """
        Creates a new BankController with a name, agency and engine

        Parameters
        ----------
        name : str
            the name of the bank
        agency : str
            the agency of the bank
        engine : sa.engine.Engine
            the engine of the bank

        Returns
        -------
        BankController
            the new BankController
        """
        Base.metadata.create_all(engine)

        return cls(name, agency, engine)

    def dispose(self):
        """
        Disposes the BankController
        """
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
        """
        Creates a new account

        Parameters
        ----------
        personFirstName : str
            the first name of the person
        personLastName : str
            the last name of the person
        age : int
            the age of the person
        cpf : str
            the cpf of the person
        accountName : str
            the name of the account
        accountPassword : str
            the password of the account
        accountBalance : float
            the balance of the account
        accountLimit : float
            the limit of the account
        commit : bool, optional
            if the account should be commited, by default False

        Returns
        -------
        AccountModel
            the new account

        """
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
        """
        Creates a new person

        Parameters
        ----------
        firstName : str
            the first name of the person
        lastName : str
            the last name of the person
        age : int
            the age of the person
        cpf : str
            the cpf of the person
        commit : bool, optional
            if the person should be commited, by default False

        Returns
        -------
        PersonModel
            the new person
        """
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
        """
        Logs in an account

        Parameters
        ----------
        accountName : str
            the name of the account
        accountPassword : str
            the password of the account

        Returns
        -------
        bool
            if the login was successful
        """
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
            self.__loggedPerson = PersonModel.fromEntity(personResult)
            result = True
        except Exception as e:
            print(e)

        return result

    def accountById(self, accountId: str):
        """
        Gets an account by its id

        Parameters
        ----------
        accountId : str
            the id of the account

        Returns
        -------
        AccountModel
            the account
        """
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
        """
        Gets a person by its cpf

        Parameters
        ----------
        cpf : str
            the cpf of the person

        Returns
        -------
        PersonModel
            the person
        """
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
        """
        Gets an account by its person id

        Parameters
        ----------
        personId : int
            the id of the person

        Returns
        ------- 
        AccountModel
            the account
        """
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
        """
        Gets an account by its name

        Parameters
        ----------
        accountName : str
            the name of the account

        Returns
        -------
        AccountModel
            the account
        """
        result = None

        try:
            accountResult = self.__session.query(AccountEntity).filter(
                AccountEntity.account_name == accountName, ).one()

            result = AccountModel.fromEntity(accountResult)
        except Exception as e:
            print(e)

        return result

    def accountsByStringInName(self, string: str) -> list[AccountModel]:
        """
        Gets a list of accounts that have a string in their name

        Parameters
        ----------
        string : str
            the string to search for

        Returns
        -------
        list[AccountModel]
            the list of accountsf
        """
        result = []

        try:
            accountResults = self.__session.query(AccountEntity).filter(
                AccountEntity.account_name.like(f'%{string}%'), ).limit(10)

            for accountResult in accountResults:
                result.append(AccountModel.fromEntity(accountResult))
        except Exception as e:
            print(e)

        return result

    # TODO: Implementar conta que busque um usuário pelo CPF
    def accountByCPF(self, cpf: str) -> AccountModel:
        ...

    def checkAccountNameExists(self, accountName: str):
        """
        Checks if an account name exists

        Parameters
        ----------
        accountName : str
            the name of the account

        Returns
        -------
        bool
            if the account name exists
        """
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
        """
        Checks if an account name exists

        Parameters
        ----------
        accountName : str
            the name of the account

        Returns
        ------- 
        bool
            if the account name exists
        """
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
        """
        Withdraws money from an account

        Parameters
        ----------
        account : AccountModel
            the account
        value : float
            the value to withdraw

        Returns
        -------
        bool
            if the withdraw was successful

        """
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
        """
        Deposits money into an account

        Parameters
        ----------
        account : AccountModel
            the account
        value : float
            the value to deposit

        Returns
        -------
        bool
            if the deposit was successful
        """
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
        """
        Transfers money from one account to another

        Parameters
        ----------
        accountFrom : AccountModel
            the account to transfer from
        accountTo : AccountModel
            the account to transfer to
        value : float
            the value to transfer

        Returns
        -------
        bool
            if the transfer was successful
        """
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
        """
        Transfers money from one account to another

        Parameters
        ----------
        accountFrom : AccountModel
            the account to transfer from
        accountToName : str
            the name of the account to transfer to
        value : float
            the value to transfer

        Returns
        -------
        bool
            if the transfer was successful
        """
        result = False

        if (accountFrom is not None and accountToName is not None and value > 0
                and accountFrom.balance >= value):
            accountTo = self.accountByName(accountToName)

            if accountTo is not None:
                result = self.transfer(accountFrom, accountTo, value)

        return result

    # TODO: testar
    def saveEntity(self, entity: Base) -> bool:
        """
        Saves an entity

        Parameters
        ----------
        entity : Base
            the entity to save

        Returns
        -------
        bool
            if the entity was saved
        """
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
        """
        Updates an entity

        Parameters
        ----------
        entity : Base
            the entity to update

        Returns
        -------
        bool
            if the entity was updated
        """
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
        """
        Deletes an entity

        Parameters
        ----------
        entity : Base
            the entity to delete

        Returns
        -------
        bool
            if the entity was deleted
        """
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
    def refreshLoggedAccount(self):
        """
        Refreshes the logged account

        Returns
        -------
        None
        """
        if self.__loggedPerson is not None:
            self.__loggedPerson = self.personByCpf(self.__loggedPerson.cpf)

        if self.__loggedAccount is not None:
            self.__loggedAccount = self.accountByPersonId(
                self.__loggedAccount.personId)

    @property
    def isLogged(self) -> bool:
        """
        Checks if the user is logged

        Returns
        -------
        bool
            if the user is logged
        """
        return (self.__loggedAccount is not None
                and self.__loggedPerson is not None)

    @property
    def loggedAccount(self) -> AccountModel | None:
        """
        Gets the logged account

        Returns
        -------
        AccountModel | None
            the logged account
        """
        self.refreshLoggedAccount

        return self.__loggedAccount

    @property
    def loggedPerson(self) -> PersonModel | None:
        """
        Gets the logged person

        Returns
        -------
        PersonModel | None
            the logged person
        """
        return self.__loggedPerson

    def addLog(self, account: AccountModel, message: str, logType: str):
        """
        Adds a log to an account

        Parameters
        ----------
        account : AccountModel
            the account
        message : str
            the message
        logType : str
            the log type

        Returns
        -------
        None

        """
        log = LogModel.factoryLogModel(
            accountId=account.accountId,
            logMessage=message,
            logType=logType,
        )

        if log is not None:
            self.saveEntity(log.toEntity())

    def accountLogs(self, account: AccountModel) -> list[LogModel]:
        """
        Gets the logs of an account

        Parameters
        ----------
        account : AccountModel
            the account

        Returns
        -------
        list[LogModel] 
            the logs of the account
        """
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
        """
        Gets the logs of the logged account

        Returns
        -------
        list[LogModel]
            the logs of the logged account
        """
        result = []

        # Atualiza a conta logada
        self.refreshLoggedAccount

        if self.loggedAccount is not None:
            result = self.accountLogs(self.loggedAccount)

        return result

    def __repr__(self):
        return f'BankController(name={self.__name}, agency={self.__agency})'
