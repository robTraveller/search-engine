from resourceLink import ResourceLinkList
from multiprocessing import Process

list = ResourceLinkList()
#link = ResourceLink(addr='1')
#list.appendLink(link)
list.appendAddr('1')
list.appendAddr('2')
print list.size()
print list.getNextAddr()

#for path in list:
	#pass #print path
'''for link in list.getLinks().values():
	print type(link)
	print 'link:' + str(link)
	print 'link:' + link.getAddr()'''
	
'''for link in list:
	print type(link)
	print 'link:' + str(link)
	print link.getAddr()
	#print list.getLinks()[link].getAddr()'''
	

def crawlLinkage(linkList):
	print 'start search linkage...'
	try:
		STOP_LEVEL = 1 # Search to which level

		uid = request.POST.get('u_id', '')
		pwd = request.POST.get('u_pwd', '')
		nextLevelURLList = []

		for i in range(0, STOP_LEVEL):
			docList = [d.url for d in doc().getObjsByLevel(i)] #Documents.objects.filter(level = i)] #
			for addr in docList:
				linkList.append(addr)
			for url in nextLevelURLList:
				if doc.isURLExist(url) or url in docList:
					pass
				else:
					linkList.append(url)
					docList.append(url)
			nextLevelURLList = doSearchAction(uid, pwd, docList, i)
		print 'linkList Size:' 
		print linkList.size()
	except Exception as e:
		print '\nsomething error when search linkage!' + e.strerror


if __name__ == '__main__':
	linkList = ResourceLinkList()
	#crawlLinkage(linkList)
	print('create process')
	crawProcess = Process(target=crawlLinkage, args=(linkList,))
	crawProcess.start()
	print('create start')
	#searchWork()
	crawProcess.join()
