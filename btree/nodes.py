from btree.abstract_node import AbstractNode
from exceptions.duplicate_key import DuplicateKeyException
from exceptions.method_not_implemented import MethodNotImplemented
from exceptions.page_full import PageFullException
from utils.decoder import Decoder
from utils.file_manager import FileManager


class Leaf(AbstractNode):

    def __init__(self, is_root: bool, parent: int, num_records: int, pointer_records: list, num_page: int,
                 file_manager: FileManager, max_num_rec=13):
        super().__init__(is_root, parent, num_page, file_manager, max_num_rec)
        self.is_leaf = True
        self.num_records = num_records
        self.records = pointer_records

    # ACTIONS

    def insert(self, pk, username, email):
        if self.num_records == self.max_num_rec:
            return self.__split_leaf(pk, username, email)
        else:
            self.__do_binary_insert(pk, username, email)
            self.num_records += 1
            self.file_manager.save(self)
            return self

    def insert_and_split_for_parent(self, pk, username, email):
        self.__do_binary_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2 if (self.num_records + 1) // 2 > 0 else 1
        l_tree = Leaf(False, self.parent, num_records, self.records[:num_records],
                      self.num_page, self.file_manager, self.max_num_rec)
        r_tree = Leaf(False, self.parent, num_records, self.records[num_records:],
                      self.file_manager.next_num_page(), self.file_manager, self.max_num_rec)
        return l_tree, r_tree

    # ACCESSING

    def select_all(self):
        return list(map(lambda record_kv: [record_kv[0], record_kv[1][0], record_kv[1][1]], self.records))

    def count_metadata(self):
        return 1, self.num_records

    def last_key_record(self):
        return self.records[-1][0]

    # TESTING

    def can_insert(self):
        return self.num_records < self.max_num_rec

    # PRIVATE ACTIONS

    def __split_leaf(self, pk, username, email):
        self.__do_binary_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2

        l_tree = Leaf(False, self.num_page, num_records, self.records[:num_records],
                      self.file_manager.next_num_page(), self.file_manager, self.max_num_rec)
        self.file_manager.save(l_tree)

        r_tree = Leaf(False, self.num_page, num_records, self.records[num_records:],
                      self.file_manager.next_num_page(), self.file_manager, self.max_num_rec)
        self.file_manager.save(r_tree)

        base_node = Internal(self.is_root, self.parent, 1,
                             dict({l_tree.last_key_record(): l_tree.num_page}),
                             r_tree.num_page, self.num_page, self.file_manager, 510)

        self.file_manager.save(base_node)

        return base_node

    def __do_binary_insert(self, pk, username, email):
        left, right = 0, len(self.records) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.records[mid][0] == pk:
                raise DuplicateKeyException()
            elif self.records[mid][0] < pk:
                left = mid + 1
            else:
                right = mid - 1
        self.records.insert(left, [pk, [username, email]])

    # PRIVATE TESTING

    def __binary_contains(self, key):
        left, right = 0, len(self.records) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.records[mid][0] == key:
                return True
            elif self.records[mid][0] < key:
                left = mid + 1
            else:
                right = mid - 1
        return False

##############################################################################################################


class Internal(AbstractNode):
    def __init__(self, is_root: bool, parent: int, num_keys: int, children: dict, right_child: int, num_page: int,
                 file_manager: FileManager, max_num_rec=510):
        super().__init__(is_root, parent, num_page, file_manager, max_num_rec)
        self.__num_keys = num_keys
        self.__children = children
        self.__right_child = right_child
        self.__node_caller = NodeDecoder(file_manager)

    # ACTIONS

    def insert(self, pk, username, email):
        if self.__num_keys == self.max_num_rec:
            raise PageFullException()

        subtree_key, subtree_num_page = self.__find_subtree_can_contain(pk)
        not_exist_tree = subtree_num_page is None
        if not_exist_tree:
            subtree_to_insert = self.__node_caller.seek_node(self.__right_child)
            if subtree_to_insert.can_insert():
                subtree_to_insert.insert(pk, username, email)
                self.file_manager.save(subtree_to_insert)
            else:
                l_tree, r_tree = subtree_to_insert.insert_and_split_for_parent(pk, username, email)
                self.__children[l_tree.last_key_record()] = l_tree.num_page
                self.__right_child = r_tree.num_page
                self.__num_keys += 1

                self.file_manager.save(self)
                self.file_manager.save(l_tree)
                self.file_manager.save(r_tree)
        else:
            subtree_to_insert = self.__node_caller.seek_node(subtree_num_page)
            if subtree_to_insert.can_insert():
                subtree_to_insert.insert(pk, username, email)
                self.file_manager.save(subtree_to_insert)
            else:
                l_tree, r_tree = subtree_to_insert.insert_and_split_for_parent(pk, username, email)
                del self.__children[subtree_key]
                self.__children[l_tree.last_key_record()] = l_tree.num_page
                self.__children[r_tree.last_key_record()] = r_tree.num_page
                self.__children = dict(sorted(self.__children.items()))
                self.__num_keys += 1

                self.file_manager.save(self)
                self.file_manager.save(l_tree)
                self.file_manager.save(r_tree)

        return self

    # ACCESSING

    def select_all(self):
        records = []
        children = list(self.__children.values())
        children.append(self.__right_child)

        for num_child_page in children:
            child = self.__node_caller.seek_node(num_child_page)
            records.extend(child.select_all())
        return records

    def num_keys(self):
        return self.__num_keys

    def count_metadata(self):
        num_records = 0
        num_pages = 1
        children = list(self.__children.values())
        children.append(self.__right_child)

        for num_child_page in children:
            child = self.__node_caller.seek_node(num_child_page)
            curr_num_pages, curr_num_rec = child.count_metadata()
            num_records += curr_num_rec
            num_pages += curr_num_pages

        return num_pages, num_records

    def right_child(self):
        return self.__right_child

    def children(self):
        return self.__children

    def can_insert(self):
        raise MethodNotImplemented()

    # PRIVATE ACCESSING

    def insert_and_split_for_parent(self, pk, username, email):
        raise MethodNotImplemented()

    def __find_subtree_can_contain(self, pk):
        keys = list(self.__children.keys())
        low, high = 0, len(keys) - 1
        mid = None
        while low <= high:
            mid = (low + high) // 2
            mid_key = keys[mid]
            if mid_key == pk:
                return mid_key

            if mid_key < pk:
                low = mid + 1
            else:
                high = mid - 1
        if low == len(keys) and pk > keys[-1]:
            return None, None
        else:
            return keys[mid], self.__children[keys[mid]]


##############################################################################################################


class NodeDecoder:

    def __init__(self, file_manager):
        self.__decoder = Decoder()
        self.__file_manager = file_manager

    def init_tree(self):
        node_bytes = self.__file_manager.get_bytes(0, 4096)
        return self.__parse_tree(node_bytes, 0)

    def create_tree(self):
        return Leaf(True, 0, 0, [], 0, self.__file_manager)

    def seek_node(self, num_page):
        fst_byte = num_page * 4096
        lst_byte = fst_byte + 4096
        data_bytes = self.__file_manager.get_bytes(fst_byte, lst_byte)

        return self.__parse_tree(data_bytes, num_page)

    def __get_records(self, data_bytes, num_records):
        records = []
        curr_record = 0

        while curr_record < num_records * 295:
            key_start_byte = curr_record
            value_last_byte = key_start_byte + 295

            records.append(self.__decoder.do(data_bytes[key_start_byte:value_last_byte]))

            curr_record += 295

        return records

    def __get_children_pointers(self, data_bytes, num_keys):
        records = dict()
        curr_record = 0

        while curr_record < num_keys * 8:
            key_start_byte = curr_record
            page_num_fst_byte = key_start_byte + 4
            page_num_last_byte = page_num_fst_byte + 4
            key = self.__decoder.decode_num_four_bytes(data_bytes[key_start_byte:page_num_fst_byte])
            value = self.__decoder.decode_num_four_bytes(data_bytes[page_num_fst_byte:page_num_last_byte])
            records[key] = value

            curr_record += 8
        return records

    def __parse_tree(self, node_bytes, num_page):
        is_leaf = node_bytes[0] == 1
        if is_leaf:
            is_root = node_bytes[1] == 1
            parent = int.from_bytes(node_bytes[2:6], byteorder='big') if not is_root else 0
            num_records = int.from_bytes(node_bytes[6:10], byteorder='big')

            if num_records > 0:
                records = self.__get_records(node_bytes[10:295 * num_records], num_records)
            else:
                records = []
            return Leaf(is_root, parent, num_records, records, num_page, self.__file_manager)
        else:
            is_root = node_bytes[1] == 1
            parent = int.from_bytes(node_bytes[2:6], byteorder='big') if not is_root else 0
            num_keys = int.from_bytes(node_bytes[6:10], byteorder='big')
            right_child = int.from_bytes(node_bytes[10:14], byteorder='big')

            if num_keys > 0:
                records = self.__get_children_pointers(node_bytes[14:14 + 8 * num_keys], num_keys)
            else:
                records = []

            return Internal(is_root, parent, num_keys, records, right_child, num_page, self.__file_manager)
