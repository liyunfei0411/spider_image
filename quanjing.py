import random
import requests
import time
import json
import os
import urllib

proxies = {"http:": "http://127.0.0.1:8087",
           "https:": "https://127.0.0.1:8087"}
url = "https://www.quanjing.com/Handler/SearchUrl.ashx"
params = {"t": 5427,
        "callback": "searchresult",
        "q": "吸烟",
        "stype": 1,
        "pagesize": 100,
        "pagenum": 1,
        "imageType": 2,
        "fr": 1,
        "sortFlag": 1,
        "_": 1571886089547}
headers = {"Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "BIGipServerpool_web_ssl=2957748416.47873.0000; Hm_lvt_c01558ab05fd344e898880e9fc1b65c4=1571360314,1571884843; qimo_seosource_578c8dc0-6fab-11e8-ab7a-fda8d0606763=%E7%BB%94%E6%AC%8F%E5%94%B4; qimo_seokeywords_578c8dc0-6fab-11e8-ab7a-fda8d0606763=; accessId=578c8dc0-6fab-11e8-ab7a-fda8d0606763; pageViewNum=9; Hm_lpvt_c01558ab05fd344e898880e9fc1b65c4=1571885900",
            "Host": "www.quanjing.com",
            "Referer": "https://www.quanjing.com/search.aspx?q=%E5%90%B8%E7%83%9F",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}
headers_image = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
base_path = os.path.join(os.path.abspath("."), "quanjing")
title_list = ["吸烟男人", "吸烟女人", "吸烟东方人", "吸烟老人", "吸烟成年","吸烟"]


def get_url_list(i):
    now_time = int(time.time())
    t = int(random.random()*10000)
    params["pagenum"] = i
    params["t"] = t
    params["_"] = now_time
    try:
        time.sleep(5)
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, params=params, proxies=proxies, verify=False)
        if response.status_code == 200:
            url_str = response.content.decode()[13:-1]
            url_list = json.loads(url_str)["imglist"]
            return url_list
    except Exception as e:
        print(e)
        return None


def get_image(url):
    try:
        time.sleep(2)
        requests.packages.urllib3.disable_warnings()
        res = requests.get(url, headers=headers_image, proxies=proxies, verify=False)
        if res.status_code == 200:
            return res.content
    except Exception as e:
        print(e)
        return None


def save_image(url_list):
    num = 1
    for url_dict in url_list:
        print("第%d个图片" % num)
        url = url_dict["imgurl"]
        image = get_image(url)
        if image:
            file_name = url.split("/")[-1]
            file_path = os.path.join(base_path, file_name)
            with open(file_path, "wb") as f:
                f.write(image)
            print(url, "图片已经写入")
        num += 1


def main():
    for title in title_list:
        print(title, "图片开始下载")
        params["q"] = title
        q = {"q": title}
        headers["Referer"] = "https://www.quanjing.com/search.aspx?" + urllib.parse.urlencode(q)
        i = 27
        while True:
            print("第%d页" % i)
            url_list = get_url_list(i)
            if url_list:
                save_image(url_list)
            else:
                break
            i += 1


if __name__ == '__main__':
    main()
