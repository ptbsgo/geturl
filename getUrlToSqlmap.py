# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 18:26
# @Author  : ptbs
# @File    : getUrlToSqlmap.py
# @Software: PyCharm
# ---------CODE-------------
import os
import welcome as wc

dirs = wc.mk_date_dir()

# sqlmap安装路径
sqlmap_path = r"C:\Python27\sqlmap"

# 存储目标URL的文本文件路径
urls_file = dirs + '/output.txt'

# 存储错误URL的文本文件路径
out_err = dirs + '/out_err.txt'

# 读入文档提取url
file_path = './tmp/urls.txt'

# 代理地址
PROXY_HTTP = "http://127.0.0.1:8080"

# 设置全局代理
SET_PROXY = "set ALL_PROXY=http://127.0.0.1:8080"



# 定义一个函数，用于验证链接是否可访问
def validate_url(url):
    import requests
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

# 验证output_file_path文件中的链接是否可访问


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

    err_urls=[]
    # 正则表达式匹配完整URL和部分URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, content)
    for url in urls:
        if not validate_url(url):                    #确认下能否访问
            err_urls.append(url)
            urls.remove(url)
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
            if validate_url(url):                        #确认下能否访问
                urls.append(url)
            else:
                err_urls.append(url)


    # 将URL写入输出文件中
    with open(urls_file, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')

    # 将错误URL写入输出文件err_url.txt
    with open(out_err, 'w', encoding='utf-8') as f:
        for url in err_urls:
            f.write(url + '\n')

def run_sqlmap(sqlmap_path, urls_file,level):
    # 代理地址
    proxy_http = " --proxy=" + PROXY_HTTP

    # 全局代理
    set_proxy = SET_PROXY

    # sqlmap命令行参数
    sqlmap_optons = " -m " + urls_file + " --random-agent -v 3 --level " + level + " --batch " + proxy_http

    # 构造完整的命令
    command = "python " + sqlmap_path + "\sqlmap.py" + sqlmap_optons

    # 执行命令
    os.system(set_proxy)
    os.system(command)






if __name__ == '__main__':
    wc.welcome("getUrlToSqlmap")
    y = input("是否先提取文件？Y/N")
    if y == "y" or y == "Y":
        extract_urls(file_path, urls_file)
    y = input("是否运行SQLMAP？Y/N")
    if y == "y" or y == "Y":
        level = input("请输入sqlmap,level 等级：")
        run_sqlmap(sqlmap_path, urls_file,level)
    else:
        print("bye!")