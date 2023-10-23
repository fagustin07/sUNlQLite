from commands.command import Command


class Clear(Command):
    def do(self, vm):
        return vm.clear_console()
