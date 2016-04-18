# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2016-02-25 11:21                        *
   *                                                      *
   * Filename: getHostname.py
  *                                                      *
  ********************************************************

        
    功能说明:
"""

############FOR DEBUG######
import sys
import os
dir_ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print dir_
sys.path.insert(0, dir_)

import commands
import time
import socket
from util.logger import info_log
from util.mail import Email



class GetHostname():

    @classmethod
    def getHostname(cls):
        hostname = socket.gethostname()
        subject = u"获取主机名"
        now_time = time.asctime( time.localtime(time.time()) )
        body = u"time: %s" % now_time
        body += u"\nmsg: %s" % hostname
        Email.send_text(subject, 'zhangbaoqing', body)



GetHostname.getHostname()
