import json
import socket


from ..commands.login import login
from ..commands.deposit import deposit
from ..commands.register import register
from ..commands.withdraw import withdraw
from ..commands.transfer import transfer
from ..commands.logged_account_infos import loggedAccountInfos
from .bank_controller import BankController


class ClientBackController:
    def __init__(self, client, address, bankName, bankAgency, engine):
        self.__client: socket.socket = client
        self.__address = address
        self.__buffer_size = 1024

        self.__bank = BankController.factorybankControllerWithEngine(
            bankName, bankAgency, engine,
        )

        self.commands = {
            'login': login,
            'register': register,
            'loggedAccountInfos': loggedAccountInfos,
            'deposit': deposit,
            'withdraw': withdraw,
            'transfer': transfer,
        }

    def start(self):
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
                response = self.commands[data['command']](data, self.__bank)
                self.send(response)
            else:
                self.send({'status': 'command not found'})

    def send(self, data):
        # Envia um json em pacotes de 1024 bytes
        # "end" é uma flag que indica o fim da mensagem

        dataStr = json.dumps(data)

        for i in range(0, len(dataStr), self.__buffer_size):
            self.__client.send(dataStr[i:i+self.__buffer_size].encode('utf-8'))

        self.__client.send('end'.encode('utf-8'))

    def receive(self) -> dict[str, str]:
        # Recebe um json em pacotes de 1024 bytes
        # "end" é uma flag que indica o fim da mensagem

        data = ''

        while True:
            data += self.__client.recv(self.__buffer_size).decode('utf-8')

            if data[-3:] == 'end':
                break

        data = data[:-3]

        return json.loads(data)