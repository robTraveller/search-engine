__author__ = 'root'
from docx import Document
from docx.shared import Inches
from parseDataBase import ParserSuper
from parseDataBase import ParseInputDS
import os
from seUtility import SeUtility

class ParsePPT(ParserSuper):
	def parseContent(self, dicInput):
		inFilePath = dicInput[ParseInputDS.RAWDATA]
		url = dicInput[ParseInputDS.RESOURCEADDR]
		outFilePath = inFilePath.replace('.', '_') + '.txt'
		try:
			self.exportPPT(inFilePath, outFilePath)
			os.remove(inFilePath)
		except Exception as e:
			print e
			raise e
		self._title = self._getTitle(url)
		return self._title, outFilePath


	def exportPPT(self, infile, outfile):
		(fi, fo, fe) = os.popen3('catppt "%s" > "%s"' % (infile, outfile))
		fi.close()
		retval = fo.read()
		erroroutput = fe.read()
		fo.close()
		fe.close()
		if not erroroutput:
			return
		else:
			raise OSError("Executing the command caused an error: %s" % erroroutput)

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
	user = 'I302581'
	password = ''
	if password == '':
		import getpass
		password = getpass.getpass()
		# password = '***'

	#openShareFolder(user, password)
	#path = r'\\10.58.0.100\Root\Business_One\Projects\Dev\SDK\KnowledgeWarehouse\_Ebook\java'
	# path = r'//CNST50066074/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/java/m2ebook-pdf.pdf'
	path = r'//pvgn50863254a/share/DOCTEST/automation.ppt'
	from fetchFile import FetchFile
	fetcher = FetchFile(path, user, password) #openShareFolder()
	# try:
	s, url, fileType = fetcher.fetchData()
	print type(s)
	print s
	print 'code: ',fetcher.getResponseCode()
	parser = ParsePPT()
	dicIn = {ParseInputDS.RAWDATA:s}
	outpath = parser.parseContent(dicIn)
	print 'out file:', outpath
	print 'code: ',fetcher.getResponseCode()

# if __name__ == '__main__': sys.exit(exportPDF(r'Application Architecture Guide v2.pdf', r'result.txt'))
if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
