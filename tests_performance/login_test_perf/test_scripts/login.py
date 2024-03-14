import socket
import time
import binascii
import requests
import random
import string
import base64

# Open a connection
class Transaction(object):
    def __init__(self):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self._conn.connect(('10.196.228.12', 8080))
        self.url = 'http://10.196.228.12:8080/api/v2'
        self.user_a = ''
        self.password_a = base64.b64decode('')

    def run_recorded(self):
        file_raw = open('recorded_traffic', 'r')
        buf = file_raw.read()
        time.sleep(0.5)
        self._conn.send(buf)
        content = self._conn.recv(4096)
        print binascii.hexlify(content)
        assert ('0000000d4103001da211001f010008a038' in binascii.hexlify(content)), 'Failed'

    def run_login(self):
        url = self.url + '/' + 'login'
        data = {'login': self.user_a, 'password': self.password_a}
        r = requests.post(url, data)
        r.raw.read()

    def run(self):
        ticket = 'ST-67-bla'
        dirname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        r = requests.post(self.url + '/file/create' + '?ticket=' + ticket,
                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                   'Accept': 'application/json'}, data={'name': dirname})
        r.raw.read()


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
