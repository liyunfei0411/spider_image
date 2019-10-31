import requests
import json
import os


class SouGou:
    def __init__(self):
        self.proxy_pool_url = 'http://127.0.0.1:5555/random'
        self.path = os.path.abspath(".")
        self.url = "https://pic.sogou.com/pics"
        self.pages = None
        self.proxy = ""
        self.proxies = {
            'http': 'http://' + self.proxy,
            'https': 'https://' + self.proxy,
        }
        self.params = {
            "query": "室内吸烟",
            "mode": 1,
            "start": 48,
            "reqType": "ajax",
            "reqFrom": "result",
            "tn": 0
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_pool_url)
            if response.status_code == 200:
                self.proxy = response.text
                self.proxies["http"] = 'http://' + self.proxy
                self.proxies["https"] = 'https://' + self.proxy
        except ConnectionError:
            return None

    def get_total(self):
        #获取图片总计数量和start
        if self.proxy:
            try:
                response = requests.get(self.url,params=self.params,headers=self.headers, proxies=self.proxies)
                if response.status_code == 200:
                    json_str = response.content.decode("GBK")
                    json_dict = json.loads(json_str)
                    total_str = json_dict["totalItems"]
                    total_list = total_str.split(",")
                    total = int("".join(total_list))
                    print("图片数量：", total)
                    if total % 48 == 0:
                        self.pages = int(total/48)
                    else:
                        self.pages = int(total/48) + 1
                    print("总共页数：", self.pages)
                    return None
            except Exception:
                print("代理IP已经被封请重新获取代理IP")
                self.get_proxy()
                print("新的代理IP：", self.proxy)
                self.get_total()
        else:
            print("无法获取代理IP")
            print("查看是否打开IP池，检查IP池是否正常")
            self.get_proxy()
            self.get_total()

    def get_url_list(self, i):
        if self.proxy:
            self.params["start"] = i*48
            try:
                response = requests.get(self.url, params=self.params, headers=self.headers, proxies=self.proxies)
                if response.status_code == 200:
                    json_str = response.content.decode("GBK")
                    json_dict = json.loads(json_str)
                    url_list = json_dict["items"]
                    print("获取了第%d页的图片url列表" % i)
                    return url_list
            except Exception:
                print("代理IP已经被封请重新获取代理IP")
                self.get_proxy()
                print("新的代理IP：", self.proxy)
                self.get_total()
        else:
            print("无法获取代理IP")
            print("查看是否打开IP池，检查IP池是否正常")
            self.get_proxy()
            print("获取到代理IP：", self.proxy)
            self.get_url_list(i)

    def get_image(self, url):
        if self.proxies:
            try:
                response = requests.get(url, headers=self.headers, proxies=self.proxies)
                if response.status_code == 200:
                    return response.content
                else:
                    return None
            except Exception:
                self.get_proxy()
                self.get_image(url)

        else:
            print("无法获取代理IP")
            print("查看是否打开IP池，检查IP池是否正常")
            self.get_proxy()
            print("获取到代理IP：", self.proxy)
            self.get_image(url)

    def save_images(self, url_list):
        for url_dict in url_list:
            url = url_dict["pic_url"]
            content = self.get_image(url)
            if content:
                path = os.path.join(self.path, "images")
                filename = url.split("/")[-1]
                filename = os.path.join(path, filename)
                try:
                    with open(filename,"wb") as f:
                        f.write(content)
                    print(filename, "图片已经爬去写入images中")
                except Exception as e:
                    print("*"*100)
                    print(e)
                    print("*"*100)

    def run(self):
        self.get_proxy()
        print(self.proxy)
        print(self.proxies)
        self.get_total()
        for i in range(50, self.pages+1):
            url_list = self.get_url_list(i)
            self.save_images(url_list)
        print("图片爬去完毕")


if __name__ == '__main__':
    sougou = SouGou()
    sougou.run()

