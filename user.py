# encoding=utf-8
import time
import base64
import hashlib
import rsa

import MyQR.myqr as qr


class User(object):
    def __init__(self):
        self.username = 'test1234'
        self.passwd = 'Abcd@1234'

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
        md5 = hashlib.md5(ID).hexdigest()
        print(md5)
        return md5

    def generateQRcode(self):
        ID = self.generatePayID()
        info = self.username + ',' + ID
        qr.run(info)

    def signature(self):
        pass

    def confirm(self):
        pass


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
    user.generateQRcode()
