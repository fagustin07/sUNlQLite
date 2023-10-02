from modules.compiler import Compiler
from modules.exceptions.duplicate_key import DuplicateKeyException
from modules.exceptions.page_full import PageFullException
from modules.table import Table


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
            except Exception as e:
                print('Se produjo un error en compilación')
                raise e

            try:
                command_global.do(self)
            except PageFullException as e:
                print('Split no implementado')
            except DuplicateKeyException as e:
                print('Clave duplicada')
            except Exception as e:
                print('Se produjo un error en ejecución')

    def insert(self, record):
        self.table.insert(record)
        print('INSERT exitoso')

    def select(self):
        for record in self.table.select():
            print(record[0], record[1], record[2])

    def finish(self):
        self.table.commit()
        self.keep_running = False

    def metadata(self):
        metadata = self.table.metadata()
        print('Paginas: ' + str(metadata[0]))
        print('Registros: ' + str(metadata[1]))
