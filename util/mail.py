# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2016-02-25 20:21                        *
   *                                                      *
   * Filename: mail.py
  *                                                      *
  ********************************************************

        
    功能说明:
        邮件发送
"""

import base64
import commands
import traceback
import tempfile
import os
import socket

import smtplib

from .logger import mail_log
from .common_functions import CommonFunctions
from configs.config import DEBUG, MAINTAINERS, HOSTNAME

class Email:
    """发送邮件
    """

    @classmethod
    def send_to_maintainers(cls, subject, content, mail_from='mailcommand@app.xiaomi.com'):
        if type(content) == unicode:
            content = content.encode('utf-8')
        subject = "[zbq][mail_query][%s]%s" % (HOSTNAME, subject)
        mail_to = ";".join(MAINTAINERS)

        line = "-" * 150
        err_traceback = CommonFunctions.get_exception_info()
        content += "\n\n\n"+line+"\n"
        content += "<strong>异常信息:</strong>"
        content += "\n"+line+"\n"
        content +=  err_traceback

        content += "\n"+line+"\n\n\n"
        content += "<strong>堆栈信息:</strong>"
        content += "\n"+line+"\n"
        content += "\n".join(traceback.format_stack())
        content += "\n"+line+"\n"
        cls.send_text(subject, mail_to, content, None, mail_from)


    @classmethod
    def send_text(cls, subject, mail_to, content, mail_cc=None, mail_from='mailcommand@app.xiaomi.com'):
        """发送文本消息,文本后将追加公共信息
        """
        if type(subject) == unicode:
            subject = subject.encode('utf-8')

        if type(mail_to) == unicode:
            mail_to = mail_to.encode('utf-8')

        if type(mail_cc) == unicode:
            mail_cc = mail_cc.encode('utf-8')

        if type(mail_from) == unicode:
            mail_from = mail_from.encode('utf-8')

        if type(content) == unicode:
            content = content.encode('utf-8')

        mail_str = ''

        if DEBUG:
            # DEBUG模式将只发给开发者
            orign_mail_to = mail_to
            mail_to = ";".join(MAINTAINERS)

            # 增加dev标识
            mail_str += "Subject: =?UTF-8?B?%s?=\nMIME-Version: 1.0\n" % (base64.b64encode("[dev]"+subject))

            # 将原始收件人写到正文中
            content = "原始收件人是：%s(Cc:%s)\n------------------------------\n%s" % (orign_mail_to, mail_cc, content)
        else:
            if mail_cc:
                mail_str += "Cc: %s\n" % (cls.__add_address(mail_cc))
                mail_to += ";%s" % mail_cc
            mail_str += "Subject: =?UTF-8?B?%s?=\nMIME-Version: 1.0\n" % (base64.b64encode("[pro]"+subject))

        mail_str += "From: %s\n" % (cls.__add_address(mail_from))
        mail_str += "To: %s\n" % (cls.__add_address(mail_to))
        mail_str += "Content-Type: text/html;charset=utf-8\n\n"

        content += "\n\n\n\n如有疑问，请及时联系运维权限平台管理员(%s)" % (";".join(MAINTAINERS))
        content = content.replace("\n", "</br>")
        mail_str += "%s" % (content)

        cls.__excute(mail_str, mail_from, mail_to)

    @classmethod
    def __excute(cls, mail_content, mail_from, mail_to):
        """执行shell脚本命令
        """
        mail_to = cls.__add_address(mail_to)
        mail_from = cls.__add_address(mail_from)
        try:
            # 产生临时文件
            f = tempfile.NamedTemporaryFile(delete=False)
            f.write(mail_content)
            f.close()

            command = "/usr/sbin/sendmail -f  '%s' '%s' < %s" % (mail_from, mail_to, f.name)
            returncode, result = commands.getstatusoutput(command)
            if returncode != 0:
                command = "/usr/sbin/sendmail -f  '%s' '%s' < %s" % (mail_from, mail_to.replace(';', ','), f.name)
                returncode, result = commands.getstatusoutput(command)
            if returncode !=0:
                mail_log.error("%s is error[%s][%s]" % (command, returncode, result))

            # 删除临时文件
            #os.unlink(f.name)

            mail_log.info(mail_content)
            mail_log.info(command)
            mail_log.info("mail command exec result: %s" % (result))
        except Exception, e:
            err_msg = CommonFunctions.get_exception_info()
            mail_log.error(err_msg)
            raise e

    @classmethod
    def __add_address(cls, mail_names):
        """检查邮件地址是否有xiaomi.com，如果没有则加上
        """
        name_list = mail_names.replace(",", ";").split(";")
        filte_name_list = []
        for name in name_list:
            if not name.endswith("xiaomi.com"):
                filte_name_list.append("%s@xiaomi.com" % (name))
            else:
                filte_name_list.append(name)
        ret = ";".join(filte_name_list)
        return ret
