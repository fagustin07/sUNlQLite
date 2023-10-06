from utils.decoder import Decoder
from btree.node import Node


class NodeInstanciator:

    def __init__(self):
        self.__decoder = Decoder()

    def init_tree(self, node_bytes):
        is_leaf = node_bytes[0] == 0
        is_root = node_bytes[1] == 0
        parent = int.from_bytes(node_bytes[2:6], byteorder='big') if int.from_bytes(node_bytes[2:6],
                                                                                    byteorder='big') > 0 else None
        num_records = int.from_bytes(node_bytes[6:10], byteorder='big')

        if num_records > 0:
            records = self.get_records(node_bytes[10:295 * num_records], num_records)
        else:
            records = []

        return Node(is_leaf=is_leaf,
                    is_root=is_root,
                    parent=parent,
                    num_records=num_records,
                    records=records,
                    num_page=1)

    @staticmethod
    def create_tree():
        return Node(True, True, None, 0, 1, [])

    def get_records(self, data_bytes, num_records):
        records = []
        curr_record = 0

        while curr_record < num_records * 295:
            key_start_byte = curr_record
            value_last_byte = key_start_byte + 295

            records.append(self.__decoder.do(data_bytes[key_start_byte:value_last_byte]))

            curr_record += 295

        return records
