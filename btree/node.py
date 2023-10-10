from exceptions.duplicate_key import DuplicateKeyException
from exceptions.page_full import PageFullException
from exceptions.record_not_found import RecordNotFoundException

USERNAME = 0
EMAIL = 1


class Node:
    def __init__(self, is_leaf, is_root, parent, num_records, num_page, records, max_records=13):
        self.is_leaf = is_leaf
        self.is_root = is_root
        self.parent = parent
        self.num_records = num_records
        self.curr_records = records
        self.num_page = num_page
        self.subtrees: dict = {}  # TODO: persistir nueva data
        self.__max_records_amount = max_records
        self.__last_leaf = None

    # ACTIONS

    def insert(self, pk, username, email):

        if self.__contains(pk):
            raise DuplicateKeyException()
        if not self.is_leaf and len(self.subtrees) == self.__max_subtrees() and not self.__last_leaf[1].can_insert():
            raise PageFullException()

        if self.is_leaf:
            if self.num_records == self.__max_records_amount:
                self.__split_leaf(pk, username, email)
            else:
                self.__do_insert(pk, username, email)
                self.num_records += 1
        else:
            subtree_key_to_insert = self.__find_subtree_key_can_contain(pk)
            not_exist_tree = subtree_key_to_insert is None
            if not_exist_tree:
                self.__split_last_leaf_and_insert(email, pk, username)
            else:
                self.__find_and_split_subtree_inserting(email, pk, subtree_key_to_insert, username)
            self.num_records += 1

    def update_username(self, key, new_username):
        self.__find_record(key)[USERNAME] = new_username

    def update_email(self, key, new_email):
        self.__find_record(key)[EMAIL] = new_email

    def update_pk(self, key, new_key):
        if self.contains_record(new_key):
            raise DuplicateKeyException()
        record = self.__find_record(key)

        self.curr_records.remove(record)
        self.__do_insert(new_key, record[USERNAME], record[EMAIL])

    def insert_and_split_for_parent(self, pk, username, email):
        self.__do_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2 if (self.num_records + 1) // 2 > 0 else 1
        l_tree = Node(True, False, self.parent, num_records, self.num_page, self.curr_records[:num_records],
                      self.__max_records_amount)
        r_tree = Node(True, False, self.parent, num_records, self.num_page + 1, self.curr_records[num_records:],
                      self.__max_records_amount)
        return l_tree, r_tree

    # ACCESSING

    def get_record(self, key):
        return self.__find_record(key)

    def get_email(self, key):
        return self.__find_record(key)[EMAIL]

    def get_username(self, key):
        return self.__find_record(key)[USERNAME]

    def get_pk(self, key):
        self.__find_record(key)
        return key

    def obtain(self, i):
        return self

    def data(self):
        if self.is_leaf:
            return list(
                map(lambda record_kv: [record_kv[0], record_kv[1][USERNAME], record_kv[1][EMAIL]], self.curr_records))
        else:
            records = []
            for list_of_records in list(map(lambda node: node.data(), self.nodes_subtrees())):
                for record in list_of_records:
                    records.append(record)
            return records

    def count_pages(self):
        return 1 + len(self.nodes_subtrees())  # TODO: cambiar cuando haya split de nodos internos

    def count_records(self):
        if self.is_leaf:
            return self.num_records
        else:
            return sum(map(lambda node: node.count_records(), self.nodes_subtrees()))

    def records(self):
        return self.curr_records.copy()

    def fst_key(self):
        return self.curr_records[0][0] if len(self.curr_records) > 0 else 0

    def last_key(self):
        return self.curr_records[-1][0] if len(self.curr_records) > 0 else 0

    def nodes_subtrees(self):
        subtrees = list(self.subtrees.values())
        if self.__last_leaf is not None:
            subtrees.append(self.__last_leaf[1])
        return subtrees

    # TESTING

    def can_insert(self):
        return self.is_leaf and self.num_records < self.__max_records_amount

    def contains_record(self, key):
        return any(record[0] == key for record in self.curr_records)

    # PRIVATE ACTIONS

    def __find_and_split_subtree_inserting(self, email, pk, subtree_key_to_insert, username):
        subtree_to_insert = self.subtrees[subtree_key_to_insert]
        if subtree_to_insert.can_insert():
            subtree_to_insert.insert(pk, username, email)
        else:
            l_tree, r_tree = subtree_to_insert.insert_and_split_for_parent(pk, username, email)
            del self.subtrees[subtree_key_to_insert]
            self.subtrees[l_tree.last_key()] = l_tree
            self.subtrees[r_tree.fst_key()] = r_tree
            self.subtrees = dict(sorted(self.subtrees.items()))

    def __split_last_leaf_and_insert(self, email, pk, username):
        subtree_to_insert = self.__last_leaf[1]
        if subtree_to_insert.can_insert():
            subtree_to_insert.insert(pk, username, email)
        else:
            l_tree, r_tree = subtree_to_insert.insert_and_split_for_parent(pk, username, email)
            self.subtrees[l_tree.last_key()] = l_tree
            self.__last_leaf = [r_tree.fst_key(), r_tree]

    def __do_insert(self, pk, username, email):
        is_saved = False
        curr_record_index = 0

        while not is_saved and curr_record_index < self.num_records:
            if pk < self.curr_records[curr_record_index][0]:
                self.curr_records.insert(curr_record_index, [pk, [username, email]])
                is_saved = True
            curr_record_index += 1
        if not is_saved:
            self.curr_records.append([pk, [username, email]])

    def __split_leaf(self, pk, username, email):
        self.__do_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2
        l_tree = Node(True, False, self, num_records, self.num_page + 1, self.curr_records[:num_records],
                      self.__max_records_amount)
        r_tree = Node(True, False, self, num_records, self.num_page + 2, self.curr_records[num_records:],
                      self.__max_records_amount)
        self.subtrees[l_tree.last_key()] = l_tree
        self.__last_leaf = [r_tree.fst_key(), r_tree]
        self.is_leaf = False
        self.curr_records = []
        self.num_records = 2

    # PRIVATE ACCESSING

    def __find_record(self, key):
        record = next(filter(lambda record_kv: record_kv[0] == key, self.curr_records), None)

        if record is not None:
            return record[1]
        else:
            raise RecordNotFoundException()

    def __find_subtree_key_can_contain(self, pk):
        return next(filter(lambda subtree_key_reference:
                           pk < subtree_key_reference or self.__is_between_keys(subtree_key_reference, pk),
                           list(self.subtrees.keys())), None)

    @staticmethod
    def __max_subtrees():
        return 510

    # PRIVATE TESTING

    def __contains(self, key):
        if self.is_leaf:
            return self.contains_record(key)
        else:
            maybe_key_subtree = self.__find_subtree_key_can_contain(key)
            if maybe_key_subtree is None:
                return self.__last_leaf[1].contains_record(key)
            else:
                return self.subtrees[maybe_key_subtree].contains_record(key)

    def __is_between_keys(self, subtree_key_reference, key):
        sorted_keys = sorted(self.subtrees.keys())
        index = sorted_keys.index(subtree_key_reference)
        if index + 1 < len(sorted_keys):
            return subtree_key_reference <= key < sorted_keys[index + 1]
        else:
            return False
