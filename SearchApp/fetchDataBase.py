from openerHelper import OpenerHelper

class FetchDataBase:
	_uid = ''
	_upwd = ''
	_addr = ''
	_responseCode = 0
	_openerHelper = None
	_resourceType = ''
	
	def __init__(self, addr, uid, upwd):
		self._addr = addr
		self._uid = uid
		self._upwd = upwd
		self._openerHelper = OpenerHelper()
		print 'opener id:' + str(id(self._openerHelper))
	
	def getResponseCode(self):
		return self._responseCode
	
	def getType(self):
		return self._resourceType
	
	def fetchData(self):
		raise Exception('please implement fetchData', self.__class__.__name__)
		
