from models import Documents
from django.db.models import Q
#import datetime
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.db import connection

class ResAddr:
	document = Documents
	url = ''
	urlList = []
	def __init__(self, s_path = ''):
		#self.documents = Documents(url=s_path)
		self.url = s_path

	def save(self):
		try:
			urlRecord = Documents.objects.filter(url=self.url)#self.documents.url)
			if urlRecord.count() == 0:
				Documents(url=self.url).save()
				print 'documents is added'
			return self.getIdByURL(self.url)
		except Documents.DoesNotExist:
			print 'does not exist'
		print 'documents already exist'
	
	def getIdByURL(self, vurl):
		doc = Documents.objects.filter(url = vurl)
		if doc.count() > 0:
			return doc[0].id
	
	def getAll(self):
		return Documents.objects.all()

	def getById(self, documentId):
		try:
			return Documents.objects.get(id=documentId)
		except Documents.DoesNotExist:
			print "table document doesn't exit"
		return None

	def delById(self, documentId):
		self.getById(documentId).delete()

	def getObjsByLevel(self, lvl):
		return Documents.objects.filter(level = lvl)
	
	def getObjsNeedRefreshLevel(self, lvl, endDelta):
		now = timezone.now()
		#start = now-timedelta(hours = startDelta)
		end = now-timedelta(hours = endDelta)
		#print 'start', start
		#print 'end' , end
		#print 'level', lvl
		cond1 = Q(level = lvl)
		cond2 = Q(date_searched__lt = end)
		cond3 = Q(date_searched__isnull=True)
		cond4 = Q(date_searched__exact =F('date_created'))
		cond5 = Q(error_msg__exact = '')
		cond6 = Q(error_msg__isnull = True)
		objs = Documents.objects.filter(cond1 & (cond2 | cond3 | cond4) & (cond5 | cond6))
		return objs
		#return Documents.objects.filter(level = lvl & (date_searched < (datetime.datetime.now()-timedelta(hours = 5)) | date_searched is None))
	
	def getObjsNeedRefresh(self, checkURL, endDelta = 1):
		now = timezone.now()
		end = now-timedelta(hours = endDelta)
		cond1 = Q(url = checkURL)
		cond2 = Q(date_searched__lt = end)
		cond3 = Q(date_searched__isnull=True)
		cond4 = Q(date_searched__exact =F('date_created'))
		#cond5 = Q(error_msg <> '')
		objs = Documents.objects.filter(cond1 & (cond2 | cond3 | cond4))# & cond5)
		return objs
		
	def isURLExist(self, checkURL):
		urlRecord = Documents.objects.filter(url= checkURL)
		if urlRecord.count() == 0:
			return False
		else:
			#print 'url exists in db, ',  checkURL
			return True
			
	def updateReponseCode(self, sid, code, url):
		if sid == None:
			self.saveReponseCode(code, url)
			return
		doc = Documents.objects.filter(id = sid)
		if (doc.count() > 0):
			doc = Documents.objects.filter(id = sid).update(error_code = code)
		else:
			self.saveReponseCode(code, url)
	
	def saveReponseCode(self, code, url):
		print 'saveresponsecode,' ,url, ',code,', code
		Documents(url=self.url, error_code = code).save();
		
	def saveResaddr(self, vurl, vlevel, vuid = '',  vtitle = ''):
		doc = Documents.objects.filter(url = vurl)
		if (len(doc) == 0):
			doc = Documents(url=vurl, uid=vuid, title=vtitle, level = vlevel)
			doc.save()
			#print 'create\n'
		else:
			if vuid != '':
				doc[0].uid = vuid
			doc[0].title = vtitle
			# doc.update()
			doc[0].save()
			doc = doc[0]
			#print 'update\n'
		return doc.id

	# Jack Yu --- added to be used in work.py line 297. getSubLinkList
	def saveNewResaddr(self, vurl, vlevel):
		doc = Documents.objects.filter(url = vurl)
		if (len(doc) == 0):
			doc = Documents(url=vurl,level = vlevel)
			doc.save()
		return doc.id
		
	def saveErrorMsg(self, vurl, msg):
		doc = Documents.objects.filter(url = vurl)
		if (len(doc) > 0):
			doc[0].error_msg = msg
			doc[0].save()
			doc = doc[0]
			#print 'update\n'
		return doc.id