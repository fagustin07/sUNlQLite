class Encoder:
    @staticmethod
    def do(pk, username, email):
        registro_codificado = bytearray(291)

        id_bytes = pk.to_bytes(4, byteorder='big')
        registro_codificado[:4] = id_bytes

        usuario_encoded = username.encode('ascii')
        registro_codificado[4:36] = usuario_encoded.ljust(32, b'\x00')

        email_encoded = email.encode('ascii')
        registro_codificado[36:291] = email_encoded.ljust(255, b'\x00')

        return registro_codificado

