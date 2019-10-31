import requests
import os
import time
from lxml import etree


base_path = os.path.abspath(".")
save_path = os.path.join(base_path, "visualhunt")
proxies = {"http:": "http://127.0.0.1:8087",
           "https": "https://127.0.0.1:8087"} #访问翻墙网站需要设置的代理

url = "https://visualhunt.com/search/instant/"
params = {
    "q": "smoker",
    "page": 1
}
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}


def get_url_list(data):
    html = etree.HTML(data)
    url_list = html.xpath("//*[@id='layout']/div[3]/div/div[1]/div/a/img/@src")
    url_list2 = html.xpath("//*[@id='layout']/div[3]/div/div[1]/div/a/img/@data-original")
    url_add = list()
    for url in url_list:
        if url.endswith("s=s"):
            url_slice = url[:-4]
            url_add.append(url_slice)
    for url2 in url_list2:
        if url2.endswith("s=s"):
            url2 = url2[:-4]
        url_add.append(url2)
    print(url_add)
    return url_add


def save_image(url):
    try:
        requests.packages.urllib3.disable_warnings()
        res = requests.get(url, headers=headers, proxies=proxies, verify=False)
        if res.status_code == 200:
            image = res.content
            file_name = url.split("/")[-1]
            file_path = os.path.join(save_path, file_name)
            with open(file_path, "wb") as f:
                f.write(image)
            print(url, "图片写入")
    except Exception as e:
        print(e)


def get_html(i):
    params["page"] = i
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, proxies=proxies, params=params, verify=False)
        print(response.status_code)
        if response.status_code == 200:
            html = response.content.decode()
            return html
        else:
            return None
    except Exception as e:
        print(e)
        return None



def run():
    i = 40
    while True:
        html = get_html(i)
        if html:
            print("第%d页" % i )
            url_list = get_url_list(html)
            for url in url_list:
                save_image(url)
        else:
            break
        i += 1


if __name__ == '__main__':

    run()
