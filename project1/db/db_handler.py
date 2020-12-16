"""
数据处理层
"""

import os
from conf import settings
import json


def select(user_name):
    from conf import settings
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{user_name}.json'
    )
    # 查看用户是否存在

    if os.path.exists(user_path):
        with open(user_path,'r',encoding='utf-8') as file:
            user_dict = json.load(file)
        return user_dict
    return None
def save(user_dict):
    # 存的目标是更方便取出数据
    user_name=user_dict.get('username')
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{user_name}.json'
    )
    with open(user_path, 'w', encoding='utf-8') as file1:
        json.dump(user_dict, file1, ensure_ascii=False)  # ensure_ascii=False 不使用默认编码(二进制)

