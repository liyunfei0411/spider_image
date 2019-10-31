import requests
from lxml import etree
import os
import time


proxies = {"http:": "http://127.0.0.1:8087",
           "https:": "https://127.0.0.1:8087"}
headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36"}
image_dir = os.path.join(os.path.abspath("."), "hailuo")

page = 513
while True:
    try:
        url = "https://m.hellorf.com/search?keyword=%E5%90%B8%E7%83%9F%E7%94%B7%E4%BA%BA&page=" + str(page)
        print("第%d页" % page)
        print("*"*100)
        time.sleep(2)
        response = requests.get(url, headers=headers, proxies=proxies)
        print(response.status_code)
        content = response.content.decode()
        html = etree.HTML(content)
        url_list = html.xpath("//div//img/@src")
        print(len(url_list))
        for image_url in url_list:
            time.sleep(1)
            res = requests.get(image_url, headers=headers, proxies=proxies)
            image = res.content
            image_name = image_url.split("/")[-1]
            image_path = os.path.join(image_dir, image_name)
            with open(image_path, "wb") as f:
                f.write(image)
            print(image_url, "已经写入")
    except Exception as e:
        print(e)
    finally:
        page += 1
