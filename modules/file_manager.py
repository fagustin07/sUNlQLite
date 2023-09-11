class FileManager:

    def __init__(self, filename):
        self.filename = filename

    def get_metadata(self):
        with open(self.filename, 'rb') as file:
            data = file.read()
            file_size = len(data)
            if file_size == 0:
                return 1, 0

            tuple_amount_pages_records = divmod(file_size, 4096)
            if tuple_amount_pages_records[1] == 0:
                amount_pages = tuple_amount_pages_records[0]
                amount_records = amount_pages * 14
            else:
                amount_pages = tuple_amount_pages_records[0] + 1
                amount_records = tuple_amount_pages_records[0] * 14 + divmod(tuple_amount_pages_records[1], 291)[0]
        print(file_size)
        print(tuple_amount_pages_records)

        print(amount_pages, amount_records)
        return amount_pages, amount_records

    def get_data(self, since, to):
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
