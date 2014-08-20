#!/usr/bin/env python
#
# redStockPrices.py: Reduce file used by Hadoop
# Input: stock prices as ticker|price pairs, keyed by time
# Output: time, ticker, value csv lines
#
import sys
from datetime import datetime

prices={}
current_time = '';

def output():
    for ticker in prices:
        try:
            print '%s,%s,%s' % (current_time, ticker, prices[ticker])
        except:
            continue

input = sys.stdin

for line in input:
    try:
        keyVal1 = line.strip().split('\t')
        time = keyVal1[0]
        vals = keyVal1[1].strip().split(',')

        # Since the keys are ordered, if we get a new time, can output the old time period
        if time != current_time:
            output()
            current_time = time
            prices = {}

        # Build a map with stock tickers and prices for output
        for entry in vals:
            keyVal2 = entry.split('|')
            ticker = keyVal2[0]
            price = keyVal2[1]
            prices[ticker] = price

    except:
        continue

# Output the last time period
output()
