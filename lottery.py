#!/usr/bin/env python
import urllib
import sqlite3
from bs4 import BeautifulSoup
import re

# BEGIN : New code 03/2014 Object oriented way
class Lottery(object):
    def __init__(self, only_new=True, database='lottery.db'):
        self.range_year = 0
        self.range_month = 0
        self.database = database
        if only_new == True:
            self.get_range(start_year=2014, end_year=2014, start_month=01, end_month=02)

    def get_page(self, year, month):
        page_data_list = []
        url = "http://www.joeblack-lottery.com/wn.php??GameTypeID=1" + \
        str("&Month=") + str(month) + str("&Year=") + str(year)+ str("&Submit=Go")
        page_data = urllib.urlopen(url).read()
        page = BeautifulSoup(page_data)
        for data in  page.find("td").strings:
            page_data_list.append(data.strip())
        return page_data_list

    def __connect_db(self):
        self.connection = sqlite3.connect(self.database)

    def save_in_db(self):
        self.__connect_db()

    def get_extracted_page(self, year, month):
        x = self.get_page(year, month)
        return self.extract_data(x)

    def extract_data(self, data):
        date_header = 0
        pos = 0
        numbers = []
        for d in data:
            if re.match('^\d\d\S{8}', d):
                date_header = re.findall('^\d\d\S{8}', d)[0]
                pos = 0
            if len(d) >= 4:
                if re.match('\d\d\d\d',d):
                    pos += 1
                    date = date_header
                    numbers.append({'number' : d[:4], 'date' : str(date).replace('.',''), 'pos' : pos})
        return numbers

    def get_range(self, start_year, end_year, start_month, end_month, day=None):
        data = []
        for year in xrange(start_year, end_year + 1):
            for month in xrange(start_month, end_month + 1):
                data.append(self.get_extracted_page(year, month))
        return data