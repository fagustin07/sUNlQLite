from domain.pager import Pager


class Table:
    def __init__(self, name, data_file):
        self.name = name
        self.pager = Pager(data_file, name)

    def insert(self, pk, username, email):
        self.pager.insert(pk, username, email)

    def select(self):
        return self.pager.pages.select_all()

    def metadata(self):
        return self.pager.metadata()
