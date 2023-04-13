# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 22:32
# @Author  : ptbs
# @File    : run_OneForAll.py
# @Software: PyCharm
# ---------CODE-------------
import os
# OneForAll安装路径
OneForAll_path = r"C:\git\OneForAll"


# 读入文档提取example
file_path = './example.txt'

# 代理地址
SET_PROXY = "set ALL_PROXY=http://127.0.0.1:8080"




def run_OneForAll(OneForAll_path, file_path):
    # 代理地址
    set_proxy = SET_PROXY


    # 构造完整的命令
    command = "py -3 " + OneForAll_path + "\oneforall.py --targets " + file_path + " run"

    # 执行命令
    os.system(set_proxy)
    os.system(command)





if __name__ == '__main__':
    run_OneForAll(OneForAll_path, file_path)