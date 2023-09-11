from modules.file_manager import FileManager
from modules.page import Page


class Pager:

    def __init__(self, filename):
        self.file_manager = FileManager(filename)
        self.amount_pages, self.amount_records = self.file_manager.get_metadata()
        self.pages_dict = dict()

    def metadata(self):
        return self.amount_pages, self.amount_records

    def get_page(self, i):
        maybe_page = self.pages_dict.get(i)
        if maybe_page is not None:
            return maybe_page
        elif i < self.amount_pages - 1:
            self.pages_dict[i] = Page(self.file_manager.get_data(i * 4096, (i + 1) * 4096))
            return self.pages_dict[i]
        elif i > self.amount_pages:
            print('Numero de pagina inexistente')
            return None
        else:
            page_start = (self.amount_pages-1) * 4096
            page_end = page_start + (self.amount_records - ((self.amount_pages-1) * 14)) * 291
            self.pages_dict[i - 1] = Page(self.file_manager.get_data(page_start, page_end))
            return self.pages_dict[i - 1]

    def page_to_write(self):
        if self.pages_dict.get(self.amount_pages - 1) is not None:
            curr_page = self.pages_dict[self.amount_pages - 1]
            if curr_page.can_insert_record():
                return curr_page
            else:
                new_page = Page(bytearray())
                self.pages_dict[self.amount_pages] = new_page
                self.amount_pages += 1
                return new_page
        else:
            page_start = (self.amount_pages-1) * 4096
            page_end = page_start + (self.amount_records - ((self.amount_pages-1) * 14)) * 291
            data = self.file_manager.get_data(page_start, page_end)
            page = Page(data)

        if page.can_insert_record():
            self.pages_dict[self.amount_pages - 1] = page
            return page
        else:
            new_page = Page(bytearray())
            self.pages_dict[self.amount_pages] = new_page
            self.amount_pages += 1
            return new_page

    def incr_record(self):
        self.amount_records += 1

    def all(self):
        self.__load_all_data_in_cache()
        return self.pages_dict.values()

    def commit(self):
        data = bytearray()
        curr_byte = 0
        for page in self.all():
            if page.amount_record < 14:
                data[curr_byte:curr_byte * page.amount_record * 291] = page.records[0:page.amount_record*291]
            else:
                data[curr_byte:curr_byte * page.amount_record * 291] = page.records
            curr_byte += 4096
        self.file_manager.commit(data)

    def __load_all_data_in_cache(self):
        curr_page = 0
        while curr_page < self.amount_pages:
            page_obj = self.pages_dict.get(curr_page)
            if page_obj is None:
                self.pages_dict[curr_page] = Page(self.file_manager.get_data(curr_page * 4096, (curr_page+1) * 4096))
            curr_page += 1
