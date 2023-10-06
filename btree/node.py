from exceptions.duplicate_key import DuplicateKeyException
from exceptions.record_not_found import RecordNotFoundException

USERNAME = 0
EMAIL = 1


class Node:
    def __init__(self, is_leaf, is_root, parent, num_records, num_page, records, max_records=13):
        self.is_leaf = is_leaf
        self.is_root = is_root
        self.parent = parent
        self.num_records = num_records
        self.__records = records
        self.num_page = num_page
        self.subtrees: dict = {}
        self.__max_records_amount = max_records
        self.__last_leaf = None

    # ACTIONS
    def insert(self, pk, username, email):

        if self.__contains(pk):
            raise DuplicateKeyException()

        if self.num_records == self.__max_records_amount:
            self.__split_leaf(pk, username, email)
        else:
            self.__do_insert(pk, username, email)
            self.num_records += 1

    def update_username(self, key, new_username):
        self.__find_record(key)[USERNAME] = new_username

    def update_email(self, key, new_email):
        self.__find_record(key)[EMAIL] = new_email

    def update_pk(self, key, new_key):
        if self.__contains(new_key):
            raise DuplicateKeyException()
        record = self.__find_record(key)

        self.__records.remove(record)
        self.__do_insert(new_key, record[USERNAME], record[EMAIL])

    # ACCESING
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
            return list(map(lambda record_kv: [record_kv[0], record_kv[1][USERNAME], record_kv[1][EMAIL]], self.__records))
        else:
            records = []
            for list_of_records in list(map(lambda node: node.data(), self.__subtrees())):
                for record in list_of_records:
                    records.append(record)
            return records

    @staticmethod
    def count_pages():
        return 1

    def count_records(self):
        if self.is_leaf:
            return self.num_records
        else:
            return sum(map(lambda node: node.count_records(), self.__subtrees()))

    def records(self):
        return self.__records.copy()

    def __find_record(self, key):
        record = next(filter(lambda record_kv: record_kv[0] == key, self.__records), None)

        if record is not None:
            return record[1]
        else:
            raise RecordNotFoundException()

    # TESTING
    def __contains(self, key):
        return key in map(lambda kv: kv[0], self.__records)

    def __split_leaf(self, pk, username, email):
        self.__do_insert(pk, username, email)
        num_records = (self.num_records + 1) // 2
        l_tree = Node(True, False, self, num_records, self.num_page + 1, self.__records[:num_records], self.__max_records_amount)
        r_tree = Node(True, False, self, num_records, self.num_page + 2, self.__records[num_records:], self.__max_records_amount)
        self.subtrees[l_tree.last_key()] = l_tree
        self.__last_leaf = [r_tree.last_key(), r_tree]
        self.is_leaf = False
        self.__records = []
        self.num_records = 0

    def __do_insert(self, pk, username, email):
        is_saved = False
        curr_record_index = 0

        while not is_saved and curr_record_index < self.num_records:
            if pk < self.__records[curr_record_index][0]:
                self.__records.insert(curr_record_index, [pk, [username, email]])
                is_saved = True
            curr_record_index += 1
        if not is_saved:
            self.__records.append([pk, [username, email]])

    def last_key(self):
        return self.__records[-1][0] if len(self.__records) > 0 else 0

    def __subtrees(self):
        subtrees = list(self.subtrees.values())
        subtrees.append(self.__last_leaf[1])
        return subtrees
