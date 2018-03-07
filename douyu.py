# -*- coding:utf-8 -*-
import requests
import re
import time
import json


class DouyuSpider():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
        }

    def get_url_list(self):
        url = 'https://www.douyu.com/gapi/rkc/directory/2_201/3'
        return url

    # 1 获取所有页面的url：pages_url
    def get_pages_url(self):
        pages_url_list = []
        self.pages_url_list = pages_url_list
        for i in range(2):
            url = 'https://www.douyu.com/gapi/rkc/directory/2_201/{}'.format(i + 1)
            pages_url_list.append(url)

        return pages_url_list


    # def get_img_url(self,res_html):
    #     pattern = re.compile(r'^data-original="(.*?)jpg$"')
    #     img_url_list = re.findall(pattern,res_html)
    #     return img_url_list
    def save_image(self,):
        pass


    def run(self):
        # 1 获取所有页面的url：pages_url
        pages_url = self.get_pages_url()
        for page_url in pages_url:
            # 发送请求，获取响应
            response = requests.get(page_url)
            # 获取响应数据
            res_json= response.content.decode()
            # 将json数据转为字符串的形式
            res_dict = json.loads(res_json)
            raw = res_dict['data']['rl']
            pattern = re.compile(r"rs1':\s'(.*?jpg)")
            image_list = re.findall(pattern, str(raw))
            for img_url in image_list:
                res = requests.get(img_url)
                img_data = res.content
                file_name = "%f.jpg" % time.time()
                with open('pic1/' + file_name, 'wb') as f:
                    f.write(img_data)
                    print('%s已完成下载' % file_name)

            # print()
            i = 1
            print('完成第%d页下载' %i)
            i += 1
            print(image_list)

if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()

