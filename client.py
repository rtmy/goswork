import os
from sys import stdin

import requests


SERVER_ADDR = '127.0.0.1:8000'


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class ConsoleInterface:
    def check_server_status(self):
        state_req = requests.get(f'http://{SERVER_ADDR}/chat/state/')
        if state_req.status_code == 200 and state_req.json().get('state', None) in ('master', 'node'):
            return state_req.json().get('state', None)
        return 
    
    def check_and_print_server_status(self):
        state = self.check_server_status()
        print('Server status:', state if bool(state) else 'FAIL')
    
    def retrieve_messages_from_server(self):
        list_ = requests.get(f'http://{SERVER_ADDR}/chat/list/')
        list_ = list_.json().get('messages', [])
        self.list_ = list_
        return list_
    
    def print_messages_from_buffer(self):
        list_ = self.retrieve_messages_from_server()
        for m in list_:
            content = m['content']

            if m.get('received'):
                print('him: ', end='')
                print(content)
            else:
                print('you: ', end='')
                print(content)
    
    def clear(self):
        self.list_ = []
        requests.get(f'http://{SERVER_ADDR}/chat/clear/')

    def send(self, message):
        requests.get(f'http://{SERVER_ADDR}/chat/send/?message={message}')
    
    def init(self):
        requests.get(f'http://{SERVER_ADDR}/chat/init/')
        self.check_and_print_server_status()
    
    def __call__(self):
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
                self.clear()
                cls()
            elif line.split('\n')[0] == 'init':
                self.init()
            elif line.split('\n')[0]:
                self.send(line.split('\n')[0])
            else:
                print('input below:')
                continue
            # print(line, end='')
            print('input below:')

if __name__ == '__main__':
    c = ConsoleInterface()
    c()
