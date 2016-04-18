# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2015-12-23 10:30                        *
   *                                                      *
   * Filename: run.py
   *                                                      *
   ********************************************************
"""
import commands
import time
from util.auth_totp import verify_my_token, get_token
from util.mailparse import MailParse
from util.logger import error_log
from util.mail import Email

class RunScript():
    
    @classmethod
    def getMail(cls):
        comm_dict = {}
        from_, body = MailParse.getMail()
        if not (from_ and body):
            return comm_dict
        comm_dict["from"] = from_
        if body:
            for command in  body.split("\r\n"):
                if command:
                    parts = command.split(":")
                    if len(parts) != 2:
                        error_log.error(u"存在不支持的自定义格式的命令参数! [command: %s]"% parts)
                        continue
                    else:
                        if parts[0].lower() not in comm_dict:
                            comm_dict[parts[0].lower()] = []
                        comm_dict[parts[0].lower()].append(parts[1].lower()) 
        return comm_dict

    @classmethod
    def executiv_order(cls, comm):
        # 一下是目前支持的命令
        if comm == "info":
            subjet = u"自定义邮件命令列表"
            body = u"目前支持的命令如下:\n"
            body += u"get:ip\n"
            body += u"get:hostname\n"
            body += u"run:sshd start\n"
            Email.send_text(subjet, 'zhangbaoqing',  body)
        elif comm == "ip":
            cmd = u"nohup python ~/work/receive_mail/command/getIp.py"
            returncode, result = commands.getstatusoutput(cmd)
            if returncode != 0:
                error_log.error(u"获取ip失败")
        elif comm == "hostname":
            cmd = u"nohup python ~/work/receive_mail/command/getHostname.py" 
            returncode, result = commands.getstatusoutput(cmd)
            if returncode != 0:
                error_log.error(u"获取主机名失败")
        elif comm == "sshd start":
            cmd = u"nohup /bin/sh ~/work/receive_mail/command/run.sh"
            returncode, result = commands.getstatusoutput(cmd)
            if returncode != 0:
                error_log.error(u"sshd start failed")
                Email.send_text(subjet, 'zhangbaoqing',  result)
            else:
                Email.send_text(u"sshd start [Succ]", 'zhangbaoqing', u"sshd start 成功")
        else:
            subjet = u"自定义邮件命令列表"
            body = u"目前支持的命令如下:\n"
            body += u"get:ip\n"
            body += u"get:hostname\n"
            body += u"run:sshd start\n"
            Email.send_text(subjet, 'zhangbaoqing',  body)




 
    @classmethod
    def runCommand(cls):
        comm_dict = cls.getMail()
        if comm_dict and comm_dict["code"]:
            if not verify_my_token(str(comm_dict["code"][0])):
                error_log.error(u"获取的口令不匹配, [code: %s]", comm_dict["code"])
                Email.send_to_maintainers(u"自定义的邮件命令", u"口令不匹配")
                return False
            if comm_dict["from"] != "zhangbaoqing@xiaomi.com":
                error_log.error(u"邮件发起者不匹配,[from: %s] ", comm_dict["from"])
                Email.send_text(u"非指定邮件用户", comm_dict["from"], u"你非指定邮件命令服务的指定用户，无权操作")
                Email.send_to_maintainers(u"自定义的邮件命令", u"邮寄发起者不匹配,[from:%s]" % comm_dict["from"])
                return False
            if 'run' in comm_dict:
                cls.executiv_order(comm_dict['run']) 
            for comm in comm_dict['get']:    
                cls.executiv_order(comm) 




if __name__ == "__main__":
    RunScript.runCommand()
