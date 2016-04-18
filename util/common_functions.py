# -*- coding:utf-8 -*- "
"""
   ***********************************************
   * File Name   : common_funtions.py
   * Author      : Chen Zijun                    *
   * Mail        : chenzijun@xiaomi.com          *
   * Created Time: 2013-04-07                    *
   ***********************************************
"""

import socket
import sys, traceback, json

class CommonFunctions:
    """一些公共的函数
    """

    @classmethod
    def get_exception_info(cls):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        info = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return "\n".join(info)

    @classmethod
    def json_decode(cls, content):
        obj = json.loads(content)
        return cls.convert(obj)
    
    @classmethod
    def convert(cls, decode_obj):
        """将json.loads()的返回值进行转化
        对于unicode将转化为utf-8
        """
        if isinstance(decode_obj, dict):
            return dict([(cls.convert(key), cls.convert(value)) for key, value in decode_obj.iteritems()])
        elif isinstance(decode_obj, list):
            return [cls.convert(element) for element in decode_obj]
        elif isinstance(decode_obj, unicode):
            return decode_obj.encode('utf-8')
        else:
            return decode_obj

    @classmethod
    def gethostbyaddr(cls, ip):
        ret = None
        if ip:
            try:
                result = socket.gethostbyaddr(ip)
                host = result[0]
                ret = host
            except :
                pass
        return ret

