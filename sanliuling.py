import requests
import json
import os
import time


class Baidu:
    def __init__(self):
        self.path = os.path.abspath(".")
        self.url = "https://image.so.com/j"
        self.pages = 0
        self.params = {
            "q": "吸烟者",
            "src": "srp",
            "correct": "吸烟者",
            "pn": 60,
            "sn": 75,
            "pd": 1,
            "prevsn": 0,
            "sid": "cb4e8dc41ba704272d53b5730cc7e77a",
            "ran": 0,
            "ras": 6,
            "cn": 0,
            "gn": 0,
            "kn": 15,
            "comm": 1
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    def get_total(self):
        #获取图片总计数量和start
        try:
            response = requests.get(self.url,params=self.params,headers=self.headers)
            if response.status_code == 200:
                json_str = response.content.decode()
                json_dict = json.loads(json_str)
                total= json_dict["total"]
                # total_list = total_str.split(",")
                total = int(total)
                print("图片数量：", total)
                if total % 60 == 0:
                    self.pages = int(total/60)
                else:
                    self.pages = int(total/60) + 1
                print("总共页数：", self.pages)
                return None
        except Exception as e:
            print("*" * 100)
            print(e)
            print("*" * 100)

    def get_url_list(self, i):
        self.params["sn"] = i*75
        self.params["prevsn"] = (i-1)*75
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers)
            if response.status_code == 200:

                json_str = response.content.decode()
                print(json_str)
                json_dict = json.loads(json_str)
                url_list = json_dict["list"]
                print("获取了第%d页的图片url列表" % i)
                return url_list
        except Exception as e:
            print("*" * 100)
            print(e)
            print("*" * 100)

    def get_image(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except Exception as e:
            print("*" * 100)
            print(e)
            print("*" * 100)

    def save_images(self,url_list):
        for url_dict in url_list:
            url = url_dict["img"]
            content = self.get_image(url)
            if content:
                path = os.path.join(self.path, "sanliuling_images")
                filename = url.split("/")[-1]
                filename = os.path.join(path, filename)
                try:
                    with open(filename,"wb") as f:
                        f.write(content)
                    print(filename, "图片已经爬去写入baidu_images中")
                except Exception as e:
                    print("*" * 100)
                    print(e)
                    print("*" * 100)

    def run(self):

        self.get_total()
        time.sleep(1)
        for i in range(1, self.pages+1):
            url_list = self.get_url_list(i)
            self.save_images(url_list)
            time.sleep(1)
        print("图片爬去完毕")


if __name__ == '__main__':
    baidu = Baidu()
    baidu.run()

