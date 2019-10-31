import requests
import json
import os
import time


class PsFive:
    def __init__(self):
        self.path = os.path.abspath(".")
        self.url = "https://500px.me/community/searchv2"
        self.pages = 0
        self.params = {
            "orderBy": "alike",
            "key": "smoker",
            "searchType": "photoAndGroup",
            "page": 1,
            "size": 20,
            "type": "json"
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    def get_url_list(self):

        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            json_dict = json.loads(response.content.decode())
            json_list = json_dict["data"]
        return json_list

    def get_image(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            # print(response.content)
            return response.content

    def save_image(self,url_list):
        for url_dict in url_list:
            url = url_dict["url"]["p2"]
            if url:
                time.sleep(5)
                image = self.get_image(url)
                file_path = os.path.join(self.path, "500ps")
                file_name = url.split("/")[-1][:-3]
                filename = os.path.join(file_path,file_name)
                with open(filename, "wb") as f:
                    f.write(image)
                print(url, "图片已经存入")
            else:
                return 1

    def run(self):
        i = 1
        while True:
            print("第%d页" % i)
            self.params["page"] = i
            url_list = self.get_url_list()
            stop = self.save_image(url_list)
            if stop == 1:
                break
            i += 1


if __name__ == '__main__':
    ps = PsFive()
    ps.run()