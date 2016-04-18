# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2015-12-25 20:02                        *
   *                                                      *
   * Filename: test.py
   *                                                      *
   ********************************************************
"""
from libs import pyotp
import time

def verify_my_token(token):
    totp_test = pyotp.TOTP("NRCHUAJJCYDK4YPG", interval=30)
    result = totp_test.verify(token, valid_window=60) # 60s 保证,cron每分钟拉取的邮件中的code有效性，也就说，code的有效性为60s,如果，拉取时间长于60s,那可能验证code无效,时间可设更长点
    return result


def get_token():
    totp_test = pyotp.TOTP("NRCHUAJJCYDK4YPG", interval=30)
    token = totp_test.now()
    print token
    return token


def create_image_token():
    seed = pyotp.random_base32()
    print seed
    totp_test = pyotp.TOTP(seed, interval=30)
    url = totp_test.provisioning_uri("zbq:command@token")
    print "url: ",url
    import qrcode
    img = qrcode.make(url)
    img.save("my_command.png")

if __name__ == "__main__":
    import sys
    #code = sys.argv[1]
    #time.sleep(60)
    #verify(code)
    print sys.path()
    print get_token()
    create_image_token()
