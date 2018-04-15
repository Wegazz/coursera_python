class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        read = ''
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                read = file.read()
        except IOError as e:
            print(e)
        return read


if __name__ == '__main__':
    reader = FileReader("example.txt")
    print(reader.read())
