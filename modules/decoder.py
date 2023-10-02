class Decoder:
    def do(self, record_kv: bytearray):
        record = record_kv[1]
        id_bytes = list(record[:4])
        user_bytes = bytes(list(record[4:36]))
        email_bytes = bytes(list(record[36:]))

        pk = int.from_bytes(id_bytes, byteorder='big')
        user = self.bytes_to_string(user_bytes)
        email = self.bytes_to_string(email_bytes)
        return pk, user, email

    @staticmethod
    def bytes_to_string(desired_bytes):
        return ''.join(char for char in desired_bytes.decode('ascii', errors='ignore') if char != '\0')

    @staticmethod
    def bytes_to_int(desired_bytearray):
        return int.from_bytes(desired_bytearray, byteorder='big')
