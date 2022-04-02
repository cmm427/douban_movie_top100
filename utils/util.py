# -*- coding: utf-8 -*-
import datetime


def get_year_range():
    current_date_time = datetime.datetime.now()
    year = current_date_time.year
    ten_year_before = int(year) - 10
    return str(ten_year_before) + "," + str(year)
