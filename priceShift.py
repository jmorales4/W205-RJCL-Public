#!/usr/bin/env python
#
# priceShift.py:  Read in individual csv files containing price data and caluculate the priceShift
# by comparing the price to the previous price.  Also and fill in missing points by copying previous points.
#
import sys
from datetime import datetime, timedelta
from os import listdir

time_format = '%Y-%m-%d %H:%M'
tenMinutes = timedelta(minutes=10)
dir = 'D:\\TenMinute\\'
start = datetime(2014, 8, 4)
finish = datetime(2014, 8, 9)

class FileEntry:
    def __init__(self, tm, ticker, price):
        self.ticker = ticker
        self.time = tm
        self.price = price
        self.priceShift = 0.0

    @classmethod
    def initFromPrevious(cls, previous):
        return cls(previous.time + tenMinutes, previous.ticker, previous.price)

    @classmethod
    def initFromFileLine(cls, line):
        vals = line.strip().split(',')
        return cls(datetime.strptime(vals[0], time_format), vals[1], float(vals[2]))

    # Output csv files with time, ticker, price and priceShift
    def writeFile(self):
        filename = dir + self.ticker + '_' + \
                   self.time.strftime(time_format).replace(' ', '_').replace(':', '') + '.twp'
        with open(filename, 'w') as f:
            f.write('%s,%s,%0.2f,%0.2f' % (self.time.strftime(time_format), self.ticker, self.price, self.priceShift))

filenames = listdir(dir)
previous_entry = None
current_entry = None

# Write files until finish time
def runOutEntry(entry):
    while entry.time < finish:
        entry = FileEntry.initFromPrevious(entry)
        entry.writeFile()

for filename in filenames:
    try:
        with open(dir + filename, 'r') as f:
            # Just one line
            for line in f:
                current_entry = FileEntry.initFromFileLine(line)
                break

            # If the ticker symbol changed, run out the previous ticker symbol
            if previous_entry is not None and current_entry.ticker != previous_entry.ticker:
                runOutEntry(previous_entry)
                previous_entry = None

            # If there is no previous entry, calculate the previous  entry from the current entry
            if previous_entry is None:
                previous_entry = FileEntry.initFromPrevious(current_entry)
                previous_entry.time = start
                previous_entry.writeFile()

            # Fill in any gaps
            while (current_entry.time - previous_entry.time) > tenMinutes:
                previous_entry = FileEntry.initFromPrevious(previous_entry)
                previous_entry.writeFile()

            # Write current entry and move to next
            current_entry.priceShift = current_entry.price - previous_entry.price
            current_entry.writeFile()
            previous_entry = current_entry

    except Exception as e:
        print >> sys.stderr, e
        continue

# Run out lst entry to finish time
runOutEntry(current_entry)
