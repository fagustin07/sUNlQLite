from btree.nodes import Internal, Leaf
from utils.encoder import Encoder


class NodeEncoder:

    def __init__(self):
        self.__encoder = Encoder()

    def do(self, page_node):
        if page_node.is_leaf:
            return self.__encode_leaf(page_node)
        else:
            return self.__encode_internal(page_node)

    def __encode_leaf(self, leaf: Leaf):
        data = bytearray(4096)
        data[0:0] = (1).to_bytes(1, byteorder='big')
        data[1:1] = (1).to_bytes(1, byteorder='big') if leaf.is_root else (0).to_bytes(1, byteorder='big')
        data[2:6] = leaf.parent.to_bytes(4, byteorder='big') if not leaf.is_root else (0).to_bytes(4, byteorder='big')
        data[6:10] = leaf.num_records.to_bytes(4, byteorder='big')
        curr_byte = 10

        for record_kv in leaf.records:
            fst_byte = curr_byte
            lst_byte = fst_byte + 295
            data[fst_byte:lst_byte] = self.__encoder.do(record_kv)
            curr_byte += 295

        return data[0:4096]

    def __encode_internal(self, internal: Internal):
        data = bytearray(4096)
        data[0:0] = (0).to_bytes(1, byteorder='big')
        data[1:1] = (1).to_bytes(1, byteorder='big') if internal.is_root else (0).to_bytes(1, byteorder='big')
        data[2:6] = internal.parent.to_bytes(4, byteorder='big') if not internal.is_root else (0).to_bytes(4, byteorder='big')
        data[6:10] = internal.num_keys().to_bytes(4, byteorder='big')
        data[10:14] = internal.right_child().to_bytes(4, byteorder='big')

        curr_byte = 14
        for record_kv in internal.children().items():
            fst_byte_key = curr_byte
            lst_byte_key = fst_byte_key + 4
            fst_byte_value = lst_byte_key
            lst_byte_value = fst_byte_value + 4
            data[fst_byte_key:lst_byte_key] = record_kv[0].to_bytes(4, byteorder='big')
            data[fst_byte_value:lst_byte_value] = record_kv[1].to_bytes(4, byteorder='big')
            curr_byte += 8

        return data[0:4096]
