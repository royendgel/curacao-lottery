#!/usr/bin/env python
import urllib
import sqlite3
from bs4 import BeautifulSoup
import re
import os
import time

# BEGIN : New code 03/2014 Object oriented way
class Lottery(object):
    def __init__(self, only_new=True, database='lottery.db', new=False):
        self.range_year = 0
        self.range_month = 0
        self.database = database
        self.connection = sqlite3.connect(self.database)
        if only_new == True:
            self.get_range(start_year=2014, end_year=2014, start_month=01, end_month=02)

        self.__createNewdb() if new else None
            # FIXME : need to delete the database if it exists
            
    def get_page(self, year, month):
        page_data_list = []
        url = "http://www.joeblack-lottery.com/wn.php??GameTypeID=1" + \
        str("&Month=") + str(month) + str("&Year=") + str(year)+ str("&Submit=Go")
        page_data = urllib.urlopen(url).read()
        page = BeautifulSoup(page_data)
        for data in  page.find("td").strings:
            page_data_list.append(data.strip())
        return page_data_list

    def __createNewdb(self):
        curs = self.connection.cursor()
        curs.executescript(open('new_db.sql','r').read())

    def get_extracted_page(self, year, month):
        x = self.get_page(year, month)
        return self.extract_data(x)

    def save_extracted_data(self, data):
        # FIXME NEED TO FIND A GOOD WAY TO STORE THE DATES IN DATABASE
        for d in data[0]:
            draw_data = (d['date'], d['pos'], d['number'],)
            self.connection.cursor().execute("INSERT INTO Drawing(Date, Position, Drawing) VALUES(?, ?, ?)", draw_data)
            self.connection.commit()

    def get_all_numbers(self):
        c = self.connection.cursor()
        return c.execute('SELECT * FROM Drawing')

    def extract_data(self, data):
        date_header = 0
        pos = 0
        numbers = []
        for d in data:
            if re.match('^\d\d\S{8}', d):
                date_header = re.findall('^\d\d\S{8}', d)[0]
                pos = 0
            elif len(d) >= 4:
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