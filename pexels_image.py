import requests
import os
import time

base_path = os.path.abspath(".")
save_path = os.path.join(base_path, "pexels")
proxies = {"http:": "http://127.0.0.1:8087",
           "https": "https://127.0.0.1:8087"} #访问翻墙网站需要设置的代理

# url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOoFkU7EkPUcMrKESJD7PmIhUeRWMbYIVtZtiAfzL0CSdxI3bA6Q"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

# response = requests.get(url, headers=headers, proxies=proxies, verify=False)
# print(response.status_code)
# filename = os.path.join(save_path,"test.jpg")
# with open(filename,"wb") as f:
#     f.write(response.content)
smoker_path = os.path.join(save_path,"smokers.txt")
smoking_path = os.path.join(save_path,"smoking.txt")
with open(smoking_path, "r") as f:
    smoking_data = f.readlines()
smoking_list = [smoking_url.strip() for smoking_url in smoking_data]

with open(smoker_path, "r") as f:
    content = f.readlines()
content_list = [smoker_url.strip() for smoker_url in content]
smoking_list.extend(content_list)
print(len(smoking_list))


for url in smoking_list:
    i = smoking_list.index(url)
    print(i)
    time.sleep(2)
    try:
        requests.packages.urllib3.disable_warnings()    #消除verify 的警告
        response = requests.get(url, headers=headers, proxies=proxies, verify=False)
    except Exception as e:
        print(e)
    if response.status_code == 200:
        image = response.content
        image_name = "pexels_{}.jpg".format(i)
        image_dir = os.path.join(save_path,image_name)
        with open(image_dir, "wb") as f:
            f.write(image)
        print("%s图片已经保存" % image_name)


