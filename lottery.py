#!/usr/bin/env python

import scraperwiki
import urllib
from bs4 import BeautifulSoup
import re

#
# This is an old code that I made with scraperwiki Classic 
# 
numbers = []
numbersnoasali = 0
test = 0 
count = 0
numberasali = 0
for year in xrange(2002,2013):
    test = test + 1 
    print test
    for month in xrange(1,13):
        url = "http://www.joeblack-lottery.com/wn.php??GameTypeID=1" + str("&Month=") + str(month) + str("&Year=") + str(year)+ str("&Submit=Go")
        urlopen = urllib.urlopen(url)
        resultaten = urlopen.read()
        data = BeautifulSoup(resultaten)
        Tabledata = data.find("td")
        TabledataContents = Tabledata.strings
        for TabledataContents in TabledataContents:
            if len(TabledataContents) >= 4:
                if re.match('\d\d\d\d.',TabledataContents): # I repeated two times I know .... I'm a little lazy 
                    count = count + 1
                    prefixf = "wegaresult/resultall.txt"
                    numbers.append(TabledataContents[:4])

for x in ["%04d" % x for x in range(10000)]:
    if x not in numbers:
        numbersnoasali = numbersnoasali + 1 
        noasali = x

for x in ["%04d" % x for x in range(10000)]:
    if x in numbers:
        numberasali = numberasali + 1 
        asali = x
        kuantu = numbers.count(x)

scraperwiki.sqlite.save(unique_keys=["winning"], data={"winning":numbers})
