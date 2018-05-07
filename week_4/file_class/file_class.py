import tempfile


class File:
    def __init__(self, path, mode=None):
        self.path = path
        self.file = open(self.path, mode or 'w+', encoding='utf-8')

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def __add__(self, other):
        obj = File(tempfile.mktemp())
        with open(self.path, 'r', encoding='utf-8') as f1:
            obj.write(f1.read())
        with open(other.path, 'r', encoding='utf-8') as f2:
            obj.write(f2.read())
        return obj

    def __iter__(self):
        return iter(self.file)

    def __next__(self):
        return next(self.file)

    def __str__(self):
        return self.path

    def write(self, data):
        self.file.write(data)

    def cat(self):
        self.file.seek(0)
        return self.file.read()


if __name__ == '__main__':
    a = File(tempfile.mktemp())
    b = File(tempfile.mktemp())

    a.write('I am a!\n')
    b.write('I am b!\n')
    print(f'--- 1. a is {a}:\n{a.cat()}')
    print(f'--- 2. b is {b}:\n{b.cat()}')

    c = a + b
    c.write('No, I am c!\n')
    print(f'--- 3. c is {c}:\n{c.cat()}')

    c.write('I am 4 row!\n')
    c.write('I am 5 row!\n')
    c.write('I am 6 row!\n')
    c.file.seek(0)
    print('--- 4. File listing:')
    for i, line in enumerate(c, start=1):
        print(i, '|', line, end='')
