[![Build Status](https://travis-ci.org/royendgel/curacao-lottery.png?branch=master)](https://travis-ci.org/royendgel/curacao-lottery)


curacao-lottery
===============

Curacao Lottery drawings analysis

I moved this code to github from my repo at scraperwiki.
This will scrape out all drawings from a local(Curaçao) site and store them in a database.

This is for personal use but if you want to use it: 
* you need to clone this repo
* use pip install requirments.txt 
* Create an empty python file in the same directory 

example : 
	import Lottery
	lot = Lottery()
	res = lot.get_range(start_year=2014, end_year=2014, start_month=01, end_month=01)
	print res

Or from the command line do the following :
	>>> from lottery import Lottery 
	>>> x = Lottery(new=True)
	>>> x.save_extracted_data(x.get_range(2002,2014,01,12))

ISSUES : 
need to implement formating like %4d for digits that contains leading zero's I had it before in the old code 

any question : royendgel@gmail.com
