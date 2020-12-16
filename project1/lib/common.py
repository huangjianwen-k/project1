"""
存放公共方法的
"""
import hashlib
from interface import user_interface
import logging.config
from conf import settings

#密码加密
def get_pwd_md5(passworld):
    pwd_change = hashlib.md5()
    pwd_change.update(passworld.encode('utf-8'))
    salt = '爬山枝头,看月亮'
    pwd_change.update(salt.encode('utf-8'))

    return pwd_change.hexdigest()

#登录认证装饰器
def login_verify(func):
    from core import src
    def wrapper(*args,**kwargs):
        if src.login_stat:
            res = func(*args,**kwargs)
            return res
        else:
            print('登录状态异常,请重新登录')
            src.login()
    return wrapper

#添加日志功能
import logging

def get_logger(log_type):
    logging.config.dictConfig(
        settings.LOGGING_DIC
    )

    logger = logging.getLogger(log_type)

    return logger