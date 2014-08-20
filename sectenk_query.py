import solr


def issueQuery(conn, query_text, style):
	return_fields = ['cik','ticker_symbol','company_name','score','sector','ceo_name']
	search_field = 'ten_k_text'
	
	if style == 'exact':
		query = search_field + ':' + '"' + query_text + '"'
		
	elif style == 'or':
		split_query = query_text.split(' ')
		split_query = [search_field + ':' + s for s in split_query]
		query = ' OR '.join(split_query)
	
	return conn.query(query, fields = return_fields)



# create a connection to a solr server
s = solr.SolrConnection('http://ec2-54-187-252-24.us-west-2.compute.amazonaws.com:8983/solr/sectenk')

tweet_text = 'diet coke right meow'

response = issueQuery(s, tweet_text, 'or')


for hit in response.results:
    print hit

