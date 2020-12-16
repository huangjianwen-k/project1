"""
购物接口
"""
from db import db_handler
from interface import bank_interface
import time



def shopping_interface(user,shopping_car):
    #计算商品总价
    cost=0
    for price_money in shopping_car.values():
        price,num = price_money
        cost += price * num
    #调用支付接口
    result,msg = bank_interface.pay_interface(user,cost)
    if result:
        return result,msg
    else:
        return False,'未知异常'

def add_shop_car_interface(user,shopping_car):
#1获取当前用户的购物车
    user_dict = db_handler.select(user)
    shopping_car_2=user_dict['shopcar']
#2添加购物车
    #判断当前用户选择的商品是否已存在
    for shop_name, price_number in shopping_car.items():
        if shop_name in  shopping_car_2:
            print(price_number)
            user_dict['shopcar'][shop_name][1] += price_number[1]
            db_handler.save(user_dict)
#如果不是重复的,则更新到商品中
        else:
            user_dict['shopcar'].update(
                {shop_name:price_number}
            )
            print('正在运送至购物车')
            time.sleep(3)
            db_handler.save(user_dict)
    return True,'添加购物车成功'

def check_shopping_car(username):
    user_dict = db_handler.select(username)
    shop_car = user_dict.get('shopcar')
    return shop_car

def change_shop_car(username):
    user_dict = db_handler.select(username)
    shop_car = user_dict.get('shopcar')
    print(shop_car)
    while True:
        shop_name = input('请输入您要修改的商品名称:>>>')
        if shop_name in shop_car:
            choice = input('修改为:>>>')

            if not choice.isdigit():
                print('您输入的数量有误,请重新输入')
                continue
            print('正在进行修改操作....')

            time.sleep(1.5)
            user_dict['shopcar'][shop_name][1] = choice
            user_dict_new = user_dict.get('shopcar')
            db_handler.save(user_dict)

            return True,f'修改成功,当前购物车[{user_dict_new}]'
        else:
            print('请输入购物车中存在的商品')
            continue


def del_shop(username):
    user_dict = db_handler.select(username)
    shop_car = user_dict.get('shopcar')
    print(shop_car)
    while True:
        shop_name = input('请输入您要删除的商品名称:>>>')
        if shop_name in shop_car:
            choice = input('是否确认删除:>>>Y/N')

            if choice == "Y":
                print('正在进行删除操作....')
                time.sleep(1.5)
                del user_dict['shopcar'][shop_name]
                user_dict_new = user_dict.get('shopcar')
                db_handler.save(user_dict)

            return True, f'修改成功,当前购物车[{user_dict_new}]'
        else:
            print('请输入购物车中存在的商品')
            continue

def clear_shop(username):
    user_dict = db_handler.select(username)
    shopping_car = user_dict.get('shopcar')
    print(shopping_car)
    while True:
        choice = input("确定要清空购物者吗小主:").strip()
        if choice not in ('Y','N'):
                print('您的输入有误,请重新输入')
                continue
        if choice == 'Y':
            print('正在清空您的购物车....')
            time.sleep(2.5)
            user_dict['shopcar']={}
            db_handler.save(user_dict)
            return True,'您的购物车已清空'
        elif choice == 'N':
            return False,'用户取消操作'