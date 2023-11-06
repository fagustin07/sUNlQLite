from exceptions.subclass_responsability import SubclassResponsability
from utils.file_manager import FileManager


class AbstractNode:

    def __init__(self, is_root: bool, parent: int, num_page: int, file_manager: FileManager, node_decoder):
        self.is_leaf = False
        self.is_root = is_root
        self.parent = parent
        self.file_manager = file_manager
        self.num_page = num_page
        self.node_caller = node_decoder

    # ACTIONS

    def insert(self, pk, username, email):
        raise SubclassResponsability()

    def data(self):
        raise SubclassResponsability()

    def change_parent_to(self, node):
        self.parent = node.num_page
        self.file_manager.save(self)
