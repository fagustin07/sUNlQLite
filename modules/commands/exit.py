from modules.commands.command import Command
from modules.vm import VirtualMachine


class Exit(Command):
    def do(self, vm: VirtualMachine):
        print("Terminado")
        vm.finish()
