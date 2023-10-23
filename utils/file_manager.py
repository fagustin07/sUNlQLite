class FileManager:

    def __init__(self, filename, node_encoder):
        self.filename = filename
        self.__node_encoder = node_encoder

    def save(self, *nodes):
        with open(self.filename, 'r+b') as file:
            for node in nodes:
                self.__save(node, file)

    def next_num_page(self):
        with open(self.filename, 'rb') as file:
            return len(file.read()) // 4096

    def get_bytes(self, since, to):
        with open(self.filename, 'rb') as file:
            bytedata = bytearray(file.read())
            return bytedata[since:to]

    def file_size(self):
        with open(self.filename, 'rb') as file:
            data = file.read()

        return len(data)

    def commit(self, data):
        with open(self.filename, 'wb') as file:
            file.write(data)

    def file(self):
        with open(self.filename, 'rb') as file:
            bytedata = bytearray(file.read())
            return bytedata

    # PRIVATE ACTIONS

    def __save(self, node, file):
        file.seek(node.num_page*4096)
        file.write(self.__node_encoder.do(node))
