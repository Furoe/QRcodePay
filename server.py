# encoding=utf-8
import socket
import threading
import time
import hashlib
import json
# import pymongo


class Server(object):
    def __init__(self):
        self.s_shop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_shop.bind(('127.0.0.1', 45679))
        self.s_shop.listen(10)

        # test,用户名与密码存储在这里，这是demo，故不考虑这些的处理
        self.users = [{'username': 'test1234', 'passwd': 'Abcd@1234'}]

    def listen(self):
        print('[status] listening')
        while True:
            # 接受一个新连接:
            sock, addr = self.s_shop.accept()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=self.shopconn, args=(sock, addr))
            t.start()

    def shopconn(self, sock, addr):
        print('[status] Accept new connection from %s:%s...' % addr)

        data = sock.recv(1024)
        data = json.loads(data)

        username = data.get('username')
        payID = data.get('payID')
        # 验证
        for name in self.users:
            if name.get('username') == username:
                now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                ID = (name.get('username') + name.get('passwd') + now).encode('utf-8')
                md5 = hashlib.md5(ID).hexdigest()
                if md5 == payID:
                    # 验证了商户shop端的信息
                    # ack模拟请求用户输入确定与否
                    data['ack'] = False
                    # 开始user的验证
                    data_user = self.confirm(data)
                    data_user = json.loads(data_user)
                    if data_user.get('ack'):
                        # 在这里进行转账操作
                        print('[pay info] pay success')
                        sock.send(u'交易成功'.encode('utf-8'))

                    else:
                        print('[pay info] pay fail')
                        sock.send(u'交易失败'.encode('utf-8'))
        sock.close()
        print('[status] Connection from %s:%s closed.' % addr)

    def confirm(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 45678))
        s.send(json.dumps(data).encode())
        data_user = s.recv(1024)
        return data_user


if __name__ == '__main__':
    server = Server()
    server.listen()