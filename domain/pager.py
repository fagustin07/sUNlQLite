from btree.node_encoder import NodeEncoder
from btree.node_instanciator import NodeInstanciator
from utils.file_manager import FileManager


class Pager:

    def __init__(self, filename):
        self.__file_manager = FileManager(filename)
        if self.__file_manager.file_size() == 0:
            self.pages = NodeInstanciator().create_tree()
        else:
            self.pages = NodeInstanciator().init_tree(self.__file_manager.file())

    def metadata(self):
        return self.pages.count_pages(), self.pages.count_records()

    def get_page(self, i):
        return self.pages.obtain(i)

    def page_to_write(self):
        return self.pages

    def commit(self):
        self.__file_manager.commit(NodeEncoder().do(self.pages))

    @staticmethod
    def __page_size():
        return 4096

    def __num_pages(self):
        return self.pages.count_pages()

    def __num_records(self):
        return self.pages.count_records()
