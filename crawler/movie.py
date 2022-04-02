# -*- coding: utf-8 -*-
import time

import requests
from utils.util import get_year_range
from crawler.net import headers, base_url


def get_top100_by_rate():
    movies = []
    url = base_url
    url += "&year_range=" + get_year_range()

    for i in range(5):
        tmp_url = url + "&start=" + str(i * 20)
        print(tmp_url)
        print('获取电影列表')
        # 等待 5 秒，再获取
        time.sleep(5)
        response = requests.get(tmp_url, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]
            movies.extend(data)
        print('获取电影列表完成\n')
    return movies


if __name__ == '__main__':
    print(get_top100_by_rate())
