import asyncio


class MetricsData:
    def __init__(self):
        self.data = {}

    def put(self, args):
        try:
            metric, value, timestamp = args
            if metric not in self.data:
                self.data[metric] = {}
            self.data[metric][int(timestamp)] = float(value)
        except (ValueError, TypeError) as e:
            raise ServerCommandArgsError(e)
        return 'ok\n\n'

    def metric_response(self, metric):
        answer = ''
        for timestamp, value in self.data.get(metric, {}).items():
            answer += f'{metric} {value} {timestamp}\n'
        return answer

    def all_metrics_response(self):
        answer = ''
        for metric in self.data.keys():
            answer += f'{self.metric_response(metric)}'
        return answer

    def response_handle(self, metric):
        if metric == '*':
            return self.all_metrics_response()
        return self.metric_response(metric)

    def get(self, args):
        try:
            metric, = args
        except (ValueError, TypeError) as e:
            raise ServerCommandArgsError(e)
        return f'ok\n{self.response_handle(metric)}\n'

    def process_data(self, data):
        words = data.split()
        if words[0] == 'put':
            return self.put(words[1:])
        if words[0] == 'get':
            return self.get(words[1:])
        raise ServerCommandError()


metrics_data = MetricsData()


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            response = metrics_data.process_data(data.decode())
        except ServerError as e:
            response = 'error\n{}\n\n'.format(e.__doc__)
        self.transport.write(response.encode())


class ServerError(Exception):
    """Общий класс исключений сервера"""
    pass


class ServerCommandError(ServerError):
    """Исключение, выбрасываемое сервером на отсутствующую команду"""
    pass


class ServerCommandArgsError(ServerError):
    """Исключение, выбрасываемое сервером при неправильных аргументах"""
    pass


def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server()
