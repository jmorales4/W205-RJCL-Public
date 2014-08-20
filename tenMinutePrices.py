#!/usr/bin/env python
#
# tenMinutePrices.py:  Read in Hadoop price output and produce individual csv files for each Ticker/10
# minute period containing time, ticker, and price
#
import sys
from datetime import datetime

time_format = '%Y-%m-%d %H:%M'
start = datetime(2014, 8, 4)
finish = datetime(2014, 8, 9)

input = sys.stdin
if len(sys.argv) > 1:
    input = open(sys.argv[1], 'r')

for line in input:
    try:
        vals = line.strip().strip().split(',')
        time = vals[0]
        ticker = vals[1]
        price = vals[2]

        t = datetime.strptime(time, time_format)
        if t < start or t > finish: continue  # Skip

        filename = 'D:\\TenMinute\\' + ticker + '_' + time.replace(' ', '_').replace(':', '')  + '.twp'
        with open(filename, 'w') as f:
            f.write('%s,%s,%s' % (time, ticker, price))

    except Exception as e:
        print >> sys.stderr, e
        continue
