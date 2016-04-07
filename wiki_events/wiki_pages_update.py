import requests
from page_parser import WikiPageParser
from threading import Thread

class UpdateWikipediaPagesData(Thread):
	"""
	Class used for fetching and storing data from Wikipedia and refreshing at 2 hours intervals
	"""
	def __init__(self, mongodb):
		Thread.__init__(self)
		self.mongodb = mongodb
	
	def	run(self):
		while True:
			"""
			Selecting all pages in 'Days_of_the_year' category
			"""
			baseurl = 'https://en.wikipedia.org/w/api.php'
			params = '?action=query&list=categorymembers&cmtitle=Category:Days_of_the_year&format=json&cmlimit=400'
			try:
				result = requests.get(baseurl + params)
			except requests.HTTPError as e:
				print('Http error. Error code: ', e.code)
			except requests.URLError as e:
				print('Url error. Reason: ', e.reason)
			except:
				print('Could not fulfill the request')	
			else:
				pages = result.json()['query']['categorymembers']
				self.update_events_collection(pages)

			time.sleep(7200)

	def update_events_collection(self, pages):
		"""
		Updating MongoDB events collection
		"""
		page_titles = [ page['title'] for page in pages ]
		for page in page_titles:
			parser = WikiPageParser(page)	
			self.mongodb.events_collection.remove({
				"day" : page.lower()
			})
			event_list = parser.get_event_list()
				
			for event in event_list:
				self.mongodb.events_collection.insert_one(event)
				