# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2015-11-27 11:23                        *
   *                                                      *
   * Filename: getIp.py
   *                                                      *
   ********************************************************
"""

###########FOR DEBUG###########
import sys
import os
dir_ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print dir_
sys.path.insert(0, dir_)

import commands
import time
import re
from util.mail import Email
from util.logger import info_log



class GetIp:


    @classmethod
    def retry_get(cls, cmd):
        cnt = 1
        returncode = -1
        
        result = u"cant't get host ip"
        while cnt < 5:
            time.sleep(2<<cnt)
            returncode, result = commands.getstatusoutput(cmd)
            if returncode == 0:
                return returncode, result
            cnt += 1
        return returncode, result


    @classmethod
    def getip(cls):
        cmd = u"/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:'"
        returncode, result = cls.retry_get(cmd)
        if returncode != 0:
            info_log.error(u"exit_code: %s, resutl: %s" % (returncode, result))
        else:
            info_log.info(u"exit_code: %s, resutl: %s" % (returncode, result))
        subject = u"获取主机ip"
        now_time = time.asctime( time.localtime(time.time()) )
        body = u"time: %s" % now_time
        body += u"\nmsg: %s" % result
        Email.send_text(subject, 'zhangbaoqing', body)



GetIp.getip()
