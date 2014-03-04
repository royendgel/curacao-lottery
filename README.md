[![Build Status](https://travis-ci.org/royendgel/curacao-lottery.png?branch=master)](https://travis-ci.org/royendgel/curacao-lottery)


curacao-lottery
===============

Curacao Lottery drawings analisis

I moved this code to github from my repo at scraperwiki.
This will scrape out all drawings from a local(Curaçao) site and store them in a database.

This is for personal use but if you want to use it: 
* you need to clone this repo
* use pip install requirments.txt 
* Create an empty python file in the same directory 

`import Lottery
lot = Lottery()
res = lot.get_range(start_year=2014, end_year=2014, start_month=01, end_month=01)
print res`

### Trying to use pep8 for best practice(In the new code)

any question : royendgel@gmail.com
