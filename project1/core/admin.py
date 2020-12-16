from core import src
from db import db_handler
from interface import user_interface

def add_user():
    src.rigister()

def change_balance():
    result, msg = user_interface.change_balance()
    if result == 'True':
        print(msg)
    elif result == 'False':
        print(msg)
    else:
        print('未知错误')
def lock_user():
    result,msg = user_interface.lock()
    if result == 'True':
        print(msg)
    elif result == 'False':
        print(msg)
    else:
        print('未知错误')

admin_func = {
    '1':add_user,
    '2':change_balance,
    '3':lock_user
}

def admin_task():
    while True:
        print('''
        1,添加账户
        2,修改额度
        3,冻结账户
        ''')

        choice = input('请输入您要完成的操作').strip()

        if choice not in admin_func:
            print('您的输入有误,请重新输入')
            continue
        admin_func.get(choice)()
        break