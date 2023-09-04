from modules.decoder import Decoder
from modules.page import Page


class Table:
    def __init__(self, name):
        self.name = name
        self.decoder = Decoder()
        self.pages = []
        fst_page = Page()
        self.pages.append(fst_page)
        self.current_page: Page = fst_page
        self.amount_pages = 1
        self.amount_records = 0

    def insert(self, record):
        if not self.current_page.can_insert_record():
            new_page = Page()
            self.pages.append(new_page)
            self.current_page = new_page
            self.amount_pages += 1

        self.current_page.insert(record)
        self.amount_records += 1

    def select(self):
        records = []
        for page in self.pages:
            for record in page.select():
                records.append(record)

        return records

    def metadata(self):
        return self.amount_pages, self.amount_records
