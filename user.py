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

        self.touse = ['name', 'price', 'username', 'ack']
        self.toshow = {'name': '商家', 'price': '订单总额', 'username': '用户名', 'ack': '支付状态'}

    def start(self):
        try:
            while True:
                print('-'*40)
                ans = input('是否生成一张付款码以付款？(yes/no)\n')
                if ans == 'yes':
                    t = threading.Thread(target=self.generateQRcode)
                    t.start()
                    print('生成付款码成功(当前分钟内有效)')
                    # 监听付款过程服务器端的信息
                    self.listen()
                elif ans == 'no':
                    print('你拒绝生成一张付款码')
                else:
                    print('输入错误')
        except Exception as msg:
            print(msg)

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
        print('waiting...')

        # 接受一个新连接:
        sock, addr = self.s.accept()
        # # 创建新线程来处理TCP连接:
        # t = threading.Thread(target=self.confirm, args=(sock, addr))
        # t.start()
        self.confirm(sock, addr)

    def confirm(self, sock, addr):
        try:
            # print('Accept new connection from %s:%s...' % addr)

            data = sock.recv(1024)
            # print(data)
            data = json.loads(data.decode())
            print('付款信息:')
            print('~'*40)
            for key in self.touse:
                print('%s: %s' % (self.toshow.get(key), data.get(key)))
            print('~'*40)
            # 用户确认是否付款
            flag = input('确认支付？(yes/no)\n')
            if flag == 'yes':
                data['ack'] = True
                print('支付成功')
            else:
                print('支付失败')

            sock.send(json.dumps(data).encode())
            sock.close()
            # print('Connection from %s:%s closed.' % addr)

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
    user.start()