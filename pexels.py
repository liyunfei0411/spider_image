import os

from selenium import webdriver
import time

#输出目录
# OUTPUT_DIR = '/Users/xxxx/Documents/运动'
base_path = os.path.abspath(".")
OUTPUT_DIR = os.path.join(base_path, "pexels")
#关键字数组：将在输出目录内创建以以下关键字们命名的txt文件
SEARCH_KEY_WORDS = ["smoking", "smokers"]
#页数
PAGE_NUM = 100

repeateNum = 0
preLen = 0

def getSearchUrl(keyWord):
    if(isEn(keyWord)):
        return 'https://www.pexels.com/search/' + keyWord + "/"
    else:
        return 'https://www.pexels.com/search/' + keyWord + "/"

def isEn(keyWord):
    return all(ord(c) < 128 for c in keyWord)

# 启动Firefox浏览器
driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

if os.path.exists(OUTPUT_DIR) == False:
    os.makedirs(OUTPUT_DIR)

def output(SEARCH_KEY_WORD):
    global repeateNum
    global preLen

    print('搜索' + SEARCH_KEY_WORD + '图片中，请稍后...')

    # 如果此处为搜搜，搜索郁金香，此处可配置为：http://pic.sogou.com/pics?query=%D3%F4%BD%F0%CF%E3&di=2&_asf=pic.sogou.com&w=05009900&sut=9420&sst0=1523883106480
    # 爬取页面地址，该处为google图片搜索url
    url = getSearchUrl(SEARCH_KEY_WORD);

    # 如果是搜搜，此处配置为：'//div[@id="imgid"]/ul/li/a/img'
    # 目标元素的xpath，该处为google图片搜索结果内img标签所在路径
    xpath = '//div[@id="rg"]/div/div/a/img'
    xpath = "//div[@class='photos']//div//div/article/a[1]/img"

    # 浏览器打开爬取页面
    driver.get(url)

    outputFile = OUTPUT_DIR + '\\' + SEARCH_KEY_WORD + '.txt'
    outputSet = set()

    # 模拟滚动窗口以浏览下载更多图片
    pos = 0
    m = 0 # 图片编号
    i = 0
    # while True:
    for i in range(PAGE_NUM):
        pos += i*600 # 每次下滚600
        js = "document.documentElement.scrollTop=%d" % pos
        driver.execute_script(js)
        time.sleep(10)
        i = i + 1
    for element in driver.find_elements_by_xpath(xpath):
        img_url = element.get_attribute('src')
        if img_url is not None and img_url.startswith('http'):
            outputSet.add(img_url)
    # if preLen == len(outputSet):
    #     if repeateNum == 2:
    #         repeateNum = 0
    #         preLen = 0
    #         break
    #     else:
    #         repeateNum = repeateNum + 1
    # else:
    #     repeateNum = 0
    #     preLen = len(outputSet)
    # if driver.find_element_by_xpath("//*[@id='smb']"):
    #     try:
    #         driver.find_element_by_xpath("//*[@id='smb']").click()
    #         print("显示更多")
    #     except Exception:
    #         print("没有到加载页面")
    # else:
    #     print("没有到数据加载")


    print('写入' + SEARCH_KEY_WORD + '图片中，请稍后...')
    file = open(outputFile, 'a')
    for val in outputSet:
        file.write(val + '\n')
    file.close()

    print(SEARCH_KEY_WORD+'图片搜索写入完毕')
    print(len(outputSet))

for val in SEARCH_KEY_WORDS:
    output(val)

driver.close()