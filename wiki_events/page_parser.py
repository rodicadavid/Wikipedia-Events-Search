# -*- coding: utf-8 -*-
from lxml import html, etree
from lxml.html import fromstring, tostring
import urllib

class WikiPageParser:
	"""
	Class for parsing data about events from Wikipedia 
	"""
	def __init__(self, pageTitle):
		self.page = pageTitle
		self.url = "https://en.wikipedia.org/wiki/" + pageTitle
		self.categories = ['Events', 'Births', 'Deaths', 'Holidays_and_observances']
		self.event_list = []

	def select_page_content(self, page_content):
		"""
		Parsing the content of a page and selecting the list of events
		"""
		for el in page_content:
			category = el.get('id')
			if category in self.categories:
				self.select_events_from_category_list(el.getparent().getnext(), category)				
			self.select_page_content(el)

	def select_events_from_category_list(self, list, category):
		"""
		Selecting a specific category of events from the list of events
		"""
		for el in list:
			event = {}
			event['category'] = category.lower()
			event['day'] = self.page.lower()
			event_text = el.text_content()
			parts = event_text.split(u" – ")
			
			if len(parts) == 1:																													
				event['title'] = parts[0].replace("\n\n", " ").replace("\n", "; ")
			else:
				event['year'] = parts[0].lower()																							
				event['title'] = parts[1].replace("\n\n", " ").replace("\n", "; ")
			self.event_list.append(event)		

	def get_event_list(self):
		"""
		Returns the list of events from a page
		"""
		if self.event_list == []:
			try:
				response = urllib.urlopen(self.url)
			except HTTPError as e:
				print ('Http error. Error code: ', e.code)
			except URLError as e:
				print( 'Url Error. Reason: ', e.reason)
			else:
				self.page_content = html.fromstring(urllib.urlopen(self.url).read())
				self.select_page_content(self.page_content)
		
		return self.event_list
