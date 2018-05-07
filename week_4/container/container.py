class Container:
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return str(self.data)


if __name__ == '__main__':
    a = Container()
    b = Container()

    a['heh'] = 'hehe'
    b['kek'] = 'keke'

    print(f'a: {a}')
    print(f'b: {b}')
