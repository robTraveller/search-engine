from fetchWiki import FetchWikiData
from fetchJam import FetchJamData
from fetchFile import FetchFile
import re
from const_fetch_type import *

WIKI = r'https://wiki.wdf.sap.corp'

JAM = r'https://jam4.sapjam.com'

NETWORK_PATH = r'//'

def getFetcher(addr, uid, upwd):

	urlType = 0 # Default:0:Wiki 1:Jam 2:network_path
	if re.search(WIKI, str(addr)):
		urlType = WIKI_TYPE
	elif re.search(JAM, str(addr)):
		urlType = JAM_TYPE
	elif addr.startswith(NETWORK_PATH):
		urlType = NETWORK_PATH_TYPE
	
	if urlType == WIKI_TYPE:
		return FetchWikiData(addr, uid, upwd)
	elif urlType == JAM_TYPE:
		return FetchJamData(addr, uid, upwd)
	elif urlType == NETWORK_PATH_TYPE:
		return FetchFile(addr, uid, upwd)
	else:
		raise Exception('unknow link type')
		#return FetchWikiData(addr, uid, upwd)
		
		
	
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
		password = getpass.getpass()

	fetcher = getFetcher(dir, user, password).fetchData()
	htmlSource = fetcher.fetchData()
	f = open('test_wiki_fetch.html', 'w')
	f.write(htmlSource)
	f.close()
	print 'Rawdata: %s' % htmlSource
	print 'Response code: %s' % fetcher.getResponseCode()
	print 'Type: %s' % fetcher.getType()

if __name__ == "__main__": 
	import sys
	sys.exit(main(sys.argv))
	
'''if __name__ == "__main__": 
	import sys
	sys.exit(getFetcher('//', 'i076639', ''))'''
