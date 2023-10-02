class Encoder:
    @staticmethod
    def do(pk, username, email):
        codified_record = bytearray(291)

        id_bytes = pk.to_bytes(4, byteorder='big')
        codified_record[:4] = id_bytes

        username_encoded = username.encode('ascii')
        codified_record[4:36] = username_encoded.ljust(32, b'\x00')

        email_encoded = email.encode('ascii')
        codified_record[36:291] = email_encoded.ljust(255, b'\x00')

        return codified_record

    def username_to_bytes(self, username):
        data = bytearray(32)
        data[0:32] = username.encode('ascii').ljust(32, b'\x00')
        return data

    def email_to_bytes(self, email):
        data = bytearray(32)
        data[0:255] = email.encode('ascii').ljust(255, b'\x00')
        return data
