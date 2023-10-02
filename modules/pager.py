from modules.file_manager import FileManager
from modules.node import Node
from modules.node_instanciator import NodeInstanciator
from modules.page import Page


class Pager:

    def __init__(self, filename):
        self.file_manager = FileManager(filename)
        if self.file_manager.file_size() == 0:
            self.pages = NodeInstanciator().create_tree()
        else:
            self.pages = NodeInstanciator().init_tree(self.file_manager.file())

    def metadata(self):
        return self.pages.count_pages(), self.pages.count_records()

    def get_page(self, i):
        return self.pages.obtain(i)

    def page_to_write(self):
        return self.pages

    def commit(self):
        print(self)
        # data = self.file_manager.file()
        # for page_kv in self.pages_dict.items():
        #     page = page_kv[1]
        #     offset = page_kv[0]
        #     if page.have_changes:
        #         curr_byte = self.__page_size() * offset
        #         if page.amount_record < 14:
        #             records = page.records[0:page.amount_record * 291]
        #         else:
        #             records = page.records
        #         data[curr_byte:curr_byte + page.amount_record * 291] = records
        # self.file_manager.commit(data)

    @staticmethod
    def __page_size():
        return 4096

    def __num_pages(self):
        return self.pages.count_pages()

    def __num_records(self):
        return self.pages.count_records()
