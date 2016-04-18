# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2015-12-23 13:52                        *
   *                                                      *
   * Filename: config.py
   *                                                      *
   ********************************************************
"""
import os
import socket

MAINTAINERS = ["zhangbaoqing"]
HOSTNAME = socket.gethostname()
DEBUG = False
#根路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = "%s/log" % ROOT_DIR
#创建log目录
not os.path.exists(LOG_DIR) and os.mkdir(LOG_DIR)

