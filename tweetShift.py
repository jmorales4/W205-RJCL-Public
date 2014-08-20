#!/usr/bin/env python
#
# tweetShift.py:  apply tweetShifts to existing files of priceShifts
#
import sys
from datetime import datetime, timedelta
from os import listdir, path
import os

time_format = '%Y-%m-%d %H:%M'
outputDir = 'D:\\TenMinute\\'
inputDir = 'TweetResults'

class FileEntry:
    # Create a FileEntry from Hadoop Reduce output
    def __init__(self, fileline):
        vals = fileline.strip().split(',')
        self.time = vals[0]
        self.ticker = vals[1]
        self.tweetShift = vals[2]
        self.count = vals[3]
        self.tweet = vals[4]
        self.score = vals[5]

    # Write to the end an existing file
    def writeFile(self):
        filename = outputDir + self.ticker + '_' + self.time.replace(' ', '_').replace(':', '') + '.twp'
        if os.path.isfile(filename):
            with open(filename, 'a') as f:
                f.write(',%s,%s,%s,%s\n' % (self.tweetShift, self.count, self.tweet, self.score))
        else:
            print '!!! Missing File: ' + filename

# Walk the inputDir, read each line in each input file, and write to end of files in outputDir
for root, dirs, files in os.walk(inputDir, topdown=False):
    for file in files:
        try:
            with open(os.path.join(root, file), 'r') as f:
                for line in f:
                    entry = FileEntry(line)
                    entry.writeFile()

        except Exception as e:
            print >> sys.stderr, e
            continue

