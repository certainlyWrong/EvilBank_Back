import json
from uuid import uuid4

from ..entities.person_entity import PersonEntity


class PersonModel:

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
        return cls(
            str(uuid4()),
            '',
            '',
            0,
            '',
        )

    @classmethod
    def fromEntity(cls, personEntity: PersonEntity) -> 'PersonModel':
        return cls(
            personEntity.person_id,  # type: ignore
            personEntity.person_first_name,  # type: ignore
            personEntity.person_last_name,  # type: ignore
            personEntity.person_age,  # type: ignore
            personEntity.person_cpf,  # type: ignore
        )

    def toEntity(self) -> PersonEntity:
        return PersonEntity(
            person_id=self.personId,
            person_first_name=self.firstName,
            person_last_name=self.lastName,
            person_age=self.age,
            person_cpf=self.cpf,
        )

    def toDict(self) -> dict:
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
