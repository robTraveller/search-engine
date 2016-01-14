#import inspect
#filename, linenum, funcname = inspect.getframeinfo(inspect.currentframe())[:3] 
#import traceback
from multiprocessing import Process
import datetime

def printLog(proc, *arg):
	# return
	if isinstance(proc, Process) and proc != None:
		if proc.name == '_indexer' or proc.name == '_sublinkCrawler' or proc.name.startswith('content%'):
			return
		#print type(proc)
		print datetime.datetime.now().strftime("%Y %d %B %I:%M%p"), ' pid:', proc.pid, ' name:', proc.name,
	else:
		print datetime.datetime.now().strftime("%Y %d %B %I:%M%p"), proc,
	for s in arg:
		print s,
	print ''
	
	'''try: # just get a few frames
		f = traceback.extract_stack(limit=2)
		if f:
			print f[0]
	except:
		if __debug__:
			traceback.print_exc()
		pass'''
