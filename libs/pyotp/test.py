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
from .totp import TOTP

def verify(token):
    totp_test = TOTP("asdfafadf", interval=30)
    print totp_test.verify(token, valid_window=30)

def get_token():
    totp_test = TOTP("asdfafadf", interval=30)
    return totp_test.now()


def create_image_token():
    totp_test = TOTP("asdfafadf")
    url = totp_test.provisoning_uri("zbqtest:tt@token")
    print "url: ",url
    import qrcode
    img = qrcode.make(url)
    img.save("test4.png")


if __name__ == "__main__":
    create_image_token()
