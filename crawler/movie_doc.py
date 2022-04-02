# -*- coding: utf-8 -*-
import requests
from crawler.net import headers


class MovieDoc:
    def __init__(self, url):
        self.url = url

    def get_movie_doc(self):
        r = requests.get(self.url, headers=headers)
        r.encoding = 'utf-8'
        return r

