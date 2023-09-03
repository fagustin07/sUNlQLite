from modules.compiler import Compiler
from modules.vm import VirtualMachine


class SunQLite:
    def __init__(self, compiler: Compiler, vm: VirtualMachine):
        self.compiler = compiler
        self.vm = vm
        self.can_exec = True

    def start(self):
        while self.can_exec:
            user_input = input("sql>")  # Espera la entrada del usuario
            command = self.compiler.do(user_input)
            self.vm.do(command)
