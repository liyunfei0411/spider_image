import requests
from proxypool.setting import TEST_URL


PROXY_POOL_URL = 'http://localhost:5555/random'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


proxy = get_proxy()
print(proxy)

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

print(TEST_URL)
response = requests.get(TEST_URL, headers=headers, proxies=proxies, verify=False)
if response.status_code == 200:
    print('Successfully')
    print(response.text)