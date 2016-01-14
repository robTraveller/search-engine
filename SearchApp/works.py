import time
import datetime
from multiprocessing.managers import BaseManager
import time
import datetime
from multiprocessing import Process
from crawler import *
from resourceLink import ResourceLinkList
from resAddr import ResAddr

from WebPageTools import do_syscmd_reindexer
from WebPageTools import validate
from logger import printLog
import traceback

class MyManager(BaseManager):
	pass

class startProcess():
	_instance = None

	CRAWLER_PROCESS_COUNT = 20
	PARSER_PROCESS_COUNT = 15

	ContentSize = range(CRAWLER_PROCESS_COUNT)
	contents = range(CRAWLER_PROCESS_COUNT)

	ParserSize = range(PARSER_PROCESS_COUNT)
	parsers = range(PARSER_PROCESS_COUNT)

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			#Single -> startProcess
			cls._instance = super(startProcess, cls).__new__( 
								cls, *args, **kwargs)
		return cls._instance
	
	def __init__(self):
		printLog('initialize startProcess')
		MyManager.register('linkList', ResourceLinkList)
		self.manager = MyManager()
		self.manager.start()
		self.linkList = self.manager.linkList()
	
	
	def start(self):
		# self.startIndexKeeper()
		self.startContentIndexKeeper()
	
	_indexer = None
	def startIndexKeeper(self):
		try:
			if self._indexer == None or self._indexer.is_alive():
				self._indexer = IndexKeeper(self.linkList)
				self._indexer.name = '_indexer'
				self._indexer.start()
			self.startSubLinkCrawler()
		except Exception, e:
			printLog('\nsomething error! %s' % e)
	
	_sublinkCrawler = None
	def startSubLinkCrawler(self):
		try:
			if self._sublinkCrawler == None or not self._sublinkCrawler.is_alive():
				self._sublinkCrawler = SubLinkCrawler(self.linkList)
				self._sublinkCrawler.name = '_sublinkCrawler'
				self._sublinkCrawler.start()
		except Exception, e:
			printLog('\nsomething error! %s' % e)
		
	def setUserInfo(self, uid, upwd):
		self.linkList.setUid(uid)
		self.linkList.setUpwd(upwd)
		# self._loadWikiLeftNavi(uid, upwd)
		self.startContentCrawler()

	def _loadWikiLeftNavi(self, uid, upwd):
		fetcher = getFetcher('https://wiki.wdf.sap.corp', uid, upwd)
		rawResult = fetcher.fetchNaviData()
		tempResult = getWikiLeftNaviLinks(rawResult['data'], rawResult['url'])
		finalResult = [] + tempResult['links']
		while len(tempResult['nextLevelLinks']) > 0:
			tTempResult = {}
			tTempResult['links'] = []
			tTempResult['nextLevelLinks'] = []
			for tempLinkPageId in tempResult['nextLevelLinks']:
				tRawResult = fetcher.fetchNaviData(pageId=str(tempLinkPageId))
				ttResult = getWikiLeftNaviLinks(tRawResult['data'], tRawResult['url'])
				# tTempResult = dict(tTempResult, **ttResult)
				tTempResult['links'] += ttResult['links']
				tTempResult['nextLevelLinks'] += ttResult['nextLevelLinks']
			tempResult = tTempResult
			finalResult += tempResult['links']
		for url in finalResult:
			res = ResAddr()
			id = res.saveResaddr(url, 1)

		print 'load wiki navi finished.'
		return True
	
	def startContentCrawler(self):
		try:
			for i in self.ContentSize:
				if self.contents[i] == None \
					or not isinstance(self.contents[i], ContentCrawler) \
					or not self.contents[i].is_alive():
					self.contents[i] = ContentCrawler(self.linkList)
					self.contents[i].name = 'content' + str(i)
					self.contents[i].start()
					printLog('contentCrawler1 start')
			
			'''if self.content2 == None or not self.content2.is_alive():
				self.content2 = ContentCrawler(self.linkList)
				self.content2.name = 'content2'
				self.content2.start()
				printLog('contentCrawler2 start')'''
			
			#self.content1.join()
		except Exception, e:
			printLog('\nsomething error! msg:%s' % e)

	def startContentIndexKeeper(self):
		try:
			for i in self.ParserSize:
				if self.parsers[i] == None \
					or not isinstance(self.parsers[i], IndexKeeper) \
					or not self.parsers[i].is_alive():
					self.parsers[i] = IndexKeeper(self.linkList)
					self.parsers[i].name = 'indexer' + str(i)
					self.parsers[i].start()
			self.startSubLinkCrawler()
			# if self._indexer == None or self._indexer.is_alive():
			# 	self._indexer = IndexKeeper(self.linkList)
			# 	self._indexer.name = '_indexer'
			# 	self._indexer.start()
			# self.startSubLinkCrawler()
		except Exception, e:
			printLog('\nsomething error! %s' % e)
	

class IndexKeeper(Process):
	def __init__(self, linkList):
		self._linkList = linkList
		super(IndexKeeper, self).__init__()
	
	def run(self):
		printLog(self, ' ', '  start indexKeeper...')
		linkList = self._linkList
		try:
			count = 0
			sum = 0
			startTime = time.time()
			sleeptime = 5
			indexLowerLimit = 10
			depth = 2
			while(True):
				# link = linkList.getNextLink()
				link = linkList.getNextToParseLink()
				try:
					printLog(self, ' self._linkList size:' , self._linkList.size())
					if link != None:
						printLog(self, ' ', 'parseContent')
						
						linkKeeper = SubLinkKeeper(linkList, depth)
						links = ResourceLinkList()
						links.appendLink(link)
						linkKeeper.searchLink(links)
						
						
						# id = Crawler_client().parseContent(link.getRawData(), link.getAddr(), link.getLevel())
						id = Crawler_client().parseContentEnhance(rawData=link.getRawData(), resourceAddr=link.getAddr(), fileType=link.getType(), level=link.getLevel())
						# Crawler_client().test_write_to_database()
						ResAddr().updateReponseCode(id, link.getResponseCode(), link.getAddr())

						
						self._linkList.setLinkVisited(link.getKey())
						count += 1
						sum += 1
						printLog(self.name, ' analysis link sum:' , sum)
						if(count/indexLowerLimit != 0 or (time.time() - startTime) > sleeptime):
							do_syscmd_reindexer()
							count = 0
							startTime = time.time()
					else:
						printLog(self, ' ' ,datetime.datetime.now().strftime("%I:%M%p on %B %d %Y") , 'indexKeeper sleep')
						printLog(self, 'sleep:', sleeptime, 's')
						time.sleep(sleeptime)
						printLog(self, ' ' ,datetime.datetime.now().strftime("%I:%M%p on %B %d %Y") , 'indexKeeper weakup')
				except Exception, e:
					id = ResAddr(link.getAddr()).save()
					try:
						code = e.code
					except Exception as ignoredError:
						code = 1000
					ResAddr().updateReponseCode(id, code, link.getAddr())
					ResAddr().saveErrorMsg(link.getAddr(), e.message)
					self._linkList.setLinkVisited(link.getKey())					
					self._linkList.removeLink(link.getKey())
					printLog('indexKeeper something error_1!', e)
			else:
				printLog(self, 'the IndexKeeper loop is over.')
		except Exception, e:
			printLog('indexKeeper something error_2!', e)
		printLog(self, 'end indexKeeper...')
		do_syscmd_reindexer()

class ContentCrawler(Process):
	def __init__(self, linkList):
		self._linkList = linkList
		super(ContentCrawler, self).__init__()

	def run(self):
		printLog(self, ' ' ,'start ContentCrawler...')
		linkList = self._linkList
		try:
			#startTime = time.time()
			sleeptime = 5
			indexLowerLimit = 10
			sum = 0
			while(True):
				try:
					link = linkList.getNextEmptyLink()
					printLog(self, ' ', 'linkList size:', linkList.size())
					if link != None:
						try:
							if link.getAddr() == None or len(link.getAddr()) == 0:
								e = Exception()
								e.code = 2000
								e.message = 'Empty url here'
								raise e
							fetcher = getFetcher(link.getAddr(), linkList.getUid(), linkList.getUpwd())
							rawData, resourceAddr, fileType = fetcher.fetchData()
							linkList.setLinkRawData(link.getKey(), rawData)
							linkList.setLinkType(link.getKey(), fileType)
							# linkList.setLinkResponseCode(link.getKey(), fetcher.getResponseCode())
							# linkList.setLinkRawData(link.getKey(), fetcher.fetchData())
							# linkList.setLinkResponseCode(link.getKey(), fetcher.getResponseCode())
							# linkList.setLinkType(link.getKey(), fetcher.getType())
						except Exception, e:
							raise e
						sum+=1
						#printLog(self.name, ' fetch link sum:' , sum)
						#if((time.time() - startTime) > sleeptime):
						#	startTime = time.time()
					else:
						#break
						printLog( self, ' ' ,datetime.datetime.now().strftime("%I:%M%p on %B %d %Y") , 'ContentCrawler sleep')
						printLog( self, 'sleep:', sleeptime, 's')
						time.sleep(sleeptime)
						printLog( self, ' ' ,datetime.datetime.now().strftime("%I:%M%p on %B %d %Y") , 'ContentCrawler weakup')
				except Exception, e:
					printLog('ContentCrawler while loop something error!', e, link.getAddr())
					id = ResAddr(link.getAddr()).save()
					try:
						code = e.code
					except Exception as ignoredError:
						code = 1000
					ResAddr().updateReponseCode(id, code, link.getAddr())
					print 'saveErrorMsg', str(e)
					ResAddr().saveErrorMsg(link.getAddr(), str(e))
					self._linkList.setLinkVisited(link.getKey())					
					self._linkList.removeLink(link.getKey())
			else:
				printLog(self, 'the ContentCrawler loop is over.')
		except Exception, e:
			printLog('ContentCrawler something error!', e)
		printLog( 'end ContentCrawler...')

END_SEARCH_LEVEL = 100;
class SubLinkKeeper():
	def __init__(self, linkList, depth = 1):
		self._linkList = linkList
		self._depth = 100
		# self._depth = END_SEARCH_LEVEL
		
	def searchLink(self, currentLevelLinkList):
		#printLog('start search sublink...')
		linkList = self._linkList
		depth = self._depth
		try:
			STOP_LEVEL = depth # Search to which level
			if currentLevelLinkList == None:
				return
				#currentLevelLinkList = ResourceLinkList()
			nextLevelLinkList = ResourceLinkList()

			nextLevelLinkList = self.getSubLinkList(currentLevelLinkList)
			
			for link in currentLevelLinkList:
				linkList.appendLink(link)
			for link in nextLevelLinkList:
				linkList.appendLink(link)
				
		except Exception, e:
			printLog( '\nsomething error when search linkage!%s' % str(e))
		finally:
			#printLog('linklist size', linkList.size())
			#printLog( 'exit sublinkkeeper')
			pass

	# Search action code here
	def getSubLinkList(self, currentLevelLinkList):
		nextLevelLinkList = ResourceLinkList()
		resultList = ResourceLinkList()
		for link in currentLevelLinkList:
			path = link.getAddr()
			level = link.getLevel()
			if level > self._depth:
				break;
			if len(path)>0 and validate(path):
				resultURLs = []
				try:
					rawData = link.getRawData()
					if rawData != '':
						resultURLs = Crawler_client().getSubLink(link.getRawData(), path, link.getType())
						if link.getAddr() == "https://wiki.wdf.sap.corp/wiki/plugins/pagetree/naturalchildren.action?hasRoot=true&pageId=17728069":
							resultURLs.extend(Crawler_client().getWikiLeftNaviLink(link.getRawData(), path, self._linkList.getUid(), self._linkList.getUpwd()))
					else:
						continue
				except Exception, e:
					printLog( 'failed. path:%s, level:%s, Exception:%s' % (path, level, e))
				for url in resultURLs:
					if url in nextLevelLinkList:
						pass
					else:
						nextLevelLinkList.append(url.encode('utf-8'), level + 1)
						res = ResAddr()
						# id = res.saveResaddr(url, level + 1)
						id = res.saveNewResaddr(url, level + 1)

		for link in nextLevelLinkList:
			if link in currentLevelLinkList.getLinks() or ResAddr().isURLExist(link.getAddr()):
				continue
			else:
				resultList.appendLink(link)
		return resultList

class SubLinkCrawler(Process):
	def __init__(self, linkList):
		self._linkList = linkList
		super(SubLinkCrawler, self).__init__()
	
	def run(self):
		try:
			#startDelta = 5 #hours
			endDelta = 1 #hours
			sleeptime = 60*60*endDelta
			currentLevelLinkList = ResourceLinkList()
			level = 0
			while(True):
				try:
					recs = ResAddr().getObjsByLevel(level)
					#level link
					if recs.count() > 0 and level < END_SEARCH_LEVEL:
						recs = ResAddr().getObjsNeedRefreshLevel(level, endDelta) # getObjsNeedRefreshLevel(level, endDelta)  # getObjsByLevel(level)
						printLog(self, 'recs.count', recs.count())
						# print 'hello hello hello hello ################################## linked size() : ' + str(recs.count())
						#need refresh level link
						if recs.count() > 0:
							linkKeeper = SubLinkKeeper(self._linkList)
							currentLevelLinkList.appendAddrList([d.url for d in recs], level)
							linkKeeper.searchLink(currentLevelLinkList)
						level+=1
					else:
						level = 0
						#break
						printLog( self, ' ', 'SubLinkCrawler sleep')
						printLog( self, 'sleep:', sleeptime, 's')
						time.sleep(sleeptime)
					printLog( self, ' ' , 'SubLinkCrawler weakup')
				except Exception, e:
					printLog( '\nsomething error when SubLinkCrawler! %s' % str(e))
			else:
				printLog(self, 'the SubLinkCrawler loop is over.')
		except Exception, e:
			printLog( '\nsomething error when SubLinkCrawler! %s' % str(e))
			#import traceback, os.path
			#top = traceback.extract_stack()[-1]
			#printLog( ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))

processer = startProcess()