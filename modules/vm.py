import sys


class VirtualMachine:

    def do(self, command):
        command.do(self)

    @staticmethod
    def finish():
        sys.exit()
