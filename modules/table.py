from modules.decoder import Decoder
from modules.pager import Pager


class Table:
    def __init__(self, name, data_file):
        self.name = name
        self.decoder = Decoder()
        self.pager = Pager(data_file)

    def insert(self, record):
        curr_page = self.pager.page_to_write()
        curr_page.insert(record)

    def select(self):
        return self.pager.pages.data()

    def metadata(self):
        return self.pager.metadata()

    def commit(self):
        self.pager.commit()
