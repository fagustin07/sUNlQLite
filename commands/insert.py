from commands.command import Command
from utils.encoder import Encoder


class Insert(Command):
    def __init__(self, pk: int, username: str, email: str):
        self.encoder = Encoder()
        self.pk = pk
        self.username = username
        self.email = email

    def do(self, vm):
        vm.insert(self.pk, self.username, self.email)
