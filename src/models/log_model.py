import json
from uuid import uuid4
from datetime import datetime

from ..entities.log_entity import LogEntity


class LogModel:
    """
    Log model

    ...

    Parameters
    ----------
    logId : str
        Log id
    acocuntId : str
        Account id
    logDate : datetime
        Log date
    logType : str
        Log type
    logMessage : str
        Log message

    Methods
    -------
    factoryLogModel(accountId: str, logType: str, logMessage: str) -> LogModel
        Factory method to create a log model
    fromEntity(logEntity: LogEntity) -> LogModel
        Create a log model from a log entity
    toDict() -> dict
        Create a dict from the log model
    toEntity() -> LogEntity
        Create a log entity from the log model

    """
    __slots__ = [
        '__logId',
        '__acocuntId',
        '__logDate',
        '__logType',
        '__logMessage',
    ]

    def __init__(
        self,
        logId: str,
        acocuntId: str,
        logDate: datetime,
        logType: str,
        logMessage: str,
    ):
        self.__logId = logId
        self.__acocuntId = acocuntId
        self.__logDate = logDate
        self.__logType = logType
        self.__logMessage = logMessage

    @classmethod
    def factoryLogModel(
        cls,
        accountId: str,
        logType: str,
        logMessage: str,
    ):
        """
        Factory method to create a log model

        Parameters
        ----------
        accountId : str
            Account id
        logType : str
            Log type
        logMessage : str
            Log message

        Returns
        -------
        LogModel
            Log model
        """
        result = None

        result = cls(
            str(uuid4()),
            accountId,
            datetime.now(),
            logType,
            logMessage,
        )

        return result

    @classmethod
    def fromEntity(cls, logEntity: LogEntity) -> 'LogModel':
        """
        Create a log model from a log entity

        Parameters
        ----------
        logEntity : LogEntity
            Log entity

        Returns
        -------
        LogModel
            Log model
        """
        return cls(
            logEntity.log_id,  # type: ignore
            logEntity.account_id,  # type: ignore
            logEntity.log_date,  # type: ignore
            logEntity.log_type,  # type: ignore
            logEntity.log_message,  # type: ignore
        )

    def toEntity(self) -> LogEntity:
        """
        Create a log entity from the log model

        Returns
        -------
        LogEntity
            Log entity
        """
        return LogEntity(
            log_id=self.__logId,
            account_id=self.__acocuntId,
            log_date=self.__logDate,
            log_type=self.__logType,
            log_message=self.__logMessage,
        )

    def toDict(self) -> dict:
        """
        Create a dict from the log model

        Returns
        -------
        dict
            Log model dict
        """
        return {
            'logId': self.__logId,
            'acocuntId': self.__acocuntId,
            'logDate': self.__logDate.isoformat(),
            'logType': self.__logType,
            'logMessage': self.__logMessage,
        }

    def toJson(self) -> str:
        """
        Create a json from the log model

        Returns
        -------
        str
            Log model json
        """
        return json.dumps(self.toDict())

    def fromDict(self, data: dict):
        """
        Create a log model from a dict

        Parameters
        ----------
        data : dict
            Log model dict

        Returns
        -------
        LogModel
            Log model
        """
        return LogModel(
            data['logId'],
            data['acocuntId'],
            datetime.fromisoformat(data['logDate']),
            data['logType'],
            data['logMessage'],
        )

    def fromJson(self, data: str):
        """
        Create a log model from a json

        Parameters
        ----------
        data : str
            Log model json

        Returns
        -------
        LogModel
            Log model
        """
        return self.fromDict(json.loads(data))

    @property
    def logId(self) -> str:
        return self.__logId

    @property
    def acocuntId(self) -> str:
        return self.__acocuntId

    @property
    def logDate(self) -> datetime:
        return self.__logDate

    @property
    def logType(self) -> str:
        return self.__logType

    @property
    def logMessage(self) -> str:
        return self.__logMessage
