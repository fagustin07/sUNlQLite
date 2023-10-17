from commands.command import Command


class InvalidCommand(Command):
    def do(self, vm):
        print('Operación inválida')
