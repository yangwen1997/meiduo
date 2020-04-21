import re
import random
import hashlib
import time

import requests

from yzm import Authentication


def get_userNameAndPassword():
    global userName, userPassword
    letterChar = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numChar = "1234567890"

    e_userName = []
    e_userPassword = []

    for i in range(random.randint(1, 5)):
        e_userName.append(random.choice(letterChar))
    for j in range(8 - len(e_userName)):
        e_userName.append(random.choice(numChar))

    e_userPassword.append(random.choice(letterChar))
    for k in range(6):
        e_userPassword.append(random.choice(letterChar + numChar))

    userName = ''.join(e_userName)
    userPassword = ''.join(e_userPassword)


class Register:
    def __init__(self):
        self.auth = Authentication('whitedgg', 'dgg123456', 14141)
        self.headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    def send_sms(self, phoneNum):
        """发送验证码"""
        count = 0
        post_url = "http://www.sooip.com.cn/txnsendEmailRegiest.ajax"
        resp = requests.post(post_url, data={'receiver': phoneNum}, headers=self.headers)
        is_success = re.search('<error-code>000000</error-code>', resp.text)
        if is_success:
            while count < 8:
                time.sleep(3)
                code = self.auth.getCode(phoneNum)
                if code:
                    break
                count += 1
        if code:
            print('****************Get SmsCode Success !!! The Code is 【%s】********************'%code)
            return code
        else:
            print('Not Get Sms Code !!!')
            return None

    def pwd_md5(self, password):
        """密码进行加密"""
        return hashlib.md5(password.encode('utf8')).hexdigest().upper()

    @staticmethod
    def record_account():
        with open('account.txt', 'a+') as f:
            record = '{0}  {1} \n'.format(userName, userPassword)
            f.write(record)

    def register(self):
        while True:
            get_userNameAndPassword()
            phoneNum = self.auth.getMobile()
            code = self.send_sms(phoneNum)
            if code:
                register_url = 'http://www.sooip.com.cn/txnregister.ajax'
                data = {
                    'login_id': userName,
                    'login_pwd': self.pwd_md5(userPassword),
                    'cert_code': code,
                    'e_mail': phoneNum,
                    'login_pwd_length': len(userPassword),
                }
                resp = requests.post(register_url, headers=self.headers, data=data)
                is_success = re.search('<error-code>000000</error-code>', resp.text)
                if is_success:
                    print('Register is success!!! userName:【{0}】, userPassword:【{1}】'.format(userName, userPassword))
                    Register.record_account()
                else:
                    print('Register Failed !!!')


if __name__ == '__main__':
    r = Register()
    r.register()
