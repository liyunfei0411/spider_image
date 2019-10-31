import os
import requests
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
image_dir = os.path.join(os.path.abspath("."), "newhailuo")


def get_search_url(keyword):
    q = {"q": keyword}
    q_str = urllib.parse.urlencode(q)
    return "https://www.hellorf.com/image/search?" + q_str


def get_image_url(keyword):

    search_url = get_search_url(keyword)
    i = 1
    driver.get(search_url)
    driver.maximize_window()
    time.sleep(5)
    while True:
        xpath = '//*[@id="__next"]/div/main/div/div[3]/div//div/div/figure/a/img'
        time.sleep(5)
        url_element = driver.find_elements_by_xpath(xpath)
        print("第%d页图片" % i)
        for element in url_element:
            url = element.get_attribute('data-src')
            save_image(url)
        try:
            # angle-right > g > g > polygon
            # __next > div > main > div > div.sc-1wssj0-9.sc-187tstn-4.juCkfv > ul > li:nth-child(3) > button
            driver.implicitly_wait(10)
            driver.find_element_by_css_selector('#__next > div > main > div > div.sc-1wssj0-9.sc-187tstn-4.juCkfv > ul > li:nth-child(3) > button > div').click()
            i += 1
            time.sleep(5)
        except Exception as e:
            print(e)
            break


def save_image(url):
    try:
        res = requests.get(url)
        print(res.status_code)
        image = res.content
        image_name = url.split("/")[-1]
        image_path = os.path.join(image_dir, image_name)
        with open(image_path, "wb") as f:
            f.write(image)
        print(url, "图片已经写入")
    except Exception as e:
        print(e)


def main():

    keyword = "吸烟者"
    get_image_url(keyword)

if __name__ == '__main__':
    main()
