[![Build Status](https://travis-ci.org/royendgel/curacao-lottery.png?branch=master)](https://travis-ci.org/royendgel/curacao-lottery)


curacao-lottery
===============

Curacao Lottery drawings analysis

I moved this code to github from my repo at scraperwiki.
This will scrape out all drawings from a local(Curaçao) site and store them in a database.

This is for personal use it : 
* you need to clone this repo
* use pip install requirments.txt or cargo build ( FOR RUST )

#### Now in Rust !! 

####Requirments
Python 2.7

example in the shell using interactive python: 
```python
import Lottery
lot = Lottery()
res = lot.get_range(START_YEAR=2014, END_YEAR=2014, start_month=01, end_month=01)
print res
```

Or from the command line do the following :

```shell
from lottery import Lottery 
x = Lottery(new=True)
x.save_extracted_data(x.get_range(2002,2014,01,12))
```
