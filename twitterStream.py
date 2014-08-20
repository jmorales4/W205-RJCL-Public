# ! /usr/local/bin/python
#
# twitterStream.py: Connect to the Twitter Stream API using Tweepy,
# create 1000 tweet files, and store in Amazon S3 using Boto
#

from tweepy.streaming import StreamListener
from twitterCredentials import *
from awsCredentials import *
from time import gmtime, strftime
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys
import os

class TwitterStream(StreamListener):
    file = None
    count = 0
    s3 = None

    def __init__(self):
        StreamListener.__init__(self)
        self.s3 = S3Connection(aws_access_key, aws_secret_key)
        self.start_new_tweet_file()


    def start_new_tweet_file(self):
        old_file = self.file

        filename = strftime("%Y%m%d%H%M%S.tweets", gmtime())
        self.file = open(filename, "w")
        self.count = 0

        print filename

        if old_file is not None:
            old_file.close()
            self.post_to_s3(old_file.name)

    def on_data(self, data):
        try:
            self.file.write(data[:-1])
            self.count += 1
            if self.count >= 1000:
                self.start_new_tweet_file()
            return True

        except Exception, e:
            pass

    def post_to_s3(self, filename):
        bucket = self.s3.get_bucket('rjcl-tweets')
        entry = Key(bucket)
        entry.key = filename
        b = entry.set_contents_from_filename(filename)
        print "{}: wrote {} bytes to s3".format(filename, b)
        os.remove(filename)

if __name__ == '__main__':
    print "Startup"
    while True:
        try:
            stream1 = tweepy.Stream(auth, TwitterStream())
            stream1.sample()
        except:
            print "Unexpected error:", sys.exc_info()[0]

    print "Shutdown"