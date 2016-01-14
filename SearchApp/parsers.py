__author__ = 'I302581'
from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
import re
import os
from bs4 import element

################################# Useful Static params ###################################
# Static parameter
# Not used now, but for future
# Assign every block of text with its priority
PRIORITY_DEFAULT = 5									# default
PRIORITY_FEED_BODY = 3									#
PRIORITY_FEED_INFO = 5									#
PRIORITY_FEED_COMMENT = 4								#
PRIORITY_OVERVIEW_WIDGETITEM = 3						#
PRIORITY_OVERVIEW_WIDGETCONTAINER = 3					#

################################### Helper Functions ######################################
# Parsed object structure
# String with Priority
# Result of all parse functions
class ParsedObject(object):
	_str = ''
	_priority = PRIORITY_DEFAULT

	def __init__(self, str, priority):
		self._str = str
		self._priority = priority

	def str(self):
		return self._str

	def priority(self):
		return self._priority

# Convertion Helper Function (ParsedObject Object)
# From: String list(which has no priority)
# to:   ParsedObject list (which use the specified priority)
def convertStrListtoParobjList(stringList, priority):
	if not stringList:
		return None
	result = []
	for string in stringList:
		result.append(ParsedObject(string, priority))
	return result

# Convertion Helper Function (ParsedObject Object)
# From: ParsedObject list (which use the specified priority)
# to:   String list(which has no priority)
def convertParobjListtoStrList(parsedObjList):
	if not parsedObjList:
		return None
	result = []
	for obj in parsedObjList:
		result.append(obj.str())
	return result

# Check whether a tag is belong to head class(from h1 to h9)
# Input:  tag (string)
# Output: Boolean(True or False)
def checkHead_1_9(tag):
	if not tag or len(tag) <= 0:
		return False
	try:
		result = re.findall(r'[h|H][1-9]', str(tag))
		if len(result) > 0:
			return True
		else:
			return False
	except:
		print 'except: ' + str(tag)

# Prefix document soup object, remove script!
# input: BeautifulSoup object
# output: BeautifulSoup object
def prefixSoup(soup):
	if not soup:
		return soup
	script_s = soup.find_all("script")
	for item in script_s:
		item.clear()
	return soup


################################### Parsers Super ######################################
# Parsers' super class
# Abstract class
# Can not be used directly
# Super class of parsers
class parserSuper(object):
	def parse(self, source):
		raise UnboundLocalError('Exception raised, no strategy supplied to parser.')

################################### Parsers SubClasses ##################################
# First kind of parsers, get paragraphs from html source
class parserParagraph(parserSuper):
	def parse(self, source):
		soup = BeautifulSoup(source)
		result = soup.find_all(id = "main")
		resultParas = []
		if result:
			result = result[0].find_all(re.compile("[h|H][1-9]"))
			if result:
				for temp in result:
					tagName = temp.name.encode('utf-8', 'ignore')
					tempStr = '<' + tagName + '>' + temp.get_text(strip=True).encode('utf-8', 'ignore') + '</' + tagName + '>'
					for ttt in temp.next_siblings:
						if checkHead_1_9(ttt):
							break
						elif ttt != '\n':
							tempStr += str(ttt)
					resultParas.append(tempStr)
		return resultParas

# Retuan all content in feedlist
# input: BeautifulSoup object
# output: parsedObjects
class parseJAMFeed(parserSuper):
	def parse(self, source):
		soup = BeautifulSoup(source)
		soup = prefixSoup(soup)
		result = []
		if not soup:
			return result
		feedList = soup.find_all("div", "feed_item_main")
		print 'feed count: ' + str(len(feedList))
		for feed in feedList:
			feedBody = feed.find("div", "member_action").get_text(strip=True)
			feedInfo = feed.find("div", "feedInfo").get_text(strip=True)
			feedComment = feed.find("div", "feed_response_content").get_text(strip=True)
			result.append(ParsedObject(str=feedBody, priority=PRIORITY_FEED_BODY))
			result.append(ParsedObject(str=feedInfo, priority=PRIORITY_FEED_INFO))
			result.append(ParsedObject(str=feedComment, priority=PRIORITY_FEED_COMMENT))
		return result

# Return all contentin Overview page   ===    widget parser
# input: BeautifulSoup object
# output: parsedObjects
class parseJAMOverview(parserSuper):
	def parse(self, source):
		soup = BeautifulSoup(source)
		soup = prefixSoup(soup)
		result = []
		if not soup:
			return result
		widgetList = soup.find_all("div", "widget-content")

		for widget in widgetList:
			# check widge-item
			widgetItemList = widget.find_all("div", "widget-item")
			for item in widgetItemList:
				result.append(ParsedObject(item.get_text(strip=True), PRIORITY_OVERVIEW_WIDGETITEM))
			# check widget-container
			widgetContainerList = widget.find_all("div", "list-item") # Attention: these list items are in widget-container
			for item in widgetContainerList:
				result.append(ParsedObject(item.get_text(strip=True), PRIORITY_OVERVIEW_WIDGETCONTAINER))
			# check widget-feed
			result += parseJAMFeed(widget)
		return result


# Parser factory
class parserFactory(object):
	parsers = {}
	parsers["paragraph"] = parserParagraph()
	parsers['JAM_FEED'] = parseJAMFeed()
	parsers['JAM_OVERRIEW'] = parseJAMOverview();
	parsers["undefined"] = parserSuper()

	def createParser(self, strategy=None):
		if strategy in self.parsers:
			return self.parsers[strategy]
		else:
			return self.parsers["undefined"]

