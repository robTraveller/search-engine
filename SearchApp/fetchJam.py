from fetchDataBase import FetchDataBase
import re
from WebPageTools import decompress
from urllib2 import HTTPError
from const_file_type import *
import urllib, urllib2

class FetchJamData(FetchDataBase):
	loginSign = False
	_loginUrls = {'https://jam4.sapjam.com/auth/request_login_help', 'https://jam4.sapjam.com/saml/saml2_sso?company_id=sf&idp=accounts-jamatsap.sap.com'}

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
	
	# Get data from specific sub url
	def fetchData(self):
		try:
			result =  self.fetch(addr=self._addr)
			return result,self._addr, self._detectFileType(self._addr)
		except HTTPError as e:
			print 'Exception:\n    code:%s, msg:%s' % (e.code, e.msg)
			temp =  self.exceptionHandler()
			print 'end handling.'
			return temp,self._addr, self._detectFileType(self._addr)
		except Exception as e:
			print 'Exception:\n    %s' % str(e)

	# Inner function.
	# The real function do net work.
	def fetch(self, addr, data=None, hds={}):
		if not data:
			dt = None
		else:
			dt = urllib.urlencode(data)
		req = urllib2.Request(url=addr, data=dt, headers=hds)
		opener = self._openerHelper.getOpener(self._addr)
		response = opener.open(req)
		# redirected = (response.url == addr)
		if response.url in self._loginUrls:
			raise HTTPError(addr, 400, 'need login first', None, None)
		self._responseCode = response.code
		html = response.read()
		return html

	# Handler http error one time.
	# Do login process here.
	def exceptionHandler(self):
		try:
			self.loginJam()
			# Refetch the failed url data
			return self.fetch(addr=self._addr)
		except Exception as e:
			print 'Failed handling http error manually! \nException: %s' % str(e)

	# Do login action
	def loginJam(self):
		print 'start login...'
		# step #03
		hds = { 'User-Agent': 'Fiddler',
			'Cookie': '_ct_sso=jamatsap.com'
		}
		response = self.fetch('https://jam4.sapjam.com/saml/saml2_sso',{},hds)
		res = re.search(r'value="([^"]*)"',response)
		SAMLRequest = res.group(1)
		# step #04
		hds = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Origin': 'https://jam4.sapjam.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'https://jam4.sapjam.com/saml/saml2_sso',
			'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'en-US,en;q=0.8'
		}
		data = {'SAMLRequest':SAMLRequest}
		response = self.fetch('https://accounts.sap.com/saml2/idp/sso/accounts.sap.com?bplte_company=sf', data, hds)
		response = decompress(response)
		res = re.search(r'name=\"loginXSRF\" value=[\'|\"]([^\'|\"]*)[\'|\"]', response)
		loginXSRF = res.group(1)
		# step #05
		hds = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Origin': 'https://accounts.sap.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'https://accounts.sap.com/saml2/idp/sso/accounts.sap.com?bplte_company=sf',
			'Accept-Encoding': 'gzip',
			'Accept-Language': 'en-US,en;q=0.8'
		}
		data = {'method':'POST',
			'idpSSOEndpoint':'https://accounts.sap.com/saml2/idp/sso/accounts.sap.com',
			'SAMLRequest':SAMLRequest,
			'loginXSRF':loginXSRF,
			'targetUrl':'https://www.cubetree.com/c/jamatsap.com/auth/status',
			'sourceUrl':'https://www.cubetree.com/c/jamatsap.com/auth/status',
			'org':'',
			'j_username':'I302581',
			'j_password':'TongjiJackyuSAP2014'}
		response = self.fetch('https://accounts.sap.com/saml2/idp/sso/accounts.sap.com', data, hds)
		response = decompress(response)
		res = re.search(r'name=\"SAMLResponse\" value=[\'|\"]([^\'|\"]*)[\'|\"]', response)
		SAMLResponse = res.group(1)
		# step #06
		hds = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Origin': 'https://accounts.sap.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'https://accounts.sap.com/saml2/idp/sso/accounts.sap.com',
			'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'en-US,en;q=0.8'
		}
		data = {'SAMLResponse':SAMLResponse}
		response = self.fetch('https://jam4.sapjam.com/saml/saml2_acs?idp=accounts-jamatsap.sap.com', data, hds)
		self._openerHelper.setLoginJam(True)
		print 'end login...'
