__author__ = 'I302581'
from bs4 import BeautifulSoup


class AnalyseTitleSuper(object):
	def analyse(self, source):
		raise UnboundLocalError('Exception, no strategy implemented for analyse title.')

class AnalyseTitleWiki(AnalyseTitleSuper):
	def analyse(self, source):
		title = ''
		soup = BeautifulSoup(source)
		result = soup.find_all("span", id='title-text')
		if result:
			title += result[0].get_text(strip=True)
		result = soup.find_all("div", id='breadcrumb-section')
		if result:
			title += '-' + result[0].get_text(strip=True)
		return title

class AnalyseTitleJam(AnalyseTitleSuper):
	def analyse(self, source):
		title = ''
		soup = BeautifulSoup(source)
		title = soup.find("title")
		if title:
			title = title.get_text(strip=True)
		else:
			title = "default title jam"

		return title

# AnalyseTitle Factory
class AnalyseTitleFactory(object):
	_analysestrategies = {}
	_analysestrategies['undefine'] = AnalyseTitleSuper()
	_analysestrategies['wiki'] = AnalyseTitleWiki()
	_analysestrategies['jam'] = AnalyseTitleJam()

	def createAnalyseTitle(self, strategy=None):
		if strategy in self._analysestrategies:
			analyse = self._analysestrategies[strategy]
		else:
			analyse = self._analysestrategies['undefine']
		return analyse