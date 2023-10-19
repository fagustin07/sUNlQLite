from btree.nodes import NodeDecoder
from btree.node_encoder import NodeEncoder
from utils.file_manager import FileManager


class Pager:

    def __init__(self, filename, table_name):
        file_manager = FileManager(filename, NodeEncoder())
        if file_manager.file_size() == 0:
            self.pages = NodeDecoder(file_manager).create_tree()
        else:
            self.pages = NodeDecoder(file_manager).init_tree()

    def metadata(self):
        return self.pages.count_metadata()

    def get_page(self, i):
        return self.pages.obtain(i)

    def insert(self, pk, username, email):
        self.pages = self.pages.insert(pk, username, email)

    @staticmethod
    def __page_size():
        return 4096

    def __num_pages(self):
        return self.pages.count_pages()

    def __num_records(self):
        return self.pages.count_records()
