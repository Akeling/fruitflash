import warnings
import requests
import json
import re
import xlwings

from collections import Counter

_headers = { }


warnings.filterwarnings("ignore")
# 忽略不安全警告
def get_html(url):
    # 获取请求
    res = requests.get(url).text
    # 将获取的网页json编码字符串转换为python对象
    json_dict = json.loads(res)
    # print(json_dict)
    return json_dict

if __name__ == '__main__':
    url = ;
    get_html(url);