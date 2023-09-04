from modules.commands.command import Command


class Metadata(Command):
    def do(self, vm):
        vm.metadata()
