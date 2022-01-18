import os
from sys import stdin

import requests


SERVER_ADDR = '127.0.0.1:8000'


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class ClientApi:
    """Класс для общения с сервером через HTTP"""
    def __init__(self, address=SERVER_ADDR):
        self.address = address
    
    def check_server_status(self):
        state_req = requests.get(f'http://{self.address}/chat/state/')
        if state_req.status_code == 200 and state_req.json().get('state', None) in ('master', 'node'):
            return state_req.json().get('state', None)
        return 
    
    def clear(self):
        requests.get(f'http://{self.address}/chat/clear/')
    
    def send(self, message):
        requests.get(f'http://{self.address}/chat/send/', params=dict(message=message))
    
    def init(self):
        requests.get(f'http://{self.address}/chat/init/')
    
    def messages(self):
        messages = requests.get(f'http://{SERVER_ADDR}/chat/list/')
        return messages.json().get('messages', [])


class ConsoleInterface:
    def __call__(self):
        """Отрисовка основного меню и обработка сообщений"""
        cls()
        self.check_and_print_server_status()
        self.print_messages_from_buffer()
        print('waiting for input\nprint help to list commands\ninput below:')
        for line in stdin:
            cls()
            self.print_messages_from_buffer()
            if line.split('\n')[0] == 'help':
                print('help - print this message')
                print('init 127.0.0.1:9000 - try to init connection with 127.0.0.1:9000')
                print('clear - clear history')
                print('message - send "message"')
            elif line.split('\n')[0] == 'clear':
                self.api.clear()
                cls()
            elif line.split('\n')[0] == 'init':
                self.init()
            elif line.split('\n')[0]:
                self.api.send(line.split('\n')[0])
            else:
                print('input below:')
                continue
            # print(line, end='')
            print('input below:')
    
    def __init__(self):
        self.api = ClientApi()

    def check_and_print_server_status(self):
        state = self.api.check_server_status()
        print('Server status:', state or 'FAIL')
    
    def retrieve_messages_from_server(self):
        messages = self.api.messages()
        self.messages = messages
        return messages
    
    def print_messages_from_buffer(self):
        messages = self.retrieve_messages_from_server()
        for m in messages:
            content = m['content']

            if m.get('received'):
                print('him: ', end='')
                print(content)
            else:
                print('you: ', end='')
                print(content)
    
    def clear(self):
        self.messages = []
        self.api.clear()


if __name__ == '__main__':
    c = ConsoleInterface()
    c()
