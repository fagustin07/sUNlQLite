class NodeEncoder:

    @staticmethod
    def do(page_node):
        data = bytearray(4096)

        data[0:0] = (0).to_bytes(1, byteorder='big') if page_node.is_leaf else (1).to_bytes(1, byteorder='big')
        data[1:1] = (0).to_bytes(1, byteorder='big') if page_node.is_root else (1).to_bytes(1, byteorder='big')
        data[2:6] = page_node.parent.to_bytes(4, byteorder='big') if not page_node.is_root else (0).to_bytes(4, byteorder='big')
        data[6:10] = page_node.num_records.to_bytes(4, byteorder='big')
        curr_byte = 10
        for record_kv in page_node.records():
            fst_key_byte = curr_byte
            fst_value_byte = curr_byte+4
            lst_value_byte = fst_value_byte + 291
            data[fst_key_byte:fst_value_byte] = record_kv[0].to_bytes(4, byteorder='big')
            data[fst_value_byte:lst_value_byte] = record_kv[1]
            curr_byte += 295
        return data
