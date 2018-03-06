# -*- coding:utf-8 -*-

import requests
import json
import  sys


class TransBaidu():
    def __init__(self,query_string):
        self.query_string = query_string
        self.trans_url = 'http://fanyi.baidu.com/basetrans'
        self.dect_url = 'http://fanyi.baidu.com/langdetect'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}

    def get_post_data(self):
        # 进行语言检测
        # 构造请求参数
        data = {
            'query':self.query_string
        }
        # 发送请求，获取响应
        resp = requests.post(self.dect_url,data=data)

        # headers = resp.headers
        # print(headers)

        raw = resp.content.decode()
        # 将jason数据转为字典
        dict = json.loads(raw)
        # 获取语言类型
        lan = dict['lan']
        # print(lan)

        # 准备post_data
        if lan == 'zh':
            post_data = {"query": self.query_string,
                         "from": "zh",
                         "to": "en"}
            return post_data

        if lan == 'en':
            post_data = {"query": self.query_string,
                         "from": "en",
                         "to": "zh"}
            return post_data

    def parse_url(self, post_data):  # 发送请求，获取响应
        resp = requests.post(self.trans_url, post_data, headers=self.headers)
        return resp.content.decode()

    def get_ret(self, html_str):  # 提取数据
        dict_ret = json.loads(html_str)
        ret = dict_ret["trans"][0]["dst"]
        print("{}翻译结果是：{}".format(self.query_string,ret.encode('utf-8')))

    def run(self):
        # 准备data数据
        post_data = self.get_post_data()
        # 发送请求，获取响应
        html_jon = self.parse_url(post_data)
        self.get_ret(html_jon)



if __name__ == '__main__':
    query_string = sys.argv[1]
    trans = TransBaidu(query_string)
    trans.run()

