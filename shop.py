# encoding=utf-8
import socket
import time
import hashlib
import json


class Shop(object):
    def __init__(self):
        now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        ID = ('test1234Abcd@1234' + now).encode('utf-8')
        self.md5 = hashlib.md5(ID).hexdigest()
        pass

    def confirm(self):
        data = {'username':'test1234', 'payID': self.md5, 'price': '$100.00'}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 45679))
        s.send(json.dumps(data).encode())


if __name__ == '__main__':
    shop = Shop()
    shop.confirm()