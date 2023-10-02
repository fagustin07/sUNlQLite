from modules.compiler import Compiler
from modules.exceptions.duplicate_key import DuplicateKeyException
from modules.exceptions.page_full import PageFullException
from modules.exceptions.record_not_found import RecordNotFoundException
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
                raise e
            finally:
                print('Se produjo un error en compilación')
            try:
                command_global.do(self)
            except PageFullException:
                print('Split no implementado')
            except DuplicateKeyException:
                print('Clave duplicada')
            except RecordNotFoundException:
                print('Registro no encontrado')
            except Exception:
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
