#!/usr/bin/env python3

import feedparser
import re
import time

python_wiki_rss_url = "http://www.pls-zh.ch/plsFeed/rss"

feed = feedparser.parse( python_wiki_rss_url )
timestamp = int(time.time())
parking = {}

regex_int = re.compile('^[0-9]+$')

total = 0
for rss_item in feed['items']:
  free_n = rss_item['summary'].split(' ')[-1]
  pname  = rss_item['title'].split('/')[0].rstrip().replace(' ','_')
  if regex_int.match(free_n):
    parking[pname] = int(free_n)
    total = total+int(free_n)
  else:
    parking[pname] = None


parking['Total'] = total

for pname in sorted(parking):
  print(f'{timestamp} ; {pname} ; {parking[pname]}')

