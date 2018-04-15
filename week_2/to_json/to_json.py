import functools
import json


def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result, ensure_ascii=False)

    return wrapped


@to_json
def get_data():
    return {
        'data': 42,
        'ololo': [1, 2, 3]
    }


if __name__ == '__main__':
    print(get_data())
