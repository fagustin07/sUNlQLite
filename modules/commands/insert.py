from modules.commands.command import Command
from modules.encoder import Encoder


class Insert(Command):
    def __init__(self, pk: int, username: str, email: str):
        self.encoder = Encoder()
        self.id = pk
        self.username = username
        self.email = email

    def do(self, vm):
        vm.insert(self.encoder.do(self.id, self.username, self.email))
