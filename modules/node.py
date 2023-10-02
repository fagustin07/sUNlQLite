from modules.decoder import Decoder
from modules.page_full_exception import PageFullException


class Node:
    def __init__(self, is_leaf, is_root, parent, num_records, records):
        self.is_leaf = is_leaf
        self.is_root = is_root
        self.parent = parent
        self.num_records = num_records
        self.__records = records
        self.__decoder = Decoder()

    # ACTIONS
    def insert(self, data):
        if self.num_records == 13:
            raise PageFullException()
        new_key = self.__decoder.bytes_to_int(list(data[:4]))
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

    # ACCESING
    # TODO: como iterar sobre la estructura actual?
    def obtain(self, i):
        return self

    def data(self):
        return list(map(lambda record_kv: self.__decoder.do(record_kv), self.__records)) if self.is_leaf else None

    def count_pages(self):
        return 1

    def count_records(self):
        return self.num_records if self.is_root or self.is_leaf else 0
