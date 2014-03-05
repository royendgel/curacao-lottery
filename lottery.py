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

    def get_number_by_month(self, year, month, number):
        d = self.get_range(year,year,month,month, number)
        return self.get_number_by_something(number, d)

    def get_number_by_year(self, year, number='0000'):
        d = self.get_range(year,year,01,12, number)
        return self.get_number_by_something(number, d)

    def get_number_by_something(self, number, d):
        draw_holder = []
        for n in d[0]:
            if str(n['number']) == str(number):
                draw_holder.append(n)
        if len(draw_holder) <= 0:
            return False
        else:
            return draw_holder

    def save_extracted_data(self, data):
        # FIXME NEED TO FIND A GOOD WAY TO STORE THE DATES IN DATABASE
        for drawing_list in data:
            for d in drawing_list:
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
                    if date == 0:
                        pass
                    else:
                        numbers.append({'number' : d[:4], 'date' : str(date).replace('.',''), 'pos' : pos})
        return numbers

    def web_view(self, port=8000):
        import SimpleHTTPServer
        import SocketServer
        PORT = port

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

        httpd = SocketServer.TCPServer(("", PORT), Handler)

        print "serving at port", PORT
        httpd.serve_forever()

    def search_number(self, database_file='database/basedb.db', number='0000'):
        conn = sqlite3.connect(database_file)
        curs = conn.cursor()
        number = (number,)
        for n in curs.execute("SELECT * FROM Drawing WHERE Drawing=?", number):
            return n

    def generate_numbers(self):
        print 'Generating numbers....'
        numbers = []
        for n in range(10000):
            numbers.append('%4d' %n)
        return numbers

    def generate_not_drawn(self):
        print 'Processing numbers that has not been drawn....'
        x = self.generate_numbers()
        not_drawn = []
        for n in x:
            d = (n,)
            c = self.connection.cursor().execute("SELECT * FROM Drawing WHERE Drawing = ?", d).fetchall()
            if len(c) == 0:
                not_drawn.append(n)
        return not_drawn

    def get_range(self, start_year, end_year, start_month, end_month, day=None):
        data = []
        for year in xrange(start_year, end_year + 1):
            for month in xrange(start_month, end_month + 1):
                data.append(self.get_extracted_page(year, month))
        return data
if __name__ == '__main__':
    x = raw_input('Enter the number >> ')
    lot = Lottery()
    lot.search_number(number=x)