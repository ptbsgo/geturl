# -*- coding: utf-8 -*-
# @Time    : 2023/4/15 17:48
# @Author  : ptbs
# @File    : welcome.py
# @Software: PyCharm
# ---------CODE-------------
import os


# 按当前时间创建文件夹
def mk_date_dir():
    from datetime import datetime

    # 获取当前时间
    now = datetime.now()

    # 格式化时间字符串，作为文件夹名
    folder_name = now.strftime("%Y-%m-%d-%H-%M-%S")

    # 创建文件夹
    os.makedirs(folder_name, exist_ok=True)

    return folder_name


def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def welcome(name):
    clear()
    print("****************************************************")
    print("*                                                  *")
    print("*          欢迎使用",name,"工具               *")
    print("*                                                  *")
    print("****************************************************")
    print("\n\n")

    # print("注意：")
    # print("1. 请自行修改sqlmap路径")
    # print("2. 请把urls.txt文本放入同目录tmp文件夹")
    # print("\n\n")