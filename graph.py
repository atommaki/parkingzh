#!/usr/bin/env python3

import re
import tempfile
import subprocess
import os

regex_int=re.compile('^[0-9]+$')
parkingdat='data/host-0ef47f-parkingzh.dat'

big_ones=['Total']
parking_all=[]
with open('parkingzh.capacity','r') as f:
  for line in f:
    parking_all.append(line.split()[0])
    if len(line.split()) > 1 and regex_int.match(line.split()[1]) and int(line.split()[1]) > 249:
      big_ones.append(line.split()[0])

points=1127914
#points=15717
#points=0
#for parking in parking_all:
#for parking in big_ones:
#  regex_line=re.compile('.* ; '+parking+' ; .*')
#  i=0
#  with open(parkingdat,'r') as f:
#    for line in f:
#      if regex_line.match(line):
#        i=i+1
#  if i > points:
#    points=i

print('points = '+str(points))

parking_file={}
print('big ones ', end=' ')
print(len(big_ones))
for parking in big_ones:
  print('  ' + parking)
  regex_line=re.compile('.* ; '+parking+' ; .*')
  parking_file[parking]=tempfile.mktemp()
  with open(parking_file[parking],'w') as out:
    with open(parkingdat,'r') as f:
      for line in f:
        if regex_line.match(line):
          print(line, end=' ', file=out)


print('parking_all ', end=' ')
print(len(parking_all))
zero={}
unknown={}
for parking in parking_all:
  print('  ' + parking)
  zero[parking]=0
  unknown[parking]=0
  regex_line=re.compile('.* ; '+parking+' ; .*')
  with open(parkingdat,'r') as f:
    for line in f:
      if regex_line.match(line):
        free=line.split()[-1]
        if regex_int.match(free):
          if int(free) == 0:
            zero[parking]=zero[parking]+1
        else:
          unknown[parking]=unknown[parking]+1



print(' Parking place                       zero        unknown')
for parking in parking_all:
  print('%30s   ' % parking, end=' ')
  print('%6i' % zero[parking], end=' ')
  print(100*zero[parking]/points)
  print('/%3i) ' % 88, '%', end=' ')
  print('/%3i) ' % int(100*zero[parking]/points), '%', end=' ')
  print('%6i' % unknown[parking], end=' ')
  print('/%3i) ' % int(100*unknown[parking]/points), '%')


gnuplot_file=tempfile.mktemp()
with open(gnuplot_file,'w') as gnuplot:
  print('set xdata time', file=gnuplot)
  print('set timefmt "%s"', file=gnuplot)
  print('set format x "%H:%M"', file=gnuplot)
  print('set yrange[0:]', file=gnuplot)
  print('set grid', file=gnuplot)
  for i in range(1,16):
    if i > 8:
      dt='1'
    else:
      dt='3'
    print('set style line '+str(i)+' dt '+dt, file=gnuplot) #+' lc rgb '+str(i)
  print('plot \\', file=gnuplot)
  i=0
  for parking in big_ones:
    i=i+1
    print('"'+parking_file[parking]+'" u 1:5  w l ls '+str(i)+' title "'+parking.replace('Parkhaus_','').replace('_',' ')+'", \\', file=gnuplot)
  print('', file=gnuplot)
  print('pause -1', file=gnuplot)


print(' -------------- gnuplot file --------------')
subprocess.call(['cat', gnuplot_file])
print(' ------------------------------------------')
subprocess.call(['gnuplot', gnuplot_file])

for parking in big_ones:
  os.remove(parking_file[parking])
os.remove(gnuplot_file)

