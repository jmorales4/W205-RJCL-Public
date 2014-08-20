#
# sectenk_ingest.py:  Retrieve SEC 10k files from S3 and import into Solr
#

import solr
import simplejson
from BeautifulSoup import BeautifulSoup
import urllib2
import string


def clean_strip(item):
    item['cik'] = str(item['cik'])

    for key in item:
        item[key] = unicode(item[key]).strip()
        item[key] = ''.join(s for s in item[key] if s in string.printable)

    return item


# Start by wiping the existing document catalog in Solr
urllib2.urlopen(
    'http://ec2-54-186-141-116.us-west-2.compute.amazonaws.com:8983/solr/sectenk/update?stream.body=<delete><query>*:*</query></delete>')
urllib2.urlopen(
    'http://ec2-54-186-141-116.us-west-2.compute.amazonaws.com:8983/solr/sectenk/update?stream.body=<commit/>')


# Create a connection to a solr server
s = solr.Solr('http://ec2-54-186-141-116.us-west-2.compute.amazonaws.com:8983/solr/sectenk')

f = open('companies.json', 'r')
json_data = simplejson.loads(f.read())
f.close

counter = 0
for item in json_data:
    print 'Importing: ' + item['company_name']

    item = clean_strip(item)
    counter += 1


    # Grab 10-K from Lisa's S3 bucket
    ten_k_url = 'http://10k-clean-data.s3.amazonaws.com/' + item['html_file_name']
    ten_k_url = ten_k_url.replace(".txt", "-clean.txt")
    print ten_k_url

    try:
        response = urllib2.urlopen(ten_k_url)
    except Exception, e:
        print "ERROR: Failed to retrieve 10-K document for " + item['company_name'] + "(" + ten_k_url + ")"
        continue

    html = response.read()
    soup = BeautifulSoup(html)
    item['ten_k_text'] = ''.join(soup.findAll(text=True)).strip()
    item['ten_k_text'] = item['ten_k_text'].replace("\0", " ")
    item['ten_k_text'] = ''.join(s for s in item['ten_k_text'] if s in string.printable)

    try:
        s.add(item)
        s.commit()
    except Exception, e:
        print "ERROR: Failed on add document to Solr for " + item['company_name']
        continue


