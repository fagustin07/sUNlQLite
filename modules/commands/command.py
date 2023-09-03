from abc import ABC, abstractmethod

from modules.vm import VirtualMachine


class Command:
    @abstractmethod
    def do(self, vm: VirtualMachine):
        pass
