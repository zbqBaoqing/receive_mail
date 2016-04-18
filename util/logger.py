#-*- coding:utf-8 -*-

import os
from logging.handlers import TimedRotatingFileHandler
from configs import config
import logging
logging.basicConfig(
        format='%(asctime)s\t%(levelname)s\t%(filename)s\t[line:%(lineno)d] [func:%(funcName)s] [msg:%(message)s]',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if config.DEBUG else logging.INFO)



def get_logger(logger_name, logger_module, has_formatter=True):
    """申明logger

    Args:
        logger: str
        logger_moduls: logger所属的模块，方便后面按照不同的路径进行切分
    """
    log_dir = "%s/unknown/" % (config.LOG_DIR)
    if logger_module:
        log_dir = "%s/%s/" % (config.LOG_DIR, logger_module)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    log = logging.getLogger(logger_name)
    file_handler = TimedRotatingFileHandler("%s/%s.log" % (log_dir, logger_name), 'W0')
    if has_formatter:
        logger_format = '[%(asctime)s][%(thread)d][%(levelname)s][%(filename)s][line:%(lineno)d] [func:%(funcName)s] [msg:%(message)s]'
        formatter = logging.Formatter(logger_format)
        file_handler.setFormatter(formatter)
    else:
        # 没有格式，只打印时间
        formatter = logging.Formatter('%(asctime)s\t%(message)s')
        file_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    return log

## log 申明
error_log = get_logger("error", "common")
mail_log = get_logger("mail", "common")
info_log = get_logger("info", "common")
