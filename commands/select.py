from commands.command import Command


class Select(Command):

    def do(self, vm):
        vm.select()
