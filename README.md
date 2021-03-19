# parkingzh: Parking Zurich

parkingzh is a data collection of the available free space in parking garages
of Zurich. The data is collected by multiple hosts since from this RSS feed:
http://www.pls-zh.ch/plsFeed/rss

The actual collected (raw) data is in the parkingzh-data repository, but all
the scripts (for collecting data and preprocessing) and descriptions are in
this repo. The data collection started in December 2016 and still ongoing.

## the data

The raw data collected on multiple hosts from the RSS feed in every minute. The
nodes have downtime therefore the raw data from any node is not very useful and
may be gaps even if you use all the data together.

The raw data is in ";" separated CSV files, where the columns are:
1. time in Unix timestamps in the timezone of Zurich
2. the name of the parking garage (using underscore instead of spaces)
3. free space in the parking garage

Check out the parkingzh-data repo for the raw data and link it into this repo:
```
ln -s /location/of/the/repo/parkingzh-data data
```

## tools

### parkingzh-fetch-data.py
This is the data collector script. Reads from the RSS feed, writes to the
stdout. Check the `crontab.txt` file how it is used on the collector nodes


### preprocessing.py
This script takes the raw data form multiple files merge them together and
separates them by parking garages. It reads from the `data/` directory (or
symlink) and the output goes to the `data/preprocessed` dir. You may want to
use this data instead of the raw one.


