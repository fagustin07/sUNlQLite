from utils.decoder import Decoder
from domain.pager import Pager


class Table:
    def __init__(self, name, data_file):
        self.name = name
        self.decoder = Decoder()
        self.pager = Pager(data_file)

    def insert(self, pk, username, email):
        self.pager.page_to_write().insert(pk, username, email)

    def select(self):
        return self.pager.pages.data()

    def metadata(self):
        return self.pager.metadata()

    def commit(self):
        self.pager.commit()
