from modules.commands.command import Command


class InvalidCommand(Command):
    def do(self, vm):
        print("Comando no reconocido")
