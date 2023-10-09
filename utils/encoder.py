from btree.node import USERNAME, EMAIL


class Encoder:
    @staticmethod
    def do(record_kv):
        pk = record_kv[0]
        username = record_kv[1][USERNAME]
        email = record_kv[1][EMAIL]
        codified_record = bytearray(295)

        key_record_bytes = pk.to_bytes(4, byteorder='big')
        codified_record[:4] = key_record_bytes

        id_bytes = pk.to_bytes(4, byteorder='big')
        codified_record[4:8] = id_bytes

        username_encoded = username.encode('ascii')
        codified_record[8:40] = username_encoded.ljust(32, b'\x00')

        email_encoded = email.encode('ascii')
        codified_record[40:295] = email_encoded.ljust(255, b'\x00')

        return codified_record
