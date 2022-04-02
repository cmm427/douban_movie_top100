# -*- coding: utf-8 -*-
import csv
import datetime
import os.path


class CsvHelper:
    columns = ['评分', '片名', '导演', '编剧', '主演', '类型', '制片国家/地区', '上映日期', '短评数', '影评数', '链接']

    def __init__(self, path):
        t = datetime.datetime.now()
        result_file = os.path.join(path, "top100_" + t.strftime("%Y%m%d%H%M%S") + ".csv")

        self._csv_file = open(result_file, 'w', newline='', encoding='utf-8-sig')
        self._writer = csv.writer(self._csv_file)
        self._writer.writerow(self.columns)

    def write_row(self, movie_list):
        try:
            for movie in movie_list:
                row = [movie['score'],
                       movie["title"],
                       movie['directors'],
                       movie['scriptwriters'],
                       movie['actors'],
                       movie['types'],
                       movie['release_region'],
                       movie['release_date'],
                       movie['short_comments'],
                       movie['movie_comments'],
                       movie['url']]
                print("row: ", row)
                self._writer.writerow(row)
        except IOError as e:
            print(e)

    def close(self):
        self._csv_file.close()
