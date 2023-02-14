# import json
import socket
import threading as td
import sqlalchemy as sa
from .client_back_controller import ClientBackController

"""
Uma classe que representa um controlador de serviço.

Ela permite que o usuário possa iniciar,
parar e reiniciar o uso do serviço do banco.
A comunicação com o serviço é feita através de sockets e json.
"""


class ServiceController:
    def __init__(self):
        self.__host = '0.0.0.0'
        self.__port = 8000

        self.__threads = []

        self.bankAgency = '1234'
        self.bankName = 'evil bank'

        self.__engine = self.__createEngine(self.bankName)
        self.__connection = self.__engine.connect()

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host, self.__port))
        self.__socket.listen(10)

        self.__lock = td.Lock()

    def start(self):
        print('Start service')
        while True:
            client, address = self.__socket.accept()

            # Verificar se o cliente foi recebido
            if client:
                print(f'Cliente conectado: {address}')

                # Criar uma nova thread para atender o cliente
                client_thread = td.Thread(
                    target=ClientBackController(
                        client=client,
                        address=address,
                        bankName=self.bankName,
                        bankAgency=self.bankAgency,
                        engine=self.__engine,
                    ).start,
                    args=(self.__lock,),
                )

                self.__threads.append(client_thread)
                client_thread.start()

    # def verifyThreadsClosed(self):
    #     for thread in self.__threads:
    #         if not thread.is_alive():
    #             self.__threads.remove(thread)

    def __createEngine(self, name):
        dataBaseName = name.lower().replace(' ', '')

        engine = sa.create_engine(
            'mysql+mysqlconnector://root:123456@localhost:3306')
        engine.execute(f'CREATE DATABASE IF NOT EXISTS {dataBaseName}')
        engine = sa.create_engine(
            f'mysql+mysqlconnector://root:123456@localhost:3306/{dataBaseName}'
        )

        return engine

    def stop(self):
        ...


if __name__ == '__main__':
    service_controller = ServiceController()
    service_controller.start()
