from models import Contents
from django.db.models import Q
from HTMLParser import HTMLParser
import os
import re
from WebPageTools import partPage
from WebPageTools import get_title
from WebPageTools import getSubTotalURLS
from WebPageTools import getWikiLeftNaviLinks
from fetchData import getFetcher
from resAddr import ResAddr
# For Parsers
from parseDataBase import ParserSuper
from parseDataBase import ParseInputDS
from const_file_type import GLOBAL_FILE_TYPE
from parseHtml import ParseHtml
from parseHtmlJam import ParseHtmlJam
from parseHtmlWiki import ParseHtmlWiki
from parserPdf import ParserPDF
from parseSF import ParserSF
from parseDOCX import ParserDOCX
from parseDOC import ParseDOC
from parsePPT import ParsePPT

class ReadBigFile:
	def __init__(self, fileName, blockSize = 512):
		self.fileName = fileName
		import codecs
		self.f = codecs.open(self.fileName, 'r', 'utf-8')
		# self.f = open(self.fileName, 'r')
		self.blockSize = blockSize

	def getNextBlock(self):
		block = self.f.read(self.blockSize)
		if not block:
			self.f.close()
			return None
		return block

class Crawler_client:
	url = ''
	uid = ''
	upwd = ''

	# For Parsers
	parsers = None

	# Initial the crawler with url, user ID, user passwd
	def __init__(self, uid = '', upwd = ''):
		self.uid = uid
		self.upwd = upwd

		# For Parsers
		if Crawler_client.parsers == None:
			Crawler_client.parsers = {}
			Crawler_client.parsers[GLOBAL_FILE_TYPE.HTML] = ParseHtml()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.JAM] = ParseHtmlJam()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.WIKI] = ParseHtmlWiki()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.SF] = ParserSF()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.PDF] = ParserPDF()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.DOCX] = ParserDOCX()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.DOC]  = ParseDOC()
			Crawler_client.parsers[GLOBAL_FILE_TYPE.PPT]  = ParsePPT()

	def start_fetch(self, url, level = 1):
		self.url = url
		result = getFetcher(self.url, self.uid, self.upwd).fetchData()
		subURLs = getSubTotalURLS(result, url)
		if (len(result) != 0):
			title = get_title(result)
			if (len(title) == 0): title = 'Default' + self.url
			# result = self.convert_html_to_content(result)
			result = partPage(result, 0)
			self.write_to_database(1, 1, title, result, self.url, level)
			# self.do_syscmd_reindexer()
		return subURLs

	def getSubLink(self, rawData, baseURL, linkType):
		if linkType not in Crawler_client.parsers:
			return []
		parser = Crawler_client.parsers[linkType]
		return parser.getSublinks(rawData, baseURL)

		# subURLs = getSubTotalURLS(rawData, baseURL)
		# return subURLs

	# def getWikiLeftNaviLink(self, rawData, baseURL, uid, pwd):
	#     subURLs = getWikiLeftNaviLinks(rawData, baseURL, uid, pwd)
	#     return subURLs


	def parseContent(self, rawData, url, level):
		print 'parseContent rawData', len(rawData)
		id = 0
		if (len(rawData) != 0):
			title = get_title(rawData)
			if (len(title) == 0): title = 'Default' + url
			# result = partPage(rawData, 0)
			result = partPage(rawData, url)
			id = self.write_to_database(1, 1, title, result, url, level)
		return id

	# def getResourceType(self, resourceAddr):
	# 	regWIKI = re.compile(r'https://wiki.wdf.sap.corp')
	# 	regJAM = re.compile(r'https://jam4.sapjam.com')
	# 	regPDF = re.compile(r'.pdf')
	# 	regTEXT = re.compile(r'.txt')
	# 	if regWIKI.search(resourceAddr):
	# 		return ParseInputType.WIKI
	# 	elif regJAM.search(resourceAddr):
	# 		return ParseInputType.JAM
	# 	elif regPDF.search(resourceAddr):
	# 		return ParseInputType.PDF
	# 	elif regTEXT.search(resourceAddr):
	# 		return ParseInputType.TXT
	# 	else:
	# 		return ParseInputType.SF

	# def _getParserByAddr(self, resourceAddr):
	# 	# To-do. Replace this with util function to detect type
	# 	# type = ParseInputType.WIKI
	# 	type = self.getResourceType(resourceAddr)
	#
	# 	parser = ParserSuper()
	# 	if type in Crawler_client.parsers:
	# 		parser = Crawler_client.parsers[type]
	# 	else:
	# 		parser = None
	# 	return type,parser


	# def parseContentEnhance(self, rawData, resourceAddr, level):
	from exeTime import exeTime
	@exeTime
	def parseContentEnhance(self, rawData, resourceAddr, fileType, level):
		# type,parser = self._getParserByAddr(resourceAddr)
		# dictInput = {ParseInputDS.RAWDATA:rawData, ParseInputDS.RESOURCEADDR:resourceAddr, ParseInputDS.TYPE:type}
		if fileType in Crawler_client.parsers:
			parser = Crawler_client.parsers[fileType]
			dictInput = {ParseInputDS.RAWDATA:rawData, ParseInputDS.RESOURCEADDR:resourceAddr, ParseInputDS.TYPE:fileType}
		else:
			return self.write_to_database(m_group_id=1, m_group_id2=1, m_title="error url", m_content='', m_url=resourceAddr, m_level=level)
		try:
			_title, _result = parser.parseContent(dictInput)
			 # = parser.getTitle(_result, resourceAddr)
		except Exception as e:
			print e
			raise e
		if fileType == GLOBAL_FILE_TYPE.PDF:
			return self.write_file_to_database(m_group_id=1, m_group_id2=1, m_title=_title, m_path=_result, m_url=resourceAddr, m_level=level)
		return self.write_to_database(m_group_id=1, m_group_id2=1, m_title=_title, m_content=_result, m_url=resourceAddr, m_level=level)

	# Write data into database(mysql now)
	def write_to_database(self,m_group_id, m_group_id2, m_title, m_content, m_url, m_level):
		print 'write_to_database'
		'''doc = Documents.objects.filter(url = m_url)
		if (len(doc) == 0):
			doc = Documents(url=m_url, uid=self.uid, title=m_title, level = m_level)
			doc.save()
			print 'create\n'
		else:
			doc[0].uid = self.uid
			doc[0].title = m_title
			# doc.update()
			doc[0].save()
			doc = doc[0]
			print 'update\n'''
		# doc = Documents(title='title', url='url')
		# doc.save()
		# print 'docid is: %s' % str(doc)
		# Delete old records
		res = ResAddr()
		id = res.saveResaddr(m_url, m_level, '', m_title)
		doc = res.getById(id)
		oldContents = Contents.objects.filter(doc = doc)
		oldContents.delete()
		import types
		if type(m_content) is types.ListType:
			for para in m_content:
				# print 'm_content' + para
				con = Contents(group_id=doc.id, group_id2=m_group_id2, doc=doc, paragraph=para, tag='p')
				con.save()
		else:
			con = Contents(group_id=doc.id, group_id2=m_group_id2, doc=doc, paragraph=m_content, tag='p')
			con.save()
		return doc.id

	#Write data into database(mysql now)
	def write_file_to_database(self,m_group_id, m_group_id2, m_title, m_path, m_url, m_level):
		print 'write_to_database'
		'''doc = Documents.objects.filter(url = m_url)
		if (len(doc) == 0):
			doc = Documents(url=m_url, uid=self.uid, title=m_title, level = m_level)
			doc.save()
			print 'create\n'
		else:
			doc[0].uid = self.uid
			doc[0].title = m_title
			# doc.update()
			doc[0].save()
			doc = doc[0]
			print 'update\n'''
		# doc = Documents(title='title', url='url')
		# doc.save()
		# print 'docid is: %s' % str(doc)
		# Delete old records
		res = ResAddr()
		id = res.saveResaddr(m_url, m_level, '', m_title)
		doc = res.getById(id)
		oldContents = Contents.objects.filter(doc = doc)
		oldContents.delete()
		try:
			print '\n\n\nstart write url:', m_url
			reader = ReadBigFile(m_path, blockSize=1024*16)
			block = reader.getNextBlock()

			while(block!=None):
				# print 'm_content' + para
				con = Contents(group_id=doc.id, group_id2=m_group_id2, doc=doc, paragraph=unicode(block), tag='p')
				con.save()
				block = reader.getNextBlock()
			os.remove(m_path)
			return  doc.id
		except Exception as e:
			print e
			print str(e)
			exit()
			return None

	def test_write_to_database(self):
		lPath = "/sapmnt/HOME/i302581/Desktop/mysite_yu_1008/temp/__CNST50066074_Root_Business_One_Projects_Dev_SDK_KnowledgeWarehouse__Ebook_Effective STL_pdf.txt"
		path = "//CNST50066074/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/java/m2ebook-pdf.pdf"
		self.write_file_to_database(m_group_id=1, m_group_id2=1, m_title='hello', m_path=lPath, m_url=path, m_level='1')