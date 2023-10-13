import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

def is_int(value):
    """Check if a string can be converted to an integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_int(value):
    """Check if a string can be converted to an integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False

class LianjiaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def fetch_prices(self, province_codes, city_codes, keyword):
        province_codes = province_codes[:-1]
        city_codes = city_codes[:-1]
        if province_codes in {"北京", "天津", "上海", "重庆"}:
            text = province_codes
        else:
            text = city_codes

        # 尝试第一种 URL（缩写）
        dizhi = ''.join([item[0] for item in lazy_pinyin(text)])
        url = f'https://{dizhi}.lianjia.com/xiaoqu/rs{keyword}/'
        response = requests.get(url=url, headers=self.headers)

        # 如果第一种 URL 失败，尝试第二种 URL（全称）
        if response.status_code != 200:
            dizhi = ''.join(lazy_pinyin(text))
            url = f'https://{dizhi}.lianjia.com/xiaoqu/rs{keyword}/'
            response = requests.get(url=url, headers=self.headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            prices_by_css = soup.select(
                'body > div.content > div.leftContent > ul > li > div.xiaoquListItemRight > div.xiaoquListItemPrice > div.totalPrice > span')
            valid_prices=[int(price.get_text()) for price in prices_by_css if is_int(price.get_text())]
            if valid_prices:  # 如果存在有效的价格，返回第一个，否则返回None
                return valid_prices[0]
            else:
                print("No valid prices found")
                return None

        else:
            print("Failed to retrieve the page")
            return None
# a="杭州市"
# b=LianjiaScraper()
# aaa=b.fetch_prices("浙江省",a,"号院")
# print(aaa)

