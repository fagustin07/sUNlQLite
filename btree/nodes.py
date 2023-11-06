import bisect

from btree.abstract_node import AbstractNode
from exceptions.duplicate_key import DuplicateKeyException
from utils.decoder import Decoder
from utils.file_manager import FileManager


class Leaf(AbstractNode):

    def __init__(self, is_root: bool, parent: int, num_records: int, pointer_records: list, num_page: int,
                 file_manager: FileManager, node_decoder):
        super().__init__(is_root, parent, num_page, file_manager, node_decoder)
        self.is_leaf = True
        self.num_records = num_records
        self.records = pointer_records

    # ACTIONS

    def insert(self, pk, username, email):
        if self.num_records == self.node_caller.max_num_records():
            return self.__split_leaf(pk, username, email)
        else:
            self.__do_binary_insert(pk, username, email)
            self.num_records += 1
            self.file_manager.save(self)
            return self

    def insert_and_split_for_parent(self, pk, username, email):
        self.__do_binary_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2
        l_records = self.records[:num_records]
        r_records = self.records[num_records:]
        l_tree = Leaf(False, self.parent, len(l_records), l_records,
                      self.num_page, self.file_manager, self.node_caller)
        r_tree = Leaf(False, self.parent, len(r_records), r_records,
                      self.file_manager.next_num_page(), self.file_manager, self.node_caller)

        parent: Internal = self.node_caller.seek_node(self.parent)
        parent.check_internal_split(self, l_tree, r_tree)

    # ACCESSING

    def select_all(self):
        return list(map(lambda record_kv: [record_kv[0], record_kv[1][0], record_kv[1][1]], self.records))

    def count_metadata(self):
        return 1, self.num_records

    def last_key_record(self):
        return self.records[-1][0]

    # TESTING

    def can_insert(self, pk):
        return self.num_records < self.node_caller.max_num_records()

    # PRIVATE ACTIONS

    def __split_leaf(self, pk, username, email):
        self.__do_binary_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2

        l_records = self.records[:num_records]
        r_records = self.records[num_records:]
        l_tree = Leaf(False, self.num_page, len(l_records), l_records,
                      self.file_manager.next_num_page(), self.file_manager, self.node_caller.max_num_records())
        self.file_manager.save(l_tree)

        r_tree = Leaf(False, self.num_page, len(r_records), r_records,
                      self.file_manager.next_num_page(), self.file_manager, self.node_caller.max_num_records())

        base_node = Internal(self.is_root, self.parent, 1,
                             dict({l_tree.last_key_record(): l_tree.num_page}),
                             r_tree.num_page, self.num_page, self.file_manager, self.node_caller)

        self.file_manager.save(r_tree, base_node)

        return base_node

    def __do_binary_insert(self, pk, username, email):
        clave_nuevo_registro = pk

        # Búsqueda binaria para encontrar la posición
        izquierda, derecha = 0, len(self.records) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            clave_actual = self.records[medio][0]

            if clave_actual == clave_nuevo_registro:
                raise DuplicateKeyException()
            elif clave_actual < clave_nuevo_registro:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        self.records.insert(izquierda, [pk, [username, email]])

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
                 file_manager: FileManager, node_decoder):
        super().__init__(is_root, parent, num_page, file_manager, node_decoder)
        self.__num_keys = num_keys
        self.__children = children
        self.__right_child = right_child

    # ACTIONS

    def insert(self, pk, username, email):
        subtree_key, subtree_num_page = self.search_subtree_can_contain(pk)
        not_exist_tree = subtree_num_page is None

        if not_exist_tree:
            subtree_to_insert = self.find_right_child_can_contain(pk)

            if subtree_to_insert.can_insert(pk):
                subtree_to_insert.insert(pk, username, email)
                self.file_manager.save(subtree_to_insert)
            else:
                subtree_to_insert.insert_and_split_for_parent(pk, username, email)

        else:
            subtree_to_insert = self.node_caller.seek_node(subtree_num_page)
            if subtree_to_insert.can_insert(pk):
                subtree_to_insert.insert(pk, username, email)
                self.file_manager.save(subtree_to_insert)
            else:
                subtree_to_insert.insert_and_split_for_parent(pk, username, email)

        return self.node_caller.seek_node(0)

    def check_internal_split(self, old_child, l_tree, r_tree):
        key = None
        for k, v in self.__children.items():
            if v == old_child.num_page:
                key = k
                break
        if key is None:
            self.__children[l_tree.last_key_record()] = l_tree.num_page
            self.__right_child = r_tree.num_page
            self.__children = dict(sorted(self.__children.items()))
        else:
            del self.__children[key]
            self.__children[l_tree.last_key_record()] = l_tree.num_page
            self.__children[r_tree.last_key_record()] = r_tree.num_page
            self.__children = dict(sorted(self.__children.items()))

        self.__num_keys += 1
        self.file_manager.save(l_tree, r_tree)
        if self.__num_keys == self.node_caller.max_num_pages():
            right_child = self.node_caller.seek_node(self.__right_child)
            self.__children[right_child.last_key_record()] = right_child.num_page
            self.__num_keys += 1
            if self.is_root:
                self.__split_internal_root()
            else:
                self.__split_internals_parent()
        else:
            self.file_manager.save(self)

    def change_children_pointer(self):
        childrens = list(self.__children.values())
        childrens.append(self.right_child())
        for num_page in childrens:
            page = self.node_caller.seek_node(num_page)
            page.change_parent_to(self)

    def select_all(self):
        records = []
        children = list(self.__children.values())
        children.append(self.__right_child)

        for num_child_page in children:
            child = self.node_caller.seek_node(num_child_page)
            records.extend(child.select_all())
        return records

    def change_splitted_child_reference(self, old_child, l_child, r_child, left_ref, right_ref):
        key = None
        for k, v in self.__children.items():
            if v == old_child.num_page:
                key = k
                break

        if key is not None:
            del self.__children[key]
            self.__children[left_ref] = l_child.num_page
            self.__children[right_ref] = r_child.num_page
        else:
            self.__children[left_ref] = l_child.num_page
            self.__right_child = r_child.num_page

        self.__children = dict(sorted(self.__children.items()))
        self.__num_keys += 1

        if self.__num_keys == self.node_caller.max_num_records():
            if self.is_root:
                self.__split_internal_root()
            else:
                self.__split_internals_parent()
        else:
            self.file_manager.save(self)

    # ACCESSING

    def can_insert(self, pk):
        _, subtree_num_page = self.search_subtree_can_contain(pk)
        if subtree_num_page is None:
            node = self.node_caller.seek_node(self.__right_child).can_insert(pk)
            return node.can_insert(pk)
        else:
            return self.node_caller.seek_node(subtree_num_page).can_insert(pk)

    def count_metadata(self):
        num_records = 0
        num_pages = 1
        children = list(self.__children.values())
        children.append(self.__right_child)

        for num_child_page in children:
            child = self.node_caller.seek_node(num_child_page)
            curr_num_pages, curr_num_rec = child.count_metadata()
            num_records += curr_num_rec
            num_pages += curr_num_pages

        return num_pages, num_records

    def num_keys(self):
        return self.__num_keys

    def right_child(self):
        return self.__right_child

    def children(self):
        return self.__children

    def search_subtree_can_contain(self, pk):
        subtree_key, subtree_num_page = self.find_subtree_can_contain(pk)
        if subtree_num_page is not None:
            node = self.node_caller.seek_node(subtree_num_page)
            if node.is_leaf:
                return subtree_key, subtree_num_page
            else:
                return node.search_subtree_can_contain(pk)
        else:
            node = self.node_caller.seek_node(self.right_child())
            if node.is_leaf:
                return subtree_key, subtree_num_page
            else:
                return node.search_subtree_can_contain(pk)

    def find_right_child_can_contain(self, pk):
        node = self.node_caller.seek_node(self.right_child())
        if node.is_leaf:
            return node
        else:
            key, num_page = node.search_subtree_can_contain(pk)
            if num_page is None:
                new_node = self.node_caller.seek_node(node.right_child())
                if new_node.is_leaf:
                    return new_node
                else:
                    return new_node.find_right_child_can_contain(pk)
            else:
                new_node = self.node_caller.seek_node(num_page)
                if new_node.is_leaf:
                    return new_node
                else:
                    return new_node.find_right_child_can_contain(pk)

    # PRIVATE ACCESSING

    def find_subtree_can_contain(self, pk):
        keys = list(self.__children.keys())
        index = bisect.bisect_left(keys, pk)

        if index < len(keys) and keys[index] == pk:
            raise DuplicateKeyException()
        elif index < len(keys):
            return keys[index], self.__children[keys[index]]
        else:
            return None, None

    # PRIVATE ACTIONS

    def __split_dicts(self):
        sort = dict(sorted(self.__children.items()))
        claves = list(sort.keys())
        valores = list(sort.values())

        punto_medio = len(claves) // 2

        claves_1 = claves[:punto_medio]
        valores_1 = valores[:punto_medio]
        claves_2 = claves[punto_medio:]
        valores_2 = valores[punto_medio:]

        diccionario_1 = {clave: valor for clave, valor in zip(claves_1, valores_1)}
        diccionario_2 = {clave: valor for clave, valor in zip(claves_2, valores_2)}

        left_new_ref, right_new_ref = claves_1[-1], claves_2[-1]
        left_last_page, right_last_page = valores_1[-1], valores_2[-1]

        return diccionario_1, diccionario_2, left_new_ref, right_new_ref, left_last_page, right_last_page, len(
            claves_1), len(claves_2)

    def __split_internal_root(self):
        dict_left, dict_right, left_ref, right_ref, l_page, r_page, l_size, r_size = self.__split_dicts()
        del dict_left[left_ref]
        del dict_right[right_ref]
        l_child = Internal(False, self.num_page, l_size - 1, dict_left, l_page,
                           self.file_manager.next_num_page(),
                           self.file_manager, self.node_caller)
        self.file_manager.save(l_child)
        r_child = Internal(False, self.num_page, r_size - 1, dict_right, r_page,
                           self.file_manager.next_num_page(),
                           self.file_manager, self.node_caller)
        self.file_manager.save(r_child)
        self.__num_keys = 1
        self.__children = dict({left_ref: l_child.num_page})
        self.__right_child = r_child.num_page
        l_child.change_children_pointer()
        r_child.change_children_pointer()
        self.file_manager.save(self)

    def __split_internals_parent(self):
        dict_left, dict_right, left_ref, right_ref, l_page, r_page, l_size, r_size = self.__split_dicts()
        del dict_left[left_ref]
        del dict_right[right_ref]
        l_child = Internal(False, self.parent, l_size - 1, dict_left, l_page,
                           self.num_page,
                           self.file_manager, self.node_caller)
        self.file_manager.save(l_child)
        r_child = Internal(False, self.parent, r_size - 1, dict_right, r_page,
                           self.file_manager.next_num_page(),
                           self.file_manager, self.node_caller)
        self.file_manager.save(r_child)
        l_child.change_children_pointer()
        r_child.change_children_pointer()
        parent_node: Internal = self.node_caller.seek_node(self.parent)
        parent_node.change_splitted_child_reference(self, l_child, r_child, left_ref, right_ref)

##############################################################################################################


class NodeDecoder:

    def __init__(self, file_manager, max_rec=13, max_pages=510):
        self.__decoder = Decoder()
        self.__file_manager = file_manager
        self.__max_records = max_rec
        self.__max_pages = max_pages

    def init_tree(self):
        node_bytes = self.__file_manager.get_bytes(0, 4096)
        return self.__parse_tree(node_bytes, 0)

    def create_tree(self):
        return Leaf(True, 0, 0, [], 0, self.__file_manager, self)

    def seek_node(self, num_page):
        fst_byte = num_page * 4096
        lst_byte = fst_byte + 4096
        data_bytes = self.__file_manager.get_bytes(fst_byte, lst_byte)

        return self.__parse_tree(data_bytes, num_page)

    def max_num_records(self):
        return self.__max_records

    def max_num_pages(self):
        return self.__max_pages

    def __get_records(self, data_bytes, num_records):
        records = []
        curr_record = 0
        decoder = self.__decoder
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
            return Leaf(is_root, parent, num_records, records, num_page, self.__file_manager, self)
        else:
            is_root = node_bytes[1] == 1
            parent = int.from_bytes(node_bytes[2:6], byteorder='big') if not is_root else 0
            num_keys = int.from_bytes(node_bytes[6:10], byteorder='big')
            right_child = int.from_bytes(node_bytes[10:14], byteorder='big')

            if num_keys > 0:
                records = self.__get_children_pointers(node_bytes[14:14 + 8 * num_keys], num_keys)
            else:
                records = {}

            return Internal(is_root, parent, num_keys, records, right_child, num_page, self.__file_manager, self)
