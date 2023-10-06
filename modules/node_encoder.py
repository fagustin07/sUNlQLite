from modules.encoder import Encoder


class NodeEncoder:

    def __init__(self):
        self.__encoder = Encoder()

    def do(self, page_node):
        data = bytearray(4096)

        data[0:0] = (0).to_bytes(1, byteorder='big') if page_node.is_leaf else (1).to_bytes(1, byteorder='big')
        data[1:1] = (0).to_bytes(1, byteorder='big') if page_node.is_root else (1).to_bytes(1, byteorder='big')
        data[2:6] = page_node.parent.to_bytes(4, byteorder='big') if not page_node.is_root else (0).to_bytes(4, byteorder='big')
        data[6:10] = page_node.num_records.to_bytes(4, byteorder='big')
        curr_byte = 10
        for record_kv in page_node.records():
            fst_byte = curr_byte
            lst_byte = fst_byte + 295
            data[fst_byte:lst_byte] = self.__encoder.do(record_kv)
            curr_byte += 295
        return data
