# -*- coding:utf-8 -*- 
import urllib
import urllib2
import os
import cookielib
from WebPageTools import getBaseURL
from Singleton import Singleton

# Single instance class
class OpenerHelper(object):
	__metaclass__ = Singleton
	_jamLoginSign = False

	# Inner class.
	# A struct: binding opener with cookie
	class openerwithcookie(object):
		_opener = None
		_cookie = None
		_cookiePath = None

		def __init__(self, baseUrl):
			self._opener = None
			self._cookie = None
			self._cookiePath = os.path.join(os.getcwd(), str(baseUrl).replace('.','_') + '.txt')
			self._loadCookie()
			cookieHandler = urllib2.HTTPCookieProcessor(self._cookie)
			self._opener = urllib2.build_opener(cookieHandler)
		# Return opener
		def getOpener(self):
			return self._opener
		# Detect whether cookie file exist.
		# If yes, use it; else create it.
		def _loadCookie(self):
			self._cookie = cookielib.MozillaCookieJar()
			if os.path.isfile(self._cookiePath):
				self._cookie.load(self._cookiePath)

		def saveCookie(self):
			self._cookie.save(self._cookiePath)
	_openerStructDic = {} # Opener dictionaries, with cookie init.
	# Get opener with url
	def getOpener(self, url):
		baseUrl = getBaseURL(url)
		if baseUrl not in self._openerStructDic:
			openerStruct = self.openerwithcookie(baseUrl)
			self._openerStructDic[baseUrl] = openerStruct
		return self._openerStructDic[baseUrl].getOpener()

	# Judge whether client helper has login JAM
	def isLoginJam(self):
		return self._jamLoginSign

	def setLoginJam(self, sign):
		self._jamLoginSign = sign
