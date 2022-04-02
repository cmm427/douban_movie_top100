# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from crawler import entity


class MovieParser:
    __link = ""
    __soup = ""
    __movie = None
    __NOT_FOUND = "页面不存在"
    __html_doc = ""

    def __set_bs_soup(self):
        self.__soup = BeautifulSoup(self.__html_doc, "html.parser")

    def set_html_doc(self, html_doc):
        self.__html_doc = html_doc

    def set_link(self, link):
        self.__link = link

    def __is_404_page(self):
        if self.__html_doc.find(self.__NOT_FOUND) != -1:
            return True
        if len(self.__html_doc) < 500:
            return True
        return False

    # 获取片名
    def __get_title(self):
        try:
            info = self.__soup.find('span', property="v:itemreviewed")
            self.__movie["title"] = info.text
        except Exception as e:
            print('获取片名', e)

    # 获取导演
    def __get_directors(self):
        try:
            info = self.__soup.find('a', {'rel': 'v:directedBy'})
            self.__movie['directors'] = info.text
        except Exception as e:
            print('获取导演', e)

    # 获取编剧
    def __get_scriptwriters(self):

        temp_str = self.__movie['scriptwriters']
        flag_position = temp_str.rfind('>')

        if flag_position > -1:
            self.__movie['scriptwriters'] = temp_str[flag_position + 1: len(temp_str)]

    # 获取主演
    def __get_actors(self):
        try:
            info = self.__soup.find_all('a', {'rel': 'v:starring'})
            info = MovieParser.__compose_list(info)
            self.__movie['actors'] = MovieParser.__trim_last_comma(info)
        except Exception as e:
            print('获取主演', e)

    # 获取类型
    def __get_types(self):
        try:
            info = self.__soup.find_all('span', {'property': 'v:genre'})
            info = MovieParser.__compose_list(info)
            self.__movie['types'] = MovieParser.__trim_last_comma(info)
        except Exception as e:
            print('获取类型', e)

    # 获取地区
    def __get_region(self):
        try:
            info = self.__soup.find('span', text='制片国家/地区:').nextSibling[1:]
            self.__movie['release_region'] = info
        except Exception as e:
            print('获取地区', e)

    # 获取上映时间
    def __get_release_date(self):
        try:
            info = self.__soup.find_all('span', {'property': 'v:initialReleaseDate'})
            info = MovieParser.__compose_list(info)
            self.__movie['release_date'] = MovieParser.__trim_last_comma(info)
        except Exception as e:
            print('获取上映时间', e)

    # 获取评分
    def __get_score(self):
        try:
            info = self.__soup.find('strong', {'property': 'v:average'})
            self.__movie['score'] = info.text
        except Exception as e:
            print('获取评分', e)

    # 获取短评数
    def __get_short_comments(self):
        try:
            info = self.__soup.find('a', {'href': self.__link + "comments?status=P"})
            self.__movie["short_comments"] = info.text
        except Exception as e:
            print('获取短评数', e)

    # 获取影评数
    def __get_movie_comments(self):
        try:
            info = self.__soup.find('a', {'href': 'reviews'})
            self.__movie['movie_comments'] = info.text
        except Exception as e:
            print('获取影评数', e)

    @staticmethod
    def __compose_list(list_):
        result = ''
        for item in list_:
            result += item.text + ','
        return result

    @staticmethod
    def __trim_last_comma(string):
        if not string:
            return None

        if string[-1] == ',':
            return string[: -1]

    def get_movie_info(self):
        self.__set_bs_soup()
        self.__movie = entity.movie.copy()

        # self.__get_title()
        self.__get_actors()
        self.__get_directors()
        self.__get_scriptwriters()
        self.__get_types()
        self.__get_region()
        self.__get_release_date()
        self.__get_score()
        self.__get_short_comments()
        self.__get_movie_comments()

        print(self.__link, "元素信息：", self.__movie)
        return self.__movie
