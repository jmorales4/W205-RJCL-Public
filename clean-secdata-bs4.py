#! /usr/local/bin/python
__author__ = 'lkirch'
#
# clean-secdata-bs4.py: Python script that uses BeautifulSoup to clean HTML from SEC 10K files
#

import codecs
import os

inputDir = 'data/'
outputDir = '../clean/'

from bs4 import BeautifulSoup, Tag

# Vasilis http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
def stripHtmlTags(self, htmlTxt):
    if htmlTxt is None:
        return None
    else:
        return ' '.join(BeautifulSoup(htmlTxt).findAll(text=True))

if __name__ == '__main__':
    for root, dirs, files in os.walk('/Users/lkirch/PycharmProjects/convertSECdatatoJSON/data/'):
        for name in files:
            print("Processing Input File: " + name)
            outputFile = name.rstrip('.txt') + '-clean.txt'
            print("Output File Will Be: " + outputFile)
            with codecs.open('data/' + name, 'r', encoding='utf-8') as sec_file, \
                    codecs.open('clean/' + outputFile, 'w+', encoding='utf-8') as clean_file:
                clean_data = stripHtmlTags(sec_file, sec_file)
                clean_data2 = stripHtmlTags(clean_data, clean_data)
                clean_file.write(clean_data2)
