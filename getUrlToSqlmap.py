# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 18:26
# @Author  : ptbs
# @File    : getUrlToSqlmap.py
# @Software: PyCharm
# ---------CODE-------------
import os
# sqlmap安装路径
sqlmap_path = r"C:\Python27\sqlmap"

# 存储目标URL的文本文件路径
urls_file = './tmp/output.txt'

# 读入文档提取url
file_path = './tmp/urls.txt'

# 代理地址
PROXY_HTTP = "http://127.0.0.1:8080"


def extract_urls(file_path, urls_file):
    import re
    from urllib.parse import unquote
    """
    从指定文本文件中提取所有URL连接，并将它们写入到新的文本文件中，每行一个连接。

    :param file_path: 文本文件路径。
    :param urls_file: 输出文本文件路径。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正则表达式匹配完整URL和部分URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, content)

    # 匹配部分URL，并拼接成完整URL
    for line in content.splitlines():
        if 'GET' in line or 'POST' in line:
            url_path = unquote(line.split()[1])              #之前代码没有解析URL编码符号的部分，如果需要解析的话可以使用urllib.parse模块中的unquote()函数来完成
            url_host = line.split()[2].split(':')[-1]
            url_protocol = 'https://' if 'https' in line else 'http://'
            url = url_protocol + url_host + url_path
            url = re.sub(r'HTTP/(1\.0|1\.1|2\.0|3)/', '', url)
            # urls.append(url)
        elif 'Host:' in line:
            url_host = line.split(':')[1].strip()
            if url_host.startswith('http'):
                url_protocol = ''
            else:
                url_protocol = 'http://'
            url = url_protocol + url_host + url_path
            urls.append(url)

    # 将URL写入输出文件中
    with open(urls_file, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')

def run_sqlmap(sqlmap_path, urls_file):
    # 代理地址
    proxy_http = PROXY_HTTP

    # sqlmap命令行参数
    sqlmap_optons = " -m " + urls_file + " --random-agent -v 3 --level 5 --batch " + proxy_http

    # 构造完整的命令
    command = "python " + sqlmap_path + "\sqlmap.py" + sqlmap_optons

    # 执行命令
    os.system(command)

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def welcome():
    clear()
    print("****************************************************")
    print("*                                                  *")
    print("*          欢迎使用getUrlToSqlmap工具               *")
    print("*                                                  *")
    print("****************************************************")
    print("\n")

    print("注意：")
    print("1. 请自行修改sqlmap路径")
    print("2. 请把urls.txt文本放入同目录tmp文件夹")
    print("\n\n")



if __name__ == '__main__':
    welcome()
    y = input("是否先提取文件？Y/N")
    if y == "y" or y == "Y":
        extract_urls(file_path, urls_file)
    y = input("是否运行SQLMAP？Y/N")
    if y == "y" or y == "Y":
        run_sqlmap(sqlmap_path, urls_file)
    else:
        print("bye!")