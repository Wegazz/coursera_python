import socket
import time
from operator import itemgetter


class Client:
    RECV_BUFFER_SIZE = 1024

    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def put(self, key, value, timestamp=None):
        byte_buffer = b''
        try:
            self.sock.sendall('put {key} {value} {timestamp}\n'
                              .format(key=key, value=str(value),
                                      timestamp=str(timestamp) or str(int(time.time()))).encode())
            while not byte_buffer.endswith(b'\n\n'):
                byte_buffer += self.sock.recv(self.RECV_BUFFER_SIZE)
        except Exception as e:
            raise ClientError(e, text=byte_buffer)

        if byte_buffer != b'ok\n\n':
            raise ClientError(text=byte_buffer)

    def get(self, key):
        byte_buffer = b''
        try:
            self.sock.sendall('get {key}\n'.format(key=str(key)).encode())
            while not byte_buffer.endswith(b'\n\n'):
                byte_buffer += self.sock.recv(self.RECV_BUFFER_SIZE)
        except Exception as e:
            raise ClientError(e, text=byte_buffer)

        buffer = byte_buffer[:-2].decode().split('\n')
        if buffer[0] == 'error' or buffer[0] != 'ok':
            raise ClientError(text=byte_buffer)

        result = {}
        for line in buffer[1:]:
            metric, value, timestamp = tuple(line.split())
            if metric not in result:
                result[metric] = []
            result[metric].append((int(timestamp), float(value)))

        for val in result.values():
            val.sort(key=itemgetter(0))

        return result


class ClientError(Exception):
    def __init__(self, exception=None, text=None):
        self.exception = exception
        self.text = text


if __name__ == '__main__':
    pass
