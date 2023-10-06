from abc import abstractmethod


class Command:
    @abstractmethod
    def do(self, vm):
        pass
