__author__ = 'root'
from parseDataBase import ParserSuper
from bs4 import BeautifulSoup
import re
from parseDataBase import ParseInputDS
from WebPageTools import getSubTotalURLS


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

class ParseHtml(ParserSuper):

	def parseContent(self, dicInput):
		source = dicInput[ParseInputDS.RAWDATA]
		soup = BeautifulSoup(source)
		soup = prefixSoup(soup)
		result = soup.get_text(strip=True)
		return result

	def getSublinks(self, rawdata, baseurl):
		return getSubTotalURLS(rawdata, baseurl)
