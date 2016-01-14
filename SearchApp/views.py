# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from models import Documents
# Add sphinxapi support here
from sphinxapi import *
from crawler import *
# Add support of django auto paging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging
from django.contrib import messages

# Search action code here
# def doSearchAction(self, uid, pwd, path):
#     client = Crawler_client(path, uid)
#     client.start_fetch()

# # Update config(Documnets) table code here
# def updateDocAction(self, m_url, m_uid, m_title):
# 	user = t_user.objects.filter(url = m_url)
# 	if (user == null):
# 		user = t_user(url=m_url, uid=m_uid, title=m_title)
# 	else:
# 		user.uid = m_uid
# 	user.save()

# show all search history view
# def showAllSearch(request):
#     client = Crawler_client("", "","")#https://wiki.wdf.sap.corp/", "testID", "testPWD")
#     # client.start_fetch()
# 	searchList = t_user.objects.all()
#     return render_to_response('showAllSearch.html', {'s_list': searchList})

# Test sphinx search API here
def test(request):
	if request.GET:
		query = request.GET.get('q', '')
		s = SphinxClient()
		s.SetServer('localhost', 9312)
		s.SetLimits(0, 16777215)
		s.SetGroupBy('group_id', SPH_GROUPBY_ATTR, '@group desc')
		if s.Status():
			query_results = s.Query(query, 'test1') # Set your own index, here we use mytest.
			#print 'query results:' + str(query_results)
			total = query_results['total']
			matches = query_results['matches']
			# print 'result: %s' % query_results
			# print 'matches: %s' % matches

			content_ids = [match['id'] for match in query_results['matches']]
			#print 'ids is: %s' % content_ids
			# pages_id = 5
			find_documents = []
			if content_ids:
				for content_id in content_ids:
					#print 'test content_id' + str(content_id)
					content = Contents.objects.filter(id=content_id)
					try:
						content = content[0]
					except:
						continue
					doc_id = content.doc_id
					print 'contentid:' + str(content_id) + ', filter id:' + str(doc_id)
					document = Documents.objects.filter(id=doc_id)
					document = document[0]
					# print 'docid:' + str(doc_id) + ', filter title:' + str(document.title)
					find_documents.append({'title':document.title, 'url':document.url, 'content':content.paragraph})
			else:
				find_documents = None
			# Hightlight results found here!
			if find_documents:
				# contents
				docs = [doc['content'] for doc in find_documents]
				words = query
				index = 'test1'
				opts = {'before_match':'<b class="highlighted">', 'after_match':'</b>', 'chunk_separator':' ... ', 'limit':400, 'around':15}
				cl = SphinxClient()
				res = cl.BuildExcerpts(docs, index, words, opts) # Assign highlighted results back
				i = 0
				if len(res) > 0:
					for doc in find_documents:
						# print '\ninitial:' + doc['content']
						#print 'res' + str(res) + typeof(res)
						doc['content'] = res[i]
						i += 1
				# titles
				doc_titles = [doc['title'] for doc in find_documents]
				words = query
				index = 'test1'
				opts = {'before_match':'<b class="highlighted">', 'after_match':'</b>', 'chunk_separator':' ... ', 'limit':400, 'around':15}
				cl = SphinxClient()
				res = cl.BuildExcerpts(doc_titles, index, words, opts) # Assign highlighted results back
				i = 0
				if len(res) > 0:
					for doc in find_documents:
						# print '\ninitial:' + doc['title']
						#print 'res' + str(res) + typeof(res)
						doc['title'] = res[i]
						i += 1
				# print 'result:%s' % str(find_documents)
				for doc in find_documents:
					if doc['url'].startswith("//"):
						doc['url'] = "file:/" + doc['url']

			# Transfer and show page
			if find_documents:
				paginator = Paginator(find_documents, 5)
				page = request.GET.get('page')
				try:
					find_documents = paginator.page(page)
				except PageNotAnInteger:
					find_documents = paginator.page(1)
				except EmptyPage:
					find_documents = paginator.page(paginator.num_pages)
			return render(request, 'search.html',
						  {'results': find_documents, 'total': total,
						   'query': query})
		else:
			logger = logging.getLogger('helper')
			logger.error('Sphinxsearch Error! %s' % s.GetLastError())
			messages.add_message(request, messages.ERROR, 'Search server is '
								 'not responding. Administrator '
								 'has been informed.')
			return render(request, 'search.html', {})
	else:
		return render(request, 'search.html', {})

# Construct search procudre
def searchInSphinx(request,word):
	if request.GET:
		query = request.GET.get('q', '')
		s = SphinxClient()
		s.SetServer('localhost', 9312)
		s.SetLimits(0, 16777215)
		if s.Status():
			query_results = s.Query(query)
			total = query_results['total']
			pages_id = [doc['id'] for doc in query_results['matches']]
			if pages_id:
				results = Documents.objects.filter(id=pages_id)
			else:
				results = None
			if results:
				paginator = Paginator(results, 25)
				page = request.GET.get('page')
				try:
					results = paginator.page(page)
				except PageNotAnInteger:
					results = paginator.page(1)
				except EmptyPage:
					results = paginator.page(paginator.num_pages)
			return render(request, 'search.html',
						  {'results': results,'total': total,
						   'query': query})
		else:
			logger = logging.getLogger('helper')
			logger.error('Sphinxsearch Error! %s' % s.GetLastError())
			messages.add_message(request, messages.ERROR, 'Search server is '
								 'not responding. Administrator '
								 'has been informed.')
			return render(request, 'search.html', {})
	else:
		return render(request, 'search.html', {})
