import urllib.request
import urllib.parse
import urllib.error
import json
import pprint
import dateutil.parser

google_books_api_key = 'AIzaSyDQ-oYsJN2_QOrkh3ebn8IXstfbISozF5s'

def find_book(title=None, author=None):
	possible_books = google_books_by_publish_date(title=title, author=author)
	return possible_books[0]


def google_books_by_publish_date(title=None, author=None):
	url_string = google_books_query_string(title=title, author=author)
	url_request = urllib.request.Request(url_string, method='GET')
	try:
		with urllib.request.urlopen(url_request) as response:
			json_response = response.read()
			google_list = json.loads(json_response)

			results = []
			for book in google_list['items']:
				if 'publishedDate' in book['volumeInfo']:
					book['volumeInfo']['publishedDate'] = dateutil.parser.parse(book['volumeInfo']['publishedDate'])
					results.append(book)

			return sorted(results, key = lambda x : x['volumeInfo']['publishedDate'])


	except urllib.error.URLError as err:
		print('There was an error with your url request', err.strerror)

def google_books_query_string(title=None, author=None):
	query_string = ''
	if title:
		query_string += title
	if author:
		query_string += ' ' + 'inauthor:' + author
	query_string = urllib.parse.quote_plus(query_string, safe=":")
	return 'https://www.googleapis.com/books/v1/volumes?q=' + query_string + '&key=' + google_books_api_key 



#pprint.pprint(find_book(title="flowers_for_algernon", author="keyes"))

#possible_results = google_books_by_publish_date(title="flowers_for_algernon", author="keyes")
#for book in possible_result:
#	print('\n\n\n\n\n\n\n\n\n\n------------------------------------------\n\n\n\n\n\n\n\n\n\n\n')
#	pprint.pprint(book['volumeInfo']['publishedDate'])


