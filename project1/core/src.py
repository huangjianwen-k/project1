"""
存放用户视图层
"""
import sys
import os
from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common
from core import admin

login_stat = None
# user_data =None

# 1、注册功能
def rigister():
    user_name = input('请输入用户名:')
    passworld = input('请输入密码:')
    re_passworld = input('请确认密码:')
    # 判断密码是否一致
    if passworld == re_passworld:
        #调用接口层的注册接口,将用户名与密码交给接口层进行处理
        passworld = common.get_pwd_md5(passworld)
        user_interface.regist_interface(user_name, passworld)
    else:
        print('两次输入的密码不一致,请重新输入')


# 2、登录功能
def login():
    while True:
        username = input('请输入用户名:').strip()
        passworld = input('请输入密码') .strip()
        passworld = common.get_pwd_md5(passworld)
        user_data= user_interface.login_interface(username,passworld)
        global login_stat
        login_stat = user_data
        return login_stat
# 3、查看余额
@common.login_verify
def check_balance():
     balance = user_interface.check_user_balance(login_stat)
     print('您的余额为: %s元 ' % balance)
     # print(balance)
# @login_auth
# def check_balance():
#     pass

# 4、提现功能
@common.login_verify
def withdraw():
    while True:
        input_num = input('请输入您要提现的金额>>>>:').strip()
        print(input_num)
        if not input_num.isdigit():
            print('您的输入有误,请重新输入')
            continue
        result,msg = bank_interface.withdraw_interface(
            login_stat,input_num
        )
        if result:
            print(msg)
        else:
            print(msg)
        break
        # if flag:
        #     pass
        # else:
        #     pass

# 5、还款功能
@common.login_verify
def repay():
    while True:
        repay_money = input('请输入您的还款金额').strip()
        if not repay_money.isdigit():
            print('请输入正确的金额')
            continue
        result,msg = bank_interface.bank_repay(
            login_stat,repay_money
        )
        if result:
            print(msg)
        else:
            print(msg)
        break
# 6、转账功能
@common.login_verify
def transfer():
    while True:
        transfer_name = input('请输入目标用户>>:').strip()
        transfer_money = input('请输入要转账的金额').strip()
        if not transfer_money.isdigit():
            print('转账金额输入有误,请重新输入')
            continue
        result,msg = bank_interface.bank_transfer(login_stat,transfer_name,transfer_money)

        if result == True:
            print(msg)
        else:
            print(msg)
            continue
        break

# 7、查看流水
@common.login_verify
def check_flow():
    flow_list = bank_interface.check_flow(login_stat)
    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前没有流水哦')

# 8、购物功能
@common.login_verify
def shopping():
    #商品列表
    shop_list = [
        ['戏志才',800],
        ['关索',600],
        ['关银屏',760]
    ]
    # 初始化当前购物车

    shopping_car = {}
    while True:
        for index,shop in enumerate(shop_list):
            shop_name,shop_price = shop
            print(f'商品编号[{index}]',
                  f'商品名称[@@{shop_name}]',
                  f''f'商品单价[{shop_price}$]')
        #让用户选择
        choice = input('请输入目标商品编号(结算输入T,加入购物车请输入F):>>>').strip()
        if choice =='T':
            #调用支付接口
            result,msg = shop_interface.shopping_interface(login_stat,shopping_car)
            print(result)
            if result == True:
                print(msg)
            elif result == False:
                print(msg)
            else:
                print('未知错误')
            continue
        elif choice =='F':
            if not shopping_car:
                print('购物车是空的,不能添加')
                continue
            result,msg = shop_interface.add_shop_car_interface(
                login_stat,shopping_car
            )
            if result:
                print(msg)
                break



        if not choice.isdigit():
            print('商品编号仅能输入数字哦')
            continue
        choice = int(choice)

        if choice not in range(len(shop_list)):
            print('没有这个商品编码,请确认后重新输入')
            continue

        #获取商品列表与单价
        shop_name,shop_price = shop_list[choice]

        #5加入购物车
        if shop_name in shopping_car:
            shopping_car[shop_name][1] +=1
        else:
            shopping_car[shop_name] = [shop_price,1]
        print(shopping_car)



# 9、查看购物车
@common.login_verify
def check_shop_car():
    shop_car = shop_interface.check_shopping_car(login_stat)
    print(shop_car)
    while True:
        choice = input('[干啥嘞:支付:p/整理购物车:c/清空购物车:clear]>>>>>')
        if choice not in ('p','c','clear'):
            print('您的输入有误,请重新输入')
        if choice == 'p':
            if not shop_car:
                print('您的购物车是空的哦,快去添加商品吧....')
                continue
            result,msg = shop_interface.shopping_interface(login_stat,shop_car)
            if result == True:
                print ('success',msg)
            elif result == False:
                print('fail',msg)
            else:
                print('未知错误')
        elif choice == 'c':
            choice = input('修改商品数量:1/删除商品:2')
            if choice == '1':
                result,msg = shop_interface.change_shop_car(login_stat)
                if result == True:
                    print ('修改成功',msg)
                elif result == False:
                    print('未做修改',msg)
                else:
                    print('未知错误')
            elif choice == '2':
                result,msg = shop_interface.del_shop(login_stat)
                if result == True:
                    print ('修改成功',msg)
                elif result == False:
                    print('未做修改',msg)
                else:
                    print('未知错误')
        elif choice == 'clear':
            result, msg = shop_interface.clear_shop(login_stat)
            if result == True:
                print('修改成功', msg)
            elif result == False:
                print('未做修改', msg)
            else:
                print('未知错误')
# 10、管理员功能
@common.login_verify
def admin_hash():
    admin.admin_task()

func_dict = {
    '1':rigister,
    '2':login,
    '3':check_balance,
    '4':withdraw,
    '5':repay,
    '6':transfer,
    '7':check_flow,
    '8':shopping,
    '9':check_shop_car,
    '10':admin_hash
}

# 视图主程序:
def run():
    while True:
        print("""            
        1、注册功能
        2、登录功能
        3、查看余额
        4、提现功能
        5、还款功能
        6、转账功能
        7、查看流水
        8、购物功能
        9、查看购物车
        10、管理员功能
        """)
        user_input = input('请根据编号输入您要使用的服务:>>>').strip()
        if user_input not in func_dict:
            print('您的输入有误,请重新输入:')
            continue

        func_dict.get(user_input)()

if __name__ == "__main__":
    run()