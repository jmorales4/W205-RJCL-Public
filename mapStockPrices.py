#!/usr/bin/env python
#
# mapStockPrices.py: Map file used by Hadoop
# input = stock quote file
# output key = time rounded down to nearest 10 minutes
# output val = csv of ticker|price pairs
#
import sys
from datetime import datetime, timedelta

prices = {}

input = sys.stdin
for line in input:
    try:
        # StockQuote schema and sample line
        #
        # 0 Symbol|1 Company Name|2 Last Price|3 Last Trade Date|4 Last Trade Time|5 Change|6 Percent Change| ...
        # A|Agilent Technolog|56.07|8/1/2014|4:04pm|-0.02|-0.04%|1601356|1808860|N/A|N/A|56.09|55.77| ...

        line = line.strip()
        words = line.split('|')
        if len(words) < 5: continue  # not enough data in this line, ignore

        ticker = words[0]
        if ticker == '0 Symbol': continue  # header row

        price = words[2]

        t = datetime.strptime(words[3] + ' ' + words[4], '%m/%d/%Y %I:%M%p')
        nearest10Minutes = (t.minute / 10) * 10  # time rounded down to nearest 10 minutes
        t = t.replace(minute=nearest10Minutes) + timedelta(hours=4)
        trade_time = t.strftime('%Y-%m-%d %H:%M')

        if not trade_time in prices:
            prices[trade_time] = []

        # Build up a price list of ticker|price pairs for all stocks for each 10 minute period
        priceList = prices[trade_time]
        priceList.append(ticker + '|' + price);

    except:
        continue

# Emit the price lists: key = time val = csv of ticker|price pairs
for trade_time in prices:
    priceList = prices[trade_time]
    print '%s\t%s' % (trade_time, ','.join(priceList))

