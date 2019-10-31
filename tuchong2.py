import requests
from lxml import etree
import re
import os
import time
import urllib


proxies = {"http:": "http://127.0.0.1:8087",
           "https:": "https://127.0.0.1:8087"}
title_list = ["吸烟美女", "吸烟女人", "吸烟者", "吸烟的男人", "吸烟男", "吸烟区", "smoker"] #吸烟
url = "http://stock.tuchong.com/search"
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "wluuid=WLGEUST-0882D3B4-E75D-BEA7-2162-FF5B1EDC1336; ssoflag=0; _ga=GA1.3.130634069.1571359703; lang=zh; _ga=GA1.2.832436841.1571813526; _gid=GA1.2.476664302.1571813526; wlsource=tc_pc_home_search; _gid=GA1.3.476664302.1571813526; accessId=e7dfc0b0-b3b6-11e7-b58e-df773034efe4; PHPSESSID=k2rq160hdt7k2nhfq19d3hl7tj; href=http%3A%2F%2Fstock.tuchong.com%2Fsearch%3Fsource%3Dtc_pc_home_search%26term%3D%25E5%2590%25B8%25E7%2583%259F; weilisessionid3=5c69b1abd83828d51a188ab5125009d4; qimo_seosource_e7dfc0b0-b3b6-11e7-b58e-df773034efe4=%E7%AB%99%E5%86%85; qimo_seokeywords_e7dfc0b0-b3b6-11e7-b58e-df773034efe4=; webp_enabled=0; pageViewNum=42",
            "Host": "stock.tuchong.com",
            "Referer": "http://stock.tuchong.com/search?source=tc_pc_home_search&term=%E5%90%B8%E7%83%9F",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
base_path = os.path.join(os.path.abspath("."), "tuchong")
headers_image = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
params = {"term": "吸烟",
          "use": 0,
          "sort": 0,
          "category": 0,
          "page": 1,
          "size": 100,
          "exact": 0,
          "platform": "weili",
          "royalty_free": 0,
          "has_person": 0,
          "gender": 0,
          "samemodel": 0,
          "price": 0,
          "is_need_overwrite": "true",
          "searchId": "b7db1f763d6a4e3599cc20ac79bc2bea",
          }


def get_imageid():
    try:
        time.sleep(5)
        requests.packages.urllib3.disable_warnings()
        res = requests.get(url, headers=headers, params=params, proxies=proxies, verify=False)
        print(res.status_code)
        html = etree.HTML(res.content.decode())
        image_id_str = html.xpath("/html/body/script[4]/text()")
        image_id_list = eval(re.search(r"window\.hits(\s*)=(\s*)(.*)(\s*)window", image_id_str[0]).group(3)[:-1])
        print(len(image_id_list))
        headers_image["Referer"] = res.url
        return image_id_list
    except Exception as e:
        print(e)
        return None


def get_image(image_url):
    try:
        time.sleep(2)
        requests.packages.urllib3.disable_warnings()
        response = requests.get(image_url, headers=headers_image, proxies=proxies, verify=False)
        print(response.status_code, "获得图片内容")
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(e)
        return None


def save_image(image_id_list):
    num = 1
    for image_id in image_id_list:
        print("第%d张图片" % num)
        image_url = "http://icweiliimg9.pstatp.com/weili/ms/" + image_id["imageId"] + ".webp"
        print(image_url)
        image = get_image(image_url)
        if image:
            file_name = image_id["imageId"] + ".jpg"
            file_path = os.path.join(base_path, file_name)
            with open(file_path, "wb") as f:
                f.write(image)
            print(url, "图片已经写入")
        num += 1


if __name__ == '__main__':
    title = "smoker"
    referer = urllib.parse.urlencode({"term": title})
    print(referer)
    headers["Referer"] = "http://stock.tuchong.com/search?source=tc_pc_home_search&" + referer
    headers_image["Referer"] = headers["Referer"]
    for i in range(3, 51):
        params["term"] = title
        params["page"] = i
        print(title, "第%d页" % i)
        image_id_list = get_imageid()
        save_image(image_id_list)