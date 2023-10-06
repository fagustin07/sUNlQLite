from modules.exceptions.duplicate_key import DuplicateKeyException
from modules.exceptions.page_full import PageFullException
from modules.exceptions.record_not_found import RecordNotFoundException


USERNAME = 0
EMAIL = 1


class Node:
    def __init__(self, is_leaf, is_root, parent, num_records, num_page, records):
        self.is_leaf = is_leaf
        self.is_root = is_root
        self.parent = parent
        self.num_records = num_records
        self.__records = records
        self.num_page = num_page

    # ACTIONS
    def insert(self, pk, username, email):

        if self.__contains(pk):
            raise DuplicateKeyException()

        if self.num_records == 13:
            raise PageFullException()
        is_saved = False
        curr_record_index = 0

        while not is_saved and curr_record_index < self.num_records:
            if pk < self.__records[curr_record_index][0]:
                self.__records.insert(curr_record_index, [pk, [username, email]])
                is_saved = True
            curr_record_index += 1
        if not is_saved:
            self.__records.append([pk, [username, email]])
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
        self.__records -= 1

        self.insert(new_key, record[USERNAME], record[EMAIL])

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
        return list(map(lambda record_kv:
                        [record_kv[0], record_kv[1][USERNAME], record_kv[1][EMAIL]],
                        self.__records)) if self.is_leaf else []

    @staticmethod
    def count_pages():
        return 1

    def count_records(self):
        return self.num_records if self.is_root or self.is_leaf else 0

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
