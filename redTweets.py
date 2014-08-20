#!/usr/bin/env python
#
# redTweets.py: Reduce file used by Hadoop
# Input: stock sentiments as ticker|sentiment pairs, keyed by time (10 minute periods)
# Output: time, ticker, aggregated sun of tweetShift, aggregated count of Tweets, and the text and score of the most
# significant Tweet for the period
import sys
from datetime import datetime

data={}
current_time = '';

class Entry:
    def __init__(self):
        self.sum = 0.0
        self.count = 0
        self.hi_tweet = ''
        self.hi_score = 0.0

    def update(self, tweet, score):
        self.sum += score
        self.count += 1
        if abs(score) > abs(self.hi_score):
            self.hi_tweet = tweet
            self.hi_score = score

def output():
    for ticker in data:
        try:
            entry = data[ticker]
            print '%s,%s,%0.4f,%d,%s,%0.4f' % (current_time, ticker, entry.sum, entry.count,
                                               entry.hi_tweet, entry.hi_score)
        except:
            continue

input = sys.stdin

for line in input:
    try:
        keyVal1 = line.strip().split('\t')
        time = keyVal1[0]
        vals = keyVal1[1].strip().split(',')

        # Keys are in order so a new time means we can output the old time period
        if time != current_time:
            output()
            current_time = time
            data = {}

        # Current tweet
        tweet = vals[0]

        # Aggregate each ticker
        for entry in vals[1:]:
            keyVal2 = entry.split('|')
            ticker = keyVal2[0]
            score = float(keyVal2[1])
            if not ticker in data:
                data[ticker] = Entry()

            entry = data[ticker]
            entry.update(tweet, score)


    except Exception as e:
        print >> sys.stderr, e
        continue

# Output the last time period
output()
