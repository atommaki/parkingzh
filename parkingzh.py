#!/usr/bin/python2.7

import feedparser
import pprint
import re
import time

python_wiki_rss_url = "http://www.pls-zh.ch/plsFeed/rss"

feed = feedparser.parse( python_wiki_rss_url )
timestamp=int(time.time())
parking={}
#pp = pprint.PrettyPrinter(indent=2)

regex_int=re.compile('^[0-9]+$')

total=0
for i in feed["items"]:
#  print "------------------------------------"
#  pp.pprint(i)
#  print "------------------------------------"
  free=i["summary"].split(" ")[-1]
  title=i["title"].split("/")[0].rstrip().replace(' ','_').encode('utf-8')
  if regex_int.match(free):
    parking[title]=int(free)
    total=total+int(free)
  else:
    parking[title]=None


parking['Total']=total

for i in sorted(parking):
  print timestamp,
  print ";",
  print i,
  print ";",
  print parking[i]

