from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import re
import urlparse
import os
from parsers import parserFactory
from analysetitle import AnalyseTitleFactory
from parsers import convertParobjListtoStrList

# Parse Html Resource
# Parse JAM,WIKI,FOLDER content
# Have different strategy inside
def partPage( source, url):
	if re.search(r'https://wiki.wdf.sap.corp', str(url)):
		# WIKI Strategy
		concreteParser = parserFactory().createParser("paragraph")
		return concreteParser.parse(source)
	elif re.search(r'https://jam4.sapjam.com', str(url)):
		# JAM Strategy
		result = []
		feedParser = parserFactory().createParser("JAM_FEED")
		overviewParser = parserFactory().createParser("JAM_OVERRIEW")
		result.extend(feedParser.parse(source))
		result.extend(feedParser.parse(source))
		result = convertParobjListtoStrList(result)
		return result
	else:
		print "############################## Undefined parse strategy, please double check it."
		return None


def get_title(source):
	analyse = AnalyseTitleFactory().createAnalyseTitle('wiki')
	title = analyse.analyse(source)
	return title
	# result = re.findall(r"<title>(.*)</title>", html)
	# if (len(result) > 0) :
	# 	return result[0]
	# else :
	# 	return ''

# Check url validation
# url: input parameter
# output: true or false
def validate(url):
	# check http://
	if re.match(r'https?:/{2}\w.+$', url):
		return True
	elif url.startswith('//'):
		return True
		# if not '.' in url:
		# 	return True
		# elif url.
	else:
		return False

# Get sub URL list
# source: input html page
# output: all suburls
def getSubShortURLs(source):
	#print 'getSubShortURLs'
	urlList = []
	soup = BeautifulSoup(source)
	result = soup.find_all(id="main")
	if result:
		result = result[0].find_all(href = re.compile("^[^#].*"))
		if result:
			for item in result:
				urlList.append(item['href'].strip())
	#print 'getSubShortURLs end'
	return urlList

# Get sub URL list
# source: input html page
# base: input base url
# output: all suburls
def getSubTotalURLS(source, base):
	#print 'getSubTotalURLS'
	URLlist = []
	baseURL = getBaseURL(base)
	result = getSubShortURLs(source)
	for temp in result:
		URLlist.append(getTotalURL(temp, baseURL, base))
	#print 'getSubTotalURLS end'
	return URLlist

# Get base URL
# url: input url
# output: base url
def getBaseURL(url):
	#print 'getBaseURL'
	urlFields = list(urlparse.urlsplit(url))
	result = ''
	if (len(urlFields[0].strip()) != 0 and len(urlFields[1].strip()) != 0):
		result = ''
		# print urlFields
		for i in range(2, len(urlFields)):
			urlFields[i] = ''
		# print urlFields
		result = urlparse.urlunsplit(urlFields)
	#print 'getBaseURL end'
	return result


# Combine url with base url
def getTotalURL(url, base, baseFull):
	if not isinstance(url, unicode):
		url = url.decode()
	if not isinstance(base, unicode):
		base = base.decode()
	if validate(url):
		return url
	else:
		encodeURL = url.encode('ascii', 'ignore')
		if encodeURL.startswith('?') and '?' not in baseFull:
			return baseFull + url
		elif not encodeURL.startswith('/'):
			url = u'/' + url
		return base + url

# Wiki page, left navigation links.
def getWikiLeftNaviLinks(source, url):

	URLlist = []
	baseURL = getBaseURL(url)
	# result = getSubShortURLs(source)
	# urlList = []
	soup = BeautifulSoup(source)
	leftNavi = soup.find("ul", "plugin_pagetree_children_list")
	if not leftNavi:
		print 'Left navigation not found!'
		return None
	# naviLinks = []
	linksPart1 = leftNavi.find_all(href=re.compile("^[^#].*"))
	if linksPart1:
		for item in linksPart1:
			# naviLinks.append(item['href'].strip())
			URLlist.append(getTotalURL(item['href'].strip(), baseURL, url))

	# specialLinkIdList = leftNavi.find_all(id=re.compile("plusminus([0-9]*)-"))
	specialLinkIdList = re.findall(r'plusminus([0-9]*)-', unicode(leftNavi))
	result = {}
	if specialLinkIdList:
		result['nextLevelLinks'] = specialLinkIdList
	else:
		result['nextLevelLinks'] = []
	result['links'] = URLlist
	return result

# Decompress http response text
def decompress(content):
	import StringIO
	import gzip
	compressedstream = StringIO.StringIO(content)
	gzipper = gzip.GzipFile(fileobj=compressedstream)
	content = gzipper.read()
	return content

# Indexer
def do_syscmd_reindexer():
	os.system('indexer test1 --rotate')
