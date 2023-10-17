from exceptions.subclass_responsability import SubclassResponsability
from utils.file_manager import FileManager


class AbstractNode:

    def __init__(self, is_root: bool, parent: int, num_page: int, file_manager: FileManager, max_num_rec=13):
        self.is_leaf = False
        self.is_root = is_root
        self.parent = parent
        self.file_manager = file_manager
        self.num_page = num_page
        self.max_num_rec = max_num_rec

    # ACTIONS

    def insert(self, pk, username, email):
        raise SubclassResponsability()

    def data(self):
        raise SubclassResponsability()

