import json
from uuid import uuid4

from ..entities.person_entity import PersonEntity


class PersonModel:
    """
    Person model

    ...

    Parameters
    ----------
    personId : str
        Person id
    firstName : str
        Person first name
    lastName : str
        Person last name
    age : int
        Person age
    cpf : str
        Person cpf

    Methods
    -------
    factoryPersonModel(firstName: str, lastName: str, age: int, cpf: str) -> PersonModel
        Factory method to create a person model
    fromEntity(personEntity: PersonEntity) -> PersonModel
        Create a person model from a person entity
    toDict() -> dict
        Create a dict from the person model
    toEntity() -> PersonEntity
        Create a person entity from the person model
    """

    def __init__(
        self,
        personId: str,
        firstName: str,
        lastName: str,
        age: int,
        cpf: str,
    ):
        self.__personId = personId
        self.__firstName = firstName
        self.__lastName = lastName
        self.__age = age
        self.__cpf = cpf

    @classmethod
    def factoryPersonModel(
        cls,
        firstName: str,
        lastName: str,
        age: int,
        cpf: str,
    ):
        """
        Factory method to create a person model

        Parameters
        ----------
        firstName : str
            Person first name
        lastName : str
            Person last name
        age : int
            Person age
        cpf : str
            Person cpf

        Returns
        -------
        PersonModel
            Person model
        """
        result = None

        # validar cpf, age, personName
        if ((cpf.isnumeric() or len(cpf) != 11) and isinstance(age, int)
                and age > 0 and age < 100 and len(lastName) > 1
                and len(firstName) > 1):

            result = cls(
                str(uuid4()),
                firstName,
                lastName,
                age,
                cpf,
            )

        return result

    @classmethod
    def empty(cls) -> 'PersonModel':
        """
        Create an empty person model

        Returns
        -------
        PersonModel
            Person model
        """
        return cls(
            str(uuid4()),
            '',
            '',
            0,
            '',
        )

    @classmethod
    def fromEntity(cls, personEntity: PersonEntity) -> 'PersonModel':
        """
        Create a person model from a person entity

        Parameters
        ----------
        personEntity : PersonEntity
            Person entity

        Returns
        -------
        PersonModel
            Person model
        """
        return cls(
            personEntity.person_id,  # type: ignore
            personEntity.person_first_name,  # type: ignore
            personEntity.person_last_name,  # type: ignore
            personEntity.person_age,  # type: ignore
            personEntity.person_cpf,  # type: ignore
        )

    def toEntity(self) -> PersonEntity:
        """
        Create a person entity from the person model

        Returns
        -------
        PersonEntity
            Person entity
        """
        return PersonEntity(
            person_id=self.personId,
            person_first_name=self.firstName,
            person_last_name=self.lastName,
            person_age=self.age,
            person_cpf=self.cpf,
        )

    def toDict(self) -> dict:
        """
        Create a dict from the person model

        Returns
        -------
        dict
            Person model dict
        """
        return {
            'personId': self.personId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'age': self.age,
            'cpf': self.cpf,
        }

    def toJson(self) -> str:
        return str(self.toDict())

    def fromDict(self, personDict: dict):
        return PersonModel(
            personDict['personId'],
            personDict['firstName'],
            personDict['lastName'],
            personDict['age'],
            personDict['cpf'],
        )

    def fromJson(self, personJson: str):
        """
        Create a person model from a json

        Parameters
        ----------
        personJson : str
            Person json

        Returns
        -------
        PersonModel
            Person model
        """
        return self.fromDict(json.loads(personJson))

    @property
    def personId(self) -> str:
        return self.__personId

    @property
    def firstName(self) -> str:
        return self.__firstName

    @firstName.setter
    def firstName(self, value: str):
        self.__firstName = value

    @property
    def lastName(self) -> str:
        return self.__lastName

    @lastName.setter
    def lastName(self, value: str):
        self.__lastName = value

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int):
        self.__age = value

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, value: str):
        self.__cpf = value
