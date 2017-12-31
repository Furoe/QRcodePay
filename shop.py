# encoding=utf-8
import socket
import time
import hashlib
import json
import os
from PIL import Image
import zbarlight


class Shop(object):
    def __init__(self):
        now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        ID = ('test1234Abcd@1234' + now).encode('utf-8')
        self.md5 = hashlib.md5(ID).hexdigest()

        self.shopinfo = {'name': 'testshop1', 'receiveID': 'test1234567890987654321'}
        pass

    def generateOrder(self):
        order = {}
        price = input('请输入金额:\n')

        print('请扫描用户的付款码')
        userinfo = self.scanQRcode()

        print('生成订单中...')
        for key in self.shopinfo.keys():
            order[key] = self.shopinfo.get(key)
        order['price'] = 'RMB %.2f' % float(price)
        order['username'] = userinfo.get('username')
        order['payID'] = userinfo.get('payID')

        self.confirm(order)

    def scanQRcode(self):
        try:
            filename = input('>')
            while not os.path.exists(filename):
                print('无效的文件名称，请重新输入')
                filename = input('>')

            with open(filename, 'rb') as image_file:
                image = Image.open(image_file)
                image.load()
            print('正在扫描，请稍等...')
            # 得到了二维码原始值
            codes = zbarlight.scan_codes('qrcode', image)
            # 解析二维码的值
            data = codes[0].decode()
            userinfo = {}
            userinfo['username'], userinfo['payID'] = data.split(',')
            return userinfo
        except Exception as msg:
            print(msg)
            return {}

    def confirm(self, order):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 45679))
        s.send(json.dumps(order).encode())

        result = s.recv(1024)
        print(result.decode('utf-8'))


if __name__ == '__main__':
    shop = Shop()
    shop.generateOrder()