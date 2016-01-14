# Create your views here.
import sys
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
#from models import Documents
from resAddr import ResAddr
# Add sphinxapi support here
from sphinxapi import *
from crawler import *
# Add support of django auto paging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages

from WebPageTools import validate
from WebPageTools import do_syscmd_reindexer

from django.views.generic import ListView

from multiprocessing import Process
from resourceLink import ResourceLinkList
from fetchData import getFetcher
import time
import datetime
from multiprocessing.managers import BaseManager
#from works import IndexKeeper, SubLinkCrawler, ContentCrawler, startProcess
from works import processer

class MyManager(BaseManager):
	pass

# config view
class config(ListView):
	#reference URL
	#https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-display/
	#https://docs.djangoproject.com/en/1.6/topics/class-based-views/intro/
	model = ResAddr.document

	#specify the template name
	template_name = 'config.html'

	def get(self, request):
		return self.getURLList(request)

	def post(self, request):
		return self.addPath(request)

	def delete(self, request):
		print 'test delete'
		return self.getURLList(request)

	def addPath(self, request):
		if request.method == 'POST':
			# print request
			s_path = request.POST.get('s_path', '')
			if s_path in [None, '']:
				return self.getURLList(request)
			ResAddr(s_path).save()
		return self.getURLList(request)

	# get url list
	def getURLList(self, request):
		searchList = ResAddr().getAll()
		return render_to_response(self.template_name, {'s_list': searchList},context_instance=RequestContext(request))


	#GET method as_view will call get_context_data
	#deprecated
	def get_context_data2(self, **kwargs):
		context = super(configObj, self).get_context_data(**kwargs)
		context['s_list'] = self.getPathList()
		return context

	def getPathList(self):
		return ResAddr().getAll()

	# get url list
def getURLList( request):
	searchList = ResAddr().getAll()
	return render_to_response('config.html', {'s_list': searchList},context_instance=RequestContext(request))

def deleteURLList(request):
	if request.method == 'POST':
		# print request
		documentId = request.POST.get('d_id',-1)
		print 'documentId=' + str(documentId)
		if documentId == -1:
			return getURLList(request)
		#ResAddr().getById(documentId).delete()
		ResAddr().delById(documentId)
	return getURLList(request)



def searchURLList(request):
	if request.method == 'POST':
		print 'start search...'
		try:
			STOP_LEVEL = 2 # Search to which level
			# https://wiki.wdf.sap.corp/wiki/display/wikitrain/Getting+Started
			uid = request.POST.get('u_id', '')
			pwd = request.POST.get('u_pwd', '')
			tempDocList = []
			completedList = [] # Already searched url list

			for i in range(0, STOP_LEVEL):
				docList = [d.url for d in ResAddr().getObjsByLevel(i)] #Documents.objects.filter(level = i)] #
				# docList.append(tempDocList)
				# Remove urls which already searched
				# Add new urls into completed and to do list
				for url in tempDocList:
					if url in completedList or url in docList:
						pass
					else:
						docList.append(url)
						completedList.append(url)
				tempDocList = doSearchAction(uid, pwd, docList, i)
		except:
			print '\nsomething error!'
		print 'end search...'
		do_syscmd_reindexer()
		return getURLList(request)
	return ''

# Search action code here
def doSearchAction( uid, pwd, pathList, level):
	nextLevelURLList = []
	client = Crawler_client(uid, pwd)
	for path in pathList:
		if len(path)>0 and validate(path):
			print '\nstart search: %s' % path
			resultURLs = []
			try:
				resultURLs = client.start_fetch(path, level)
			except Exception, e:
				print 'failed. path:%s, level:%s, Exception:%s' % (path, level, e)
			for url in resultURLs:
				if url in nextLevelURLList:
					pass
				else:
					nextLevelURLList.append(url)
	return nextLevelURLList



def searchURLListEnhance(request):
	if request.method == 'POST':
		print 'start searchURLListEnhance...'
		try:
			#print 'sart process'
			#processes.start()
			#linkList = ResourceLinkList(uid = request.POST.get('u_id', ''), upwd = request.POST.get('u_pwd', ''))
			processer.setUserInfo(uid = request.POST.get('u_id', ''), upwd = request.POST.get('u_pwd', ''))
			
			'''MyManager.register('linkList', ResourceLinkList)
			manager = MyManager()
			manager.start()
			linkList = manager.linkList(uid = request.POST.get('u_id', ''), upwd = request.POST.get('u_pwd', ''))
			print('create process')
			
			indexer = IndexKeeper(linkList)
			indexer.start()
			print 'indexKeeper start'
			
			ContentCrawler = ContentCrawler(linkList)
			ContentCrawler.start()
			print 'contentCrawler start'
			
			depth = 1
			sublinkCrawler = SubLinkCrawler(linkList, depth)
			sublinkCrawler.start()
			print 'sublinkCrawler start'

			indexer.join()
			ContentCrawler.join()
			sublinkCrawler.join()
			print('process all start')'''
			
		except Exception, e:
			print '\nsomething error! %s' %e #+ sys.exc_info()[0]
		print 'end searchURLListEnhance...'
		#do_syscmd_reindexer()
		return getURLList(request)
	return ''

#processes = startProcess()