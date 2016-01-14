__author__ = 'root'
from parseHtml import *
from bs4 import BeautifulSoup
from parseDataBase import ParseInputDS
import re
from analysetitle import AnalyseTitleFactory

class ParseHtmlWiki(ParseHtml):
	def parseContent(self, dicInput):
		source = dicInput[ParseInputDS.RAWDATA]
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
		self._title = self._getTitle(source)
		print 'after parse, title: %s' % self._title
		return self._title, resultParas

	def _getTitle(self, source):
		analyse = AnalyseTitleFactory().createAnalyseTitle('wiki')
		title = analyse.analyse(source)
		return title


#for testing purpose
def main(argv):
	f = open('test_parseHtmlWiki.html', 'r')
	source = f.read()
	client = ParseHtmlWiki()
	mDict = dict()
	mDict[ParseInputDS.RAWDATA] = source
	client.parseContent(mDict)
	print 'pase after, title:%s' % client._title
	print 'result %s' %client.getTitle()

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))