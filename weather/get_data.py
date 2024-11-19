import requests


def main(utl: str):
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        # 'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://weather.niwa.co.nz/',
        # 'Origin': 'https://weather.niwa.co.nz',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        # 'Connection': 'keep-alive',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-site',
    }

    ret = requests.get(url=url, headers=headers)
    if ret.ok:
        print(ret.json())


if __name__ == '__main__':
    url = 'https://api.niwa.co.nz/weather/location/229675266/combined'
    main(url)
