"""
银行相关业务接口
"""
from db import db_handler
import time

def withdraw_interface(username, money):
    #获取用户字典
    userdict = db_handler.select(username)
    #余额
    user_money = int(userdict['balance'])
    money = int(money)
    #加入手续费之后
    money2 = money * 1.001

    if user_money >= money:
        user_money -= money2
        flow = f'用户[@{username}]提现成功,提现金额[{money}$],手续费[{float(money2)- money}$]元,余额[{user_money}$]'
        userdict['balance'] = user_money
        userdict['flow'].append(flow)
        db_handler.save(userdict)
        return True,flow
    return False,'您好像没有这么多钱'

def bank_repay(username,money):
    user_dict = db_handler.select(username)
    money = int(money)
    if money >0:
        balance = int(user_dict.get('balance'))
        balance += money
        flow = f'用户[{username}还款金额[{money}],账户余额[{balance}]'
        user_dict['balance'] = balance
        user_dict['flow'].append(flow)
        db_handler.save(user_dict)
        return True,flow
    return False,f'您输入的金额有误,请确认后重新输入'


def bank_transfer(username,transfer_name,transfer_money):
    st_user_dict = db_handler.select(username)
    ed_user_dict = db_handler.select(transfer_name)
    transfer_money = int(transfer_money)
    balance = st_user_dict['balance']
    if not ed_user_dict:
        return False,'目标账户不存在'
    if ed_user_dict and st_user_dict['balance'] >= transfer_money:
        print('正在发起转账,请稍等.....')

        time.sleep(3)

        st_user_dict['balance'] -= transfer_money

        ed_user_dict['balance'] += transfer_money

        balance2 = st_user_dict['balance']

        flow = f'用户{username}账户转出金额[{transfer_money}$],余额{balance2},转入目标用户[{transfer_name}]账户,本次交易无需手续费'
        flow2 = f'用户{username}账户转入金额[{transfer_money}$]'
        st_user_dict['flow'].append(flow)

        db_handler.save(st_user_dict)

        db_handler.save(ed_user_dict)


        return True,flow
    return False,f'转账失败,[@{username}]账户余额不足,当前余额{balance}'

def check_flow(username):
    userdict = db_handler.select(username)
    flow_list = userdict['flow']

    return flow_list


#支付接口
def pay_interface(user,cost):
    user_dict = db_handler.select(user)
    balance = int(user_dict.get('balance'))
    # 判断用户金额是否足够
    if balance >= cost:
        # 减钱
        user_dict['balance'] = balance - cost
        flow = f'用户[{user}]支付成功,支付金额[{cost}$]'
        user_dict['flow'].append(flow)
        db_handler.save(user_dict)
        return True,flow
    else:
        return False,f'用户[{user}]账户余额不足,支付失败,当前余额[{balance}]'

