from multiprocessing import Lock
import base64
from logger import printLog

class ResourceLink(object):
	
	#the resource address string
	_addr = ''
	
	#flag does the link visited or not, false-not visited, true visited
	_visited = False
	
	#which the level of the path
	_level = None
	
	#the content with addr. suck as wiki page
	_rawData = ''
	
	_isAnalysis = False

	_isParsedSign = False # declare is parsed or not
	
	_reponseCode = 0
	
	#resource data type
	_type = ''
	
	#local resource file path
	_localPath = ''
	
	def __init__(self, addr='', level = 0):
		self._addr = addr
		self._level = level
	
	def __str__(self):
		return 'visited' + str(self._visited) + ' ' + self._addr
		
	def _isVisited(self):
		return self._visited
	
	def _setVisited(self, visit = True):
		#print 'setLinkVisited:', visit, self._addr
		self._visited = visit
	
	def getAddr(self):
		return self._addr
	
	def setAddr(self, addr):
		self._addr = addr
	
	#get base64 encode string
	def getKey(self):
		return base64.b64encode(self._addr)
	
	def getRawData(self):
		return self._rawData
	
	def setRawData(self, rawData):
		#print 'setRawData'
		self._rawData = rawData
	
	def hasData(self):
		if self._rawData == None or len(self._rawData) == 0:
			return False
		return True
	
	def setLevel(self, level):
		self._level = level
	
	def getLevel(self):
		if self._level != None:
			return self._level
		return -10

	def isAnalysis(self):
		return self._isAnalysis
	
	def _setAnalysis(self, isAnalysis = True):
		self._isAnalysis = isAnalysis

	def isParsed(self):
		return self._isParsedSign

	def _setIsParsed(self, isParsedSign = True):
		self._isParsedSign = isParsedSign

	def getResponseCode(self):
		return self._reponseCode
		
	def setResponseCode(self, code):
		self._reponseCode = code
	
	def getType(self):
		return self._type
	
	def setType(self, type):
		self._type = type
	
	def getLocalPath(self):
		return self._localPath
	
	def setLocalPath(self, path):
		self._localPath = path
	
#kinds of resources list
class ResourceLinkList:
	
	_uid = ''
	_upwd = ''
	_mutex = Lock()
	
	#dictionary, key is the link's addr.
	_links = {}
	
	def __init__(self, uid = '',  upwd = ''):
		self._uid = uid
		self._upwd = upwd
		self._links = {}

	def __str__(self):
		for link in self._links:
			print link
		return self._links
		
	def setUid(self, uid):
		self._uid = uid
	
	def setUpwd(self, pwd):
		self._upwd = pwd
	
	def getUid(self):
		return self._uid
	
	def getUpwd(self):
		return self._upwd
	
	'''def __contains__(self, key):
		for value in self._links:
			print value.getAddr()'''
	#__getItem__ for  list[]
	
	def __iter__(self):
		return iter(self._links.values())
	
	def getLinks(self):
		return self._links
	
	def append(self, addr, level):
		self.appendAddr(addr, level)
	
	def appendAddrList(self, addrList, level):
		for addr in addrList:
			self.appendAddr(addr.encode('utf-8'), level)
	
	#directly save addr to list
	def appendAddr(self, addr, level = 0):
		link = ResourceLink(addr, level)
		self.appendLink(link)
	
	#save a link to list
	def appendLink(self, link):
		if self._verifyLink(link):
			key = link.getKey()
			self._links[key] = link
	
	#get non visited link
	def _visitLink(self, key):
		#print 'self._links[key] != None', self._links[key] != None 
		#print 'not self._links[key]._isVisited()', not self._links[key]._isVisited()
		if self._links[key] != None  \
		and not self._links[key]._isVisited():
			return self._links[key]
		else:
			self.removeLink(key)
		return None
	
	#visit next address which contain data
	def getNextLink(self):
		#print 'getNextLink'
		#self._mutex.acquire()
		#self._mutex.release()
		with self._mutex:
			#print 'in mutex zone'
			for key in self._links.keys():
				#print key
				link = self._visitLink(key)
				#skip the empty link
				if link == None or not link.hasData():
					continue
				if link != None:
					print 'next link:' , link
					return link
			return None

	# get next link which need to parsed
	def getNextToParseLink(self):
		#print 'getNextLink'
		#self._mutex.acquire()
		#self._mutex.release()
		with self._mutex:
			#print 'in mutex zone'
			for key in self._links.keys():
				#print key
				link = self._visitLink(key)
				#skip the empty link
				if link == None or not link.hasData() or link.isParsed():
					continue
				if link != None:
					print 'next link:' , link
					self._links[key]._setIsParsed()
					return link
			return None
	
	def getNextEmptyLink(self):
		#print 'getNextLink'
		with self._mutex:
			#print 'in mutex zone'
			for key in self._links.keys():
				#print key
				link = self._visitLink(key)
				if link == None or link.hasData() or link.isAnalysis():
					continue
				if link != None:
					#print 'next empty link:' , link
					self._links[key]._setAnalysis()
					return link
			return None
	
	def setLinkAnalysised(self, key, isAnalysis = True):
		with self._mutex:
			self._links[key]._setAnalysis(isAnalysis)
	
	def setLinkVisited(self, key):
		print 'setLinkVisited'
		with self._mutex:
			self._links[key]._setVisited()
	
	def setLinkRawData(self, key, rawData):
		with self._mutex:
			self._links[key].setRawData(rawData)
	
	def setLinkResponseCode(self, key, code):
		with self._mutex:
			self._links[key].setResponseCode(code)
	
	def setLinkType(self, key, type):
		with self._mutex:
			self._links[key].setType(type)
			
	#check link validity
	def _verifyLink(self, link):
		if not isinstance(link, ResourceLink):
			return False
		key = link.getKey()
		if ((self._links.has_key(key) and self._links[key] != link.getAddr()) ):
			return False
		return True	
	
	#remove link
	def removeLink(self, key):
		if self._links.has_key(key):
			oldLink = self._links[key]
			del self._links[key]
			return oldLink
	
	#get link list size
	def size(self):
		return len(self._links)

		
'''list = ResourceLinkList()
list.appendAddr('1')
list.appendAddr('2')
print list.size()
print list.getNextLink()
#for path in list:
	#pass #print path
for link in list.getLinks():
	print link.getAddr()'''

	
