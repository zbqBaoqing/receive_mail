# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2015-12-28 16:24                        *
   *                                                      *
   * Filename: test.py
   *                                                      *
   ********************************************************
"""

from util.auth_totp import create_image_token, get_token, verify_my_token

def create_token():
    create_image_token()

if __name__ == "__main__":
    import sys,time
    code = sys.argv[1]
    time.sleep(60)
    verify_my_token(code)
    get_token()
    #create_token()
