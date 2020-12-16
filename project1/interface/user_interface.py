"""
逻辑接口
    用户接口
"""
from db import db_handler
from conf import settings
import time
from lib import common

user_logger = common.get_logger('user')

# 组织用户的数据字典信息
def regist_interface(user_name,passworld,balance=15000):
    user_dict = {
        'username': user_name,
        'passworld': passworld,
        'balance': 15000,
        # 购物流水
        'flow': [],
        'shopcar': {},
        # False=未冻结 , True=已被冻结
        'locked': False

    }
    # 查看用户是否存在
    user_data =  db_handler.select(user_name)
    if user_data:
        print('用户名已存在')
        return False,user_data
    else:
        print('用户%s正在进行注册' % user_name)
        time.sleep(2.5)
        db_handler.save(user_dict)
        flow = f'用户[{user_name}]注册成功'
        user_logger.info(flow)
        return True,flow

def login_interface(username,passworld):
    userdata = db_handler.select(username)
    if userdata:
        pwd = userdata.get('passworld')
        if passworld == pwd:
            flow = f'用户[{username}]登录成功'
            user_logger.info(flow)
            return True,flow
        else:
            print('账号或密码错误,请重新输入')
            user_logger.warning('账号或密码错误,请重新输入')
            return False
    else:
        user_logger.warning('该用户不存在,请确认哦')
        return False


#查看余额
def check_user_balance(username):
    user_dict=db_handler.select(username)
    balance=user_dict.get("balance")
    user_logger.info('当前余额:',balance)
    return balance

# def admin_operation(username,type,change):
#     user_dict = db_handler.select(username)
#     KEY = type
#     value = change
#     sure = input('是否确认修改:T/F').strip()
#     if sure == 'T':
#         user_dict[KEY] = value
#         print('正在保存修改....')
#         time.sleep(2)
#         print(user_dict)
#         db_handler.save(user_dict)
#         return True,f'修改用户{username}的{type}成功,当前状态为{change}'
#
#     elif sure == 'F':
#         return False,f'修改用户{username}的{type}操作被取消'
#
#     else:
#         return False,'未知错误'

def lock():
    user = input('请输入你要修改的用户').strip()
    userdict = db_handler.select(user)
    print(userdict['locked'])
    sure = input('是否继续修改(T/F)').strip()
    if sure == 'T':
        state = input('修改为(True/False):>>>')
        userdict['locked'] = state
        db_handler.save(userdict)
        flow=f'修改账户{user}状态成功,当前状态为{state}'

        return True,flow
    else:
        flow = '用户取消操作'
        user_logger.info(flow)
        return False,flow

def change_balance():
    user = input('请输入您要修改的用户').strip()
    userdict = db_handler.select(user)
    print(userdict['balance'])
    choice = input("是否继续修改:T/F")
    while choice == 'T':
        new = input('请输入您要修改的值').strip()
        if not new.isdigit():
            user_logger.info('您的输入有误,请重新输入')
            continue
        userdict["balance"] = new
        db_handler.save(userdict)
        flow = f'修改用户{user}额度成功,当前额度{new}'
        user_logger.info(flow)
        return True,flow
        break
    else:
        flow = '用户取消操作'
        user_logger.info(flow)
        return False,flow