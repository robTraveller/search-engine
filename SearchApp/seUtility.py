__author__ = 'root'

class SeUtility:

	@classmethod
	def getTitleofShareFolderPath(cls, url):
		tempTitle = url.split('/')
		if len(tempTitle) > 1:
			if url.endswith('/'):
				return tempTitle[len(tempTitle)-2]
			else:
				return tempTitle[len(tempTitle)-1]
		elif len(tempTitle) > 0:
			return tempTitle[0]
		else:
			return url



# Unit Test here
def test_getTitleofShareFolderPath():
	print 'Start to test getTitleofShareFolderPath...'
	testUrls = ['//cnst50066074/root/Business_One/Knowledge_Warehouse/00_B1_Book_Library/B1_Booklist.xlsx',
				'//cnst50066074/root/Business_One/Knowledge_Warehouse/00_B1_Book_Library/',
				'//cnst50066074/root/Business_One/Knowledge_Warehouse/00_B1_Book_Library']
	try:
		for url in testUrls:
			print '    ' + SeUtility.getTitleofShareFolderPath(url)
	except Exception as e:
		print 'exception ' + str(e)
	print 'End to test getTitleofShareFolderPath\n'

def main(argv):
	test_getTitleofShareFolderPath()

# if __name__ == '__main__': sys.exit(exportPDF(r'Application Architecture Guide v2.pdf', r'result.txt'))
if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))