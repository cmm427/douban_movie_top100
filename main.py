import os
import time
from crawler.movie import get_top100_by_rate
from crawler.movie_parser import MovieParser
from crawler.movie_doc import MovieDoc
from storage.csv_helper import CsvHelper


def get_result_path():
    # 获取结果文件路径
    path = os.path.join(os.getcwd(), "result")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def run():
    path = get_result_path()
    csv_helper = CsvHelper(path)

    movie_parser = MovieParser()

    # 根据评分获取 top100 链接
    movies = get_top100_by_rate()

    # 电影元素对象列表
    movie_list = []
    for mv in movies:
        url = mv['url']
        title = mv['title']

        # 获取页面文档树
        movie_doc = MovieDoc(url)
        r = movie_doc.get_movie_doc()

        # 解析页面文档树，获取元素信息
        movie_parser.set_link(url)
        movie_parser.set_html_doc(r.text)
        movie = movie_parser.get_movie_info()

        # 将电影列表中的 title 和链接传递到元素对象中
        movie["title"] = title
        movie["url"] = url
        movie_list.append(movie)

        # 等待一段时间，获取下一个电影元素对象
        time.sleep(5)

    # 根据评分排序，解决部分数据排序错误问题
    movie_list.sort(key=lambda item: item['score'], reverse=True)
    print(movie_list)

    # 接爬取结果保存到文件中
    csv_helper.write_row(movie_list)
    csv_helper.close()


if __name__ == '__main__':
    run()
