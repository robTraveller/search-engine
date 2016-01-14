__author__ = 'root'
from parseHtml import *
from analysetitle import AnalyseTitleFactory

class ParseHtmlJam(ParseHtml):
	def parseContent(self, dicInput):
		source = dicInput[ParseInputDS.RAWDATA]
		soup = BeautifulSoup(source)
		result = []
		result += self._parseFeed(soup)
		result += self._parseOverview(soup)
		self._title = self._getTitle(source)
		return self._title, result

	def _parseFeed(self, soup):
		result = []
		if not soup:
			return result
		feedList = soup.find_all("div", "feed_item_main")
		print 'feed count: ' + str(len(feedList))
		for feed in feedList:
			feedBody = feed.find("div", "member_action").get_text(strip=True)
			feedInfo = feed.find("div", "feedInfo").get_text(strip=True)
			feedComment = feed.find("div", "feed_response_content").get_text(strip=True)
			result.append(feedBody)
			result.append(feedInfo)
			result.append(feedComment)
			# result.append(ParsedObject(str=feedBody, priority=PRIORITY_FEED_BODY))
			# result.append(ParsedObject(str=feedInfo, priority=PRIORITY_FEED_INFO))
			# result.append(ParsedObject(str=feedComment, priority=PRIORITY_FEED_COMMENT))
		return result

	def _parseOverview(self, soup):
		result = []
		if not soup:
			return result
		widgetItemList = soup.find_all("div", "widget-item")
		for item in widgetItemList:
			# result.append(ParsedObject(item.get_text(strip=True), PRIORITY_OVERVIEW_WIDGETITEM))
			result.append(item.get_text(strip=True))
		# check widget-container
		widgetContainerList = soup.find_all("div", "list-item") # Attention: these list items are in widget-container
		for item in widgetContainerList:
			result.append(item.get_text(strip=True))
			# result.append(ParsedObject(item.get_text(strip=True), PRIORITY_OVERVIEW_WIDGETCONTAINER))
		# # check widget-feed
		# result += self._parseFeed(soup)

		# widgetList = soup.find_all("div", "widget-content")
		#
		# for widget in widgetList:
		# 	# check widge-item
		# 	widgetItemList = widget.find_all("div", "widget-item")
		# 	for item in widgetItemList:
		# 		# result.append(ParsedObject(item.get_text(strip=True), PRIORITY_OVERVIEW_WIDGETITEM))
		# 		result.append(item.get_text(strip=True))
		# 	# check widget-container
		# 	widgetContainerList = widget.find_all("div", "list-item") # Attention: these list items are in widget-container
		# 	for item in widgetContainerList:
		# 		result.append(item.get_text(strip=True))
		# 		# result.append(ParsedObject(item.get_text(strip=True), PRIORITY_OVERVIEW_WIDGETCONTAINER))
		# 	# check widget-feed
		# 	result += parseJAMFeed(widget)
		return result

	def _getTitle(self, source):
		analyse = AnalyseTitleFactory().createAnalyseTitle('jam')
		title = analyse.analyse(source)
		return title