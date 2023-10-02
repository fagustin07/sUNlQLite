from modules.node import Node


class NodeInstanciator:

    def init_tree(self, node_bytes):
        is_leaf = node_bytes[0] == 0
        is_root = node_bytes[1] == 0
        parent = int.from_bytes(node_bytes[2:6])
        num_records = int.from_bytes(node_bytes[6:10])

        if num_records > 0:
            records = self.get_records(node_bytes[10:295 * num_records], num_records)
        else:
            records = []

        return Node(is_leaf=is_leaf,
                    is_root=is_root,
                    parent=parent,
                    num_records=num_records,
                    records=records)

    @staticmethod
    def create_tree():
        return Node(True, True, None, 0, [])

    @staticmethod
    def get_records(bytes, num_records):
        records = []
        curr_record = 0

        while curr_record > num_records*295:
            key_start_byte = curr_record
            value_start_byte = curr_record+4
            value_last_byte = value_start_byte + 291

            key = bytes[key_start_byte:value_start_byte]
            value = bytes[value_start_byte:value_last_byte]
            records.append([key, value])

            curr_record += 295
        return records


