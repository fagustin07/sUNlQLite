from modules.commands.command import Command


class Exit(Command):
    def do(self, vm):
        print('Terminado')
        vm.finish()
