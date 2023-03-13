# -*- coding: utf-8 -*-
# @Time    : 2023/3/13 12:00
# @Author  : ptbs
# @File    : geturl.py
# @Software: PyCharm
# ---------CODE-------------
from urllib import parse
import tld    # 读取域名包
import re

# 通过tld 的 get_fld 方法读取主域名
# 读取文件函数
def open_file():
    global file_urls
    file_urls = input("请输入域名文档路径：")
    try:
        f = open(file_urls, "r",encoding='utf-8')
        content = f.readlines()
        f.close()
        urls = []
        for i in range(0, len(content)):
            urls.append(content[i].rstrip('\n'))
        return urls
    except FileNotFoundError:
        print("文件没找到！")
    except PermissionError:
        print("请检查文件权限.")

# 写文件函数 必须出入列表
def write_file(example,filename):
    import os
    dirs = "./tmp/"
    # var_example = [k for k, v in locals().items() if v == example][0]  #可以使用反射机制获取一个对象的属性名称，这个属性名称就是变量的名称。然后，你可以使用str()函数将变量名称转换成字符串形式
    if not os.path.exists(dirs):
        os.mkdir(dirs)
    else:
        f = open(dirs + f'{filename}.txt','w',encoding="utf-8")
        for txt in example:
            f.write(txt + "\n")
        f.close()
        # print("文件./tmp/example.txt 写入成功!")

#使用Python内置的urllib.parse库来解析URL字符串，将其拆分为其组成部分，例如协议、域名、IP地址、端口号和路径。下面是一个示例代码
def parse_url(url):
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    domain = parsed_url.netloc
    if ":" in domain:
        ip_address, port = domain.split(":")
    else:
        ip_address = domain
        port = "80"
    path = parsed_url.path
    return (protocol, ip_address, port, path)




urls = open_file()
domain_urls = []
ip_urls = []
for url in urls:
    url = parse.unquote(url) # 可以通过urllib.parse模块的unquote方法对url地址进行解码
    url = url.split(' ')[0]  # 去掉空格后面的字符
    url = url.split('\t')[0]  # 去制表符
    url = url[::-1].split('\\')[0] #去掉末尾\ 后面的字符
    url = url[::-1] #再反转成正常的域名
    if url[:4] == 'http':
        match = re.search(r'^https?://(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::\d+)?(?:/.*)?$', url)   # 正则方法去掉 为ip为域名的域名
        if not match:
            domain_urls.append(url)
        else:
            ip_urls.append(url)    # IP 的域名单独储存

# print(new_urls)


#写入并输出到./tmp/example.txt  配合 oneforall.py --targets ./example.txt run
example = []
if domain_urls:
    for url in domain_urls:
        ret = tld.get_fld(url,fix_protocol=True)
        example .append(ret)
else:
    print("输入路径有误")
example  = list(set(example))  #set()函数将这个列表转换成集合，并自动去除重复的元素。最后，使用list()函数将集合转换回列表  把域名去重
ip_urls  = list(set(ip_urls))  #把IP域名去重
# print(example)   #测试用

write_file(example,"example")   #普通域名写入 example.txt 配合oneforall
write_file(ip_urls,"ipurls")    #ip域名写入 ipurls.txt 配合oneforall

for url in ip_urls:                         #协议、域名、IP地址、端口号和路径  写入 ./tmp/parseurl.txt
    protocol, ip_address, port, path = parse_url(url)
    f = open('./tmp/parseurl.txt', 'a', encoding="utf-8")
    f.write(f"URL: {url}" + "\n")
    f.write(f"Protocol: {protocol}" + "\n")
    f.write(f"IP Address: {ip_address}" + "\n")
    f.write(f"Port: {port}" + "\n")
    f.write(f"Path: {path}\n\n\n")
