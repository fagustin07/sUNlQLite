from modules.decoder import Decoder


class Page:
    def __init__(self):
        self.records = bytearray(self.__max_bytes())
        self.amount_record = 0
        self.decoder = Decoder()

    def can_insert_record(self):
        return (self.__max_bytes() - self.__next_byte()) > 0

    def insert(self, record):
        self.records[self.__next_byte():self.__next_byte() + self.record_size()] = record
        self.amount_record += 1

    def select(self):
        if self.amount_record == 0:
            return []
        curr_record = 0
        records = []
        while curr_record < self.amount_record:
            start_record_byte = self.record_size() * curr_record
            end_record_byte = self.record_size() * curr_record + self.record_size()
            record = self.decoder.do(self.records[start_record_byte:end_record_byte])

            records.append(record)

            curr_record += 1

        return records

    # PRIVATE
    def __next_byte(self):
        return self.amount_record * 291

    @staticmethod
    def __max_bytes():
        return 4096

    @staticmethod
    def record_size():
        return 291
