from modules.decoder import Decoder
from modules.encoder import Encoder
from modules.exceptions.duplicate_key import DuplicateKeyException
from modules.exceptions.page_full import PageFullException
from modules.exceptions.record_not_found import RecordNotFoundException


class Node:
    # TODO: como iterar sobre la estructura actual?
    def __init__(self, is_leaf, is_root, parent, num_records, records):
        self.is_leaf = is_leaf
        self.is_root = is_root
        self.parent = parent
        self.num_records = num_records
        self.__records = records
        self.__decoder = Decoder()
        self.__encoder = Encoder()

    # ACTIONS
    def insert(self, data):
        new_key = self.__decoder.bytes_to_int(list(data[:4]))

        if self.__contains(new_key):
            raise DuplicateKeyException()

        if self.num_records == 13:
            raise PageFullException()
        is_saved = False
        curr_record_index = 0

        while not is_saved and curr_record_index < self.num_records:
            if new_key < self.__records[curr_record_index][0]:
                self.__records.insert(curr_record_index, [new_key, data])
                is_saved = True
            curr_record_index += 1
        if not is_saved:
            self.__records.append([new_key, data])
        self.num_records += 1

    def update_username(self, key, new_username):
        self.__find_record(key)[4:36] = self.__encoder.username_to_bytes(new_username)

    def update_email(self, key, new_email):
        self.__find_record(key)[36:291] = self.__encoder.email_to_bytes(new_email)

    def update_pk(self, key, new_key):
        if self.__contains(new_key):
            raise DuplicateKeyException()
        record = self.__find_record(key)
        self.__records.remove(record)
        self.__records -= 1

        record[1][0:4] = new_key.to_bytes(4, byteorder='big')
        self.insert(record[1])

    # ACCESING
    def get_record(self, key):
        return self.__decoder.do(self.__find_record(key))

    def get_email(self, key):
        return self.__decoder.do(self.__find_record(key))[2]

    def get_username(self, key):
        return self.__decoder.do(self.__find_record(key))[1]

    def get_pk(self, key):
        return self.__decoder.do(self.__find_record(key))[0]

    def obtain(self, i):
        return self

    def data(self):
        return list(map(lambda record_kv: self.__decoder.do(record_kv), self.__records)) if self.is_leaf else None

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
            return record
        else:
            raise RecordNotFoundException()

    # TESTING
    def __contains(self, key):
        return key in map(lambda kv: kv[0], self.__records)
