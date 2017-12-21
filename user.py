# encoding=utf-8
import time
import base64
import socket
import hashlib
import threading
import json
import rsa

import MyQR.myqr as qr


class User(object):
    def __init__(self):
        self.username = 'test1234'
        self.passwd = 'Abcd@1234'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 45678))
        self.s.listen(10)

    def rsaEncrypt(self, str):
        # 生成公钥、私钥
        pubkey, privkey = rsa.newkeys(512)
        # 转换字符编码方式
        content = str.encode('utf-8')
        crypto = rsa.encrypt(content, pubkey)
        crypto = base64.b64encode(crypto)
        return crypto, privkey

    def rsaDecrypt(self, crypto, privkey):
        crypto = base64.b64decode(crypto)
        content = rsa.decrypt(crypto, privkey)
        content = content.decode('utf-8')
        return content

    def generatePayID(self):
        now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        ID = (self.username+self.passwd+now).encode('utf-8')
        payID = hashlib.md5(ID).hexdigest()
        print(payID)
        return payID

    def generateQRcode(self):
        ID = self.generatePayID()
        info = self.username + ',' + ID
        qr.run(info)

    def signature(self):
        pass

    def listen(self):
        print('listen')

        # 接受一个新连接:
        sock, addr = self.s.accept()
        print('server')
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=self.confirm, args=(sock, addr))
        t.start()

    def confirm(self, sock, addr):
        try:
            print('Accept new connection from %s:%s...' % addr)

            data = sock.recv(1024)
            # print(data)
            data = json.loads(data.decode())

            # 用户确认是否付款
            flag = input('OK?')
            if flag == 'yes':
                data['ack'] = True

            sock.send(json.dumps(data).encode())
            sock.close()
            print('Connection from %s:%s closed.' % addr)

        except Exception as msg:
            print(msg)


if __name__ == '__main__':
    user = User()
    # crypto, privkey = user.rsaEncrypt('hello,world!')
    # print(crypto)
    # print(privkey)
    # str = user.rsaDecrypt(crypto, privkey)
    # print(str)
    # user.generatePayID()
    # time.sleep(60)
    # user.generatePayID()
    # user.generateQRcode()
    user.listen()