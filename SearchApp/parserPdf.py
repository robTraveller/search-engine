#!/usr/bin/env python
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
from parseDataBase import ParserSuper
from parseDataBase import ParseInputDS
from exeTime import exeTime
from seUtility import SeUtility
class ParserPDF(ParserSuper):
	@exeTime
	def parseContent(self, dicInput):
		inFilePath = dicInput[ParseInputDS.RAWDATA]
		url = dicInput[ParseInputDS.RESOURCEADDR]
		outFilePath = inFilePath.replace('.', '_') + '.txt'
		try:
			self.exportPDF(inFilePath, outFilePath)
		except Exception as e:
			print e
			raise e
		self._title = self._getTitle(url)
		return self._title, outFilePath

	def getSublinks(self, rawdata, baseurl):
		return []

	# main
	def exportPDF(self, infile, outfile):
		# debug option
		#debug = 0
		# input option
		password = ''
		pagenos = set()
		maxpages = 0
		# output option
		#outfile = None
		outtype = 'text'
		imagewriter = None
		rotation = 0
		layoutmode = 'normal'
		codec = 'utf-8'
		pageno = 1
		scale = 1
		caching = True
		showpageno = True
		laparams = LAParams()
		'''for (k, v) in opts:
			if k == '-d': debug += 1
			elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
			elif k == '-m': maxpages = int(v)
			elif k == '-P': password = v
			elif k == '-o': outfile = v
			elif k == '-C': caching = False
			elif k == '-n': laparams = None
			elif k == '-A': laparams.all_texts = True
			elif k == '-V': laparams.detect_vertical = True
			elif k == '-M': laparams.char_margin = float(v)
			elif k == '-L': laparams.line_margin = float(v)
			elif k == '-W': laparams.word_margin = float(v)
			elif k == '-F': laparams.boxes_flow = float(v)
			elif k == '-Y': layoutmode = v
			elif k == '-O': imagewriter = ImageWriter(v)
			elif k == '-R': rotation = int(v)
			elif k == '-t': outtype = v
			elif k == '-c': codec = v
			elif k == '-s': scale = float(v)'''
		'''#
		PDFDocument.debug = debug
		PDFParser.debug = debug
		CMapDB.debug = debug
		PDFResourceManager.debug = debug
		PDFPageInterpreter.debug = debug
		PDFDevice.debug = debug
		#'''
		rsrcmgr = PDFResourceManager(caching=caching)
		if outfile:
			outfp = file(outfile, 'w')
		else:
			outfp = sys.stdout
		#outtype == 'text':
		device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
							imagewriter=imagewriter)
		#for fname in args:
		fp = file(infile, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		for page in PDFPage.get_pages(fp, pagenos,
									  maxpages=maxpages, password=password,
									  caching=caching, check_extractable=True):
			page.rotate = (page.rotate+rotation) % 360
			interpreter.process_page(page)
		fp.close()
		device.close()
		outfp.close()
		return

	def _getTitle(self, url):
		return SeUtility.getTitleofShareFolderPath(url)
		# title = infile.split('_')
		# if len(title) <= 0:
		# 	return infile
		# title = title[len(title)-1]
		# title = title.split('.')
		# return title[0]


#for testing purpose
def main(argv):
	import getopt
	def usage():
		print ("usage: %s [-u user] [-p password] [-d dir]"
			   " file ..." % argv[0])
		return 100

	try:
		opts, args = getopt.getopt(argv[1:], "ho:v", ["user=", "password=", "dir="])
	except getopt.GetoptError as err:
		print str(err)
		return usage()
	#print opts
	if not opts: return usage()
	user = ""
	password = ""
	dir = ''
	print 'opts', opts
	for (k, v) in opts:
		if k in ("-u", "--user") : user = v
		elif k in ("-p", "--password") : password = v
		elif k in ('-d', "--dir") : dir = v
	if password == '':
		import getpass
		# password = getpass.getpass()
		password = "TongjiJackyuSAP2014"

	#openShareFolder(user, password)
	#path = r'\\10.58.0.100\Root\Business_One\Projects\Dev\SDK\KnowledgeWarehouse\_Ebook\java'
	path = r'//CNST50066074/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/java/m2ebook-pdf.pdf'
	from fetchFile import FetchFile
	fetcher = FetchFile(path, user, password) #openShareFolder()
	# try:
	s = fetcher.fetchData()
	print type(s)
	print s
	print 'code: ',fetcher.getResponseCode()
	parser = ParserPDF()
	dicIn = {ParseInputDS.RAWDATA:s}
	outpath = parser.parseContent(dicIn)
	print 'out file:', outpath

	# except Exception as e:
	#     # print 'exception.....', str(e)
	#     raise e
	# s = fetcher.fetchData()
	# print type(s)
	# print s
	print 'code: ',fetcher.getResponseCode()

# if __name__ == '__main__': sys.exit(exportPDF(r'Application Architecture Guide v2.pdf', r'result.txt'))
if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
