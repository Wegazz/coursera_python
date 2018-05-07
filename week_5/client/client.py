import socket
import time
from operator import itemgetter


class Client:
    RECV_BUFFER_SIZE = 1024

    def __init__(self, host, port, timeout=None):
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as e:
            raise ClientSocketError(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def request(self, request):
        try:
            self.connection.sendall(request.encode())
            byte_buffer = b''
            while not byte_buffer.endswith(b'\n\n'):
                byte_buffer += self.connection.recv(self.RECV_BUFFER_SIZE)
            result = byte_buffer.decode().split('\n')
            if result[0] == 'error' or result[0] != 'ok':
                raise ClientProtocolError(result)
            return result[1:-2]
        except socket.error as e:
            raise ClientSocketError(e)

    def put(self, key, value, timestamp=None):
        self.request('put {key} {value} {timestamp}\n'.format(key=key, value=str(value),
                                                              timestamp=str(timestamp) or str(int(time.time()))))

    def get(self, key):
        result = {}
        for line in self.request(f'get {key}\n'):
            try:
                metric, value, timestamp = line.split()
                if metric not in result:
                    result[metric] = []
                result[metric].append((int(timestamp), float(value)))
            except (ValueError, TypeError) as e:
                raise ClientProtocolError(e)

        for val in result.values():
            val.sort(key=itemgetter(0))

        return result


class ClientError(Exception):
    """Общий класс исключений клиента"""
    pass


class ClientSocketError(ClientError):
    """Исключение, выбрасываемое клиентом при сетевой ошибке"""
    pass


class ClientProtocolError(ClientError):
    """Исключение, выбрасываемое клиентом при ошибке протокола"""
    pass


if __name__ == '__main__':
    pass
