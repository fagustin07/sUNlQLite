from modules.commands.command import Command
from modules.commands.command_enum import EnumCommand
from modules.vm import VirtualMachine


class Insert(Command):

    def __init__(self, pk: int, email: str, name: str):
        self.id = pk
        self.email = email
        self.name = name

    def do(self, vm: VirtualMachine):
        print("INSERT no implementado")
