import urllib, urllib2, cookielib
from urllib2 import HTTPError
from fetchDataBase import FetchDataBase
from logger import printLog
from urllib2 import HTTPError
from const_file_type import *
import re

class FetchWikiData(FetchDataBase):

	# _selfInstance = None
	#
	def __init__(self, addr, uid, upwd):
		FetchDataBase.__init__(self, addr, uid, upwd)
		self._resourceType = TYPE_DEFAULT

	def _detectFileType(self, url):
		# TODO: need add function to detect pdf, doc file
		from const_file_type import GLOBAL_FILE_TYPE
		if url.startswith('https://wiki'):
			return GLOBAL_FILE_TYPE.WIKI
		elif url.startswith('https://jam'):
			return GLOBAL_FILE_TYPE.JAM
		else:
			return GLOBAL_FILE_TYPE.OTHERS

	def fetchData(self, url = None):
		try:
			if url == None:
				url = self._addr
			else:
				url = url
			content = self._fetch(url)
			return content,url, self._detectFileType(url)
		except HTTPError as e:
			print 'Exception:\n    code:%s, msg:%s' % (e.code, e.msg)
			temp =  self._exceptionHandler(url)
			print 'end handling.'
			return temp,url, self._detectFileType(url)
		except Exception as e:
			print 'Exception:\n    %s' % str(e)

	def _fetch(self, searchUrl):
		opener = self._openerHelper.getOpener(self._addr)
		response = opener.open(searchUrl)
		if re.search(r'login\.action', response.url):
			self._responseCode = response.code
			raise HTTPError(self._addr, 400, 'Need wiki login first!', None, None)
		return response.read()

	def _exceptionHandler(self, searchUrl):
		try:
			return self._doLogin(searchUrl)
		except Exception as e:
			print 'fetchWiki,exceptionHandler, error, e: %s' % str(e)

	def _doLogin(self, searchUrl):
		login_data = urllib.urlencode({'os_username' : self._uid, 'os_password' : self._upwd})
		opener = self._openerHelper.getOpener(self._addr)
		response = opener.open(searchUrl, login_data)
		self._responseCode = response.code
		html = response.read()
		return html

	# Left navigation links
	def fetchNaviData(self, pageId = 17728069):
		tempUrl = 'https://wiki.wdf.sap.corp/wiki/plugins/pagetree/naturalchildren.action?hasRoot=true&pageId=' + str(pageId)
		tempSource, url, fileType = self.fetchData(url = tempUrl)
		rawResult = {}
		rawResult['data'] = tempSource
		rawResult['url'] = tempUrl
		return rawResult

	# # Get data from specific sub url
	# def fetchData(self):
	# 	#set as non-proxy
	# 	proxy_support = urllib2.ProxyHandler({})
	# 	#proxy = urllib2.build_opener(proxy_support)
	# 	#urllib2.install_opener(proxy)
	# 	#with cookie
	# 	cj = cookielib.CookieJar()
	# 	opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor(cj))
	# 	login_data = urllib.urlencode({'os_username' : self._uid, 'os_password' : self._upwd})
	# 	# print("login_data:" + login_data)
	# 	#acess web
	# 	URL = self._addr
	# 	try:
	# 		opener.open(URL, login_data)
	# 		response = opener.open(URL)
	# 		self._responseCode = response.code
	# 		print self._responseCode
	# 		html = response.read()
	# 		'''f = open('data.html', 'w')
	# 		f.write(html)
	# 		f.close()'''
	# 		# f = open(URL.replace('.','_').replace('/','_').replace(':','_') + '.html', 'w')
	# 		# f.write(html)
	# 		# f.close()
	# 		return html
	# 	except Exception, e:
	# 		#printLog('FetchWikiData something error!', e)
	# 		printLog( 'Exception:\n   msg:' , e)
	# 		raise e

#for testing purpose
def main(argv):
	import getopt
	def usage():
		print ("usage: %s [-u user] [-p password] [-d dir]"
			   " file ..." % argv[0])
		return 100

	try:
		opts, args = getopt.getopt(argv[1:], "ho:v", ["user=", "password="])
	except getopt.GetoptError as err:
		print str(err)
		return usage()
	#print opts
	if not opts: return usage()
	user = ""
	password = ""
	print 'opts', opts
	for (k, v) in opts:
		if k in ("-u", "--user") : user = v
		elif k in ("-p", "--password") : password = v
	if password == '':
		import getpass
		password = getpass.getpass()

	#openShareFolder(user, password)
	#path = '"\\\\10.58.0.100\\Root\\Business_One\\Projects\\Dev\\SDK\\KnowledgeWarehouse\\_Ebook\\java\\"'
	# path = r'//10.58.0.100/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/java/'
	#FetchFile(path, user, password).openShareFolder()
	# print 'user', user
	# print 'dir', dir
	# print unicode(FetchWikiData(dir, user, password).fetchData())
	firstUrl = 'https://wiki.wdf.sap.corp/wiki/pages/viewpage.action?title=Home&spaceKey=NWCtx711SP'
	secondUrl = 'https://wiki.wdf.sap.corp/wiki/plugins/pagetree/naturalchildren.action?hasRoot=true&pageId=17728069'
	FetchWikiData(firstUrl, user, password).fetchData()
	FetchWikiData(secondUrl, user, password).fetchData()

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
#sys.exit(openShareFolder(r"Application Architecture Guide v2.pdf", r"result.txt"))
