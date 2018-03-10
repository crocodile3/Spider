# -*- coding:utf-8 -*-
import requests
from lxml import etree
import json
import threading
from queue import Queue


class QiuShiSpider():
    def __init__(self):
        self.start_url= "https://www.qiushibaike.com/8hr/page/1/"
        self.domain = "https://www.qiushibaike.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
        self.url_queue = Queue()  # 保存url
        self.html_queue = Queue()  # 保存html字符串
        self.content_queue = Queue()  # 保存提取到的数据

    # 发起请求，获取响应
    def parse_url(self,start_url):
        res = requests.get(start_url, headers=self.headers)
        return res.content.decode()

    # 3.提取数据
    def get_content_list(self,html_str):

        html = etree.HTML(html_str)
        # 以每个帖子为单元，获取本页中所有的帖子（每个element元素代表一个帖子整体）
        content_list = []
        div_list = html.xpath("//div[contains(@class,'article block')]")
        next_url =self.domain + html.xpath("//span[contains(text(),'下一页')]/../@href")[0] if len(html.xpath("//span[contains(text(),'下一页')]/../@href")) else None
        # 遍历div_list,取出每个div

        for div in div_list:
            # print(etree.tostring(div,encoding="utf-8").decode())
            # 再对每个div使用xpath，取出里面的每个内容
            content = {}
            # 楼主
            content["LZ"] = div.xpath(".//h2/text()")[0].replace('\n','') if len(div.xpath(".//h2/text()")[0]) else None
            # print(content)
            content["LZ_head_img"] = div.xpath("./div[@class='author clearfix']/a//img/@src")[0] if len(div.xpath("./div[@class='author clearfix']/a//img/@src")) else None
            content['age'] = div.xpath(".//div[contains(@class,'articleGender')]/text()")[0] if len(div.xpath(".//div[contains(@class,'articleGender')]/text()")) else None
            content['main_text'] = div.xpath(".//div[@class='content']/span/text()")[0].replace("\n",'') if len( div.xpath(".//div[@class='content']/span/text()")) else None
            content['main_img'] = div.xpath(".//div[@class='thumb']//img/@src") if len(div.xpath("//div[@class='thumb']//img/@src")) else None
            content['stats-vote'] = div.xpath(".//span[@class='stats-vote']/i/text()")[0] if len(div.xpath(".//span[@class='stats-vote']/i")) else None
            content['cmt_num'] = div.xpath(".//span[@class='stats-comments']//i/text()")[0] if div.xpath(".//span[@class='stats-comments']//i/text()") else None
            content['cmt_text'] = div.xpath(".//div[@class='main-text']/text()")[0].replace('\n','') if len(div.xpath(".//div[@class='main-text']/text()")) else None
            content['cmt_name'] = div.xpath(".//span[@class='cmt-name']/text()")[0] if len(div.xpath(".//span[@class='cmt-name']/text()")) else None
            content['likenum'] = div.xpath(".//div[@class='likenum']/text()")[1].replace('\n','') if len(div.xpath(".//div[@class='likenum']/text()")) else None
            content_list.append(content)
        return content_list,next_url

    def save_content_dict(self,content_list):
        content_json = json.dumps(content_list,ensure_ascii=False,indent=2)
        with open('qiushi.txt','a') as f:
            f.write(content_json)

    def run(self):
        # 1.url
        # start_url = self.start_url
        # # 2.发起请求，获取响应
        # html_str = self.parse_url(start_url)
        #
        # # 3.提取数据
        # content_list,next_url = self.get_content_list(html_str)
        #
        # # 4.保存数据
        # self.save_content_dict(content_list)
        # print()

        next_url = self.start_url
        # 5.请求下一页地址
        while next_url:
            print(next_url)
            html_str = self.parse_url(next_url)
            content_list, next_url = self.get_content_list(html_str)
            self.save_content_dict(content_list)
if __name__ == '__main__':
    qiushi = QiuShiSpider()
    qiushi.run()