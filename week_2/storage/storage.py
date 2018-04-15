import argparse
import json
import os
import tempfile


class DataManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.storage = dict()
        self.load()

    def load(self):
        if os.path.isfile(self.file_name) and os.path.getsize(self.file_name) > 0:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                self.storage = json.load(file)

    def save(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self.storage, file, indent=True, ensure_ascii=False)

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __contains__(self, key):
        return key in self.storage


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Key-value storage')
    parser.add_argument('--key', type=str, help='KEY you wanted')
    parser.add_argument('--val', help='value to be set for KEY')
    parser.add_argument('--file', type=str, help='storage file name')
    args = parser.parse_args()

    data = DataManager(args.file or os.path.join(tempfile.gettempdir(), 'storage.data'))

    if args.key is not None:
        # Set value
        if args.val is not None:
            if args.key not in data:
                data[args.key] = list()
            data[args.key].append(args.val)
            data.save()
        # Get value
        else:
            if args.key in data:
                print(', '.join(data[args.key]))
