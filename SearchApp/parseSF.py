__author__ = 'root'
from parseDataBase import ParserSuper
from parseDataBase import ParseInputDS
from logger import printLog
import time
import datetime
from seUtility import SeUtility

class ParserSF(ParserSuper):
	def parseContent(self, dicInput):
		source = dicInput[ParseInputDS.RAWDATA]
		source = eval(source)
		url = dicInput[ParseInputDS.RESOURCEADDR]
		result = ''
		for key,value in enumerate(source):
			result += ' ' + value
		return self._getTitle(url), result

	def _getTitle(self, url):
		return SeUtility.getTitleofShareFolderPath(url)
		# if "SampleCode" in url:
		# 	print url
		# 	printLog( self, ' ' ,datetime.datetime.now().strftime("%I:%M%p on %B %d %Y") , 'SampleCode:' + url)
		# title = url.split('/')
		# if len(title[len(title)-1]) <=0:
		# 	title = title[len(title)-2]
		# else:
		# 	title = title[len(title)-1]
		# return title

	def getSublinks(self, rawdata, baseurl):
		result = []
		rawdata = eval(rawdata)
		if not (baseurl.endswith('/')):
			baseurl += '/'
		for key,value in enumerate(rawdata):
			if len(value) > 0:
				result.append(baseurl + value)
		return result