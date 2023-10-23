import os

from domain.compiler import Compiler
from domain.table import Table
from exceptions.duplicate_key import DuplicateKeyException
from exceptions.page_full import PageFullException
from exceptions.record_not_found import RecordNotFoundException


class SunQLite:
    def __init__(self, data_file):
        self.compiler = Compiler()
        self.keep_running = True
        self.table = Table('user', data_file)

    def start(self):
        command_global = None

        while self.keep_running:
            user_input = input("sql>")
            try:
                command_global = self.compiler.do(user_input)
            except Exception:
                print('Se produjo un error en compilación')
            try:
                command_global.do(self)
            except PageFullException:
                print('Split de nodo interno no implementado')
            except DuplicateKeyException:
                print('Clave duplicada')
            except RecordNotFoundException:
                print('Registro no encontrado')
            except Exception as e:
                raise e

    def insert(self, pk, username, email):
        self.table.insert(pk, username, email)
        print('INSERT exitoso')

    def select(self):
        for record in self.table.select():
            print(record[0], record[1], record[2])

    def finish(self):
        self.keep_running = False

    @staticmethod
    def clear_console():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def metadata(self):
        metadata = self.table.metadata()
        print('Paginas: ' + str(metadata[0]))
        print('Registros: ' + str(metadata[1]))
