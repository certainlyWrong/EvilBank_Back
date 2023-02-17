import json
import socket
from threading import Lock

# from ..commands.login import login
# from ..commands.deposit import deposit
# from ..commands.register import register
# from ..commands.withdraw import withdraw
# from ..commands.transfer import transfer
# from ..commands.logged_account_infos import loggedAccountInfos
# from ..commands.search_accounts import searchAccounts
# from .bank_controller import BankController


class ClientBackController:
    """
    Client back controller

    ...

    Parameters
    ----------
    client : socket.socket
        Client socket
    address : tuple
        Client address
    bankName : str
        Bank name
    bankAgency : str
        Bank agency
    engine : sqlalchemy.engine.Engine
        Database engine

    Methods
    -------
    start(lock: threading.Lock)
        Start the client back controller
    send(data: dict)
        Send data to the client
    receive() -> dict
        Receive data from the client
    """

    def __init__(
            self,
            client,
            address,
            bankName,
            bankAgency,
            engine,
    ):
        self.__client: socket.socket = client
        self.__address = address
        self.__buffer_size = 1024

        # self.__bank = BankController.factoryWithEngine(
        #     bankName, bankAgency, engine,
        # )

        self.__bank = BankController(
            name=bankName,
            agency=bankAgency,
            engine=engine,
        )

        # self.__bank = BankController.factoryWithNameAndAgency(
        #     bankName, bankAgency,
        # )

        self.commands = {
            'login': login,
            'register': register,
            'loggedAccountInfos': loggedAccountInfos,
            'deposit': deposit,
            'withdraw': withdraw,
            'transfer': transfer,
            'searchAccounts': searchAccounts,
        }

    def start(self, lock: Lock):
        """
        Start the client back controller

        Parameters
        ----------
        lock : threading.Lock
            Lock to avoid database access at the same time

        Returns
        -------
        None
        """
        while True:
            data = self.receive()

            if data['command'] == 'exit':
                print(f'Cliente desconectado: {self.__address}')
                self.__client.close()
                break

            if data['command'] in self.commands:
                print(
                    f'Cliente { self.__address } | comando {data["command"]}',
                )

                """ O lock é usado para evitar que duas threads
                acessem o banco de dados ao mesmo tempo.

                Apesar de não ser necessário devido as propriedades ACID
                do banco de dados, é uma boa prática de programação."""
                lock.acquire()
                response = self.commands[data['command']](data, self.__bank)
                lock.release()

                self.send(response)
            else:
                self.send({'status': 'command not found'})

    def send(self, data):
        """
        Send data to the client

        Parameters
        ----------
        data : dict
            Data to send

        Returns
        -------
        None
        """

        dataStr = json.dumps(data)

        for i in range(0, len(dataStr), self.__buffer_size):
            self.__client.send(dataStr[i:i+self.__buffer_size].encode('utf-8'))

        self.__client.send('end'.encode('utf-8'))

    def receive(self) -> dict[str, str]:
        """
        Receive data from the client

        Returns
        -------
        dict[str, str]
            Data received
        """

        data = ''

        while True:
            data += self.__client.recv(self.__buffer_size).decode('utf-8')

            if data[-3:] == 'end':
                break

        data = data[:-3]
        return json.loads(data)
