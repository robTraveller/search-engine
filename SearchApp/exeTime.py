import time
import os

DEBUG_FILE_PATH = 'debug/log_debug.txt'

def exeTime(func):
	def newFunc(*args, **args2):
		t0 = time.time()
		f = open(os.path.realpath(DEBUG_FILE_PATH), 'w')
		f.write('\n' + "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
		print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
		back = func(*args, **args2)
		f.write('\n' + "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
		print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
		f.write('\n' + "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
		print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
		f.close()
		return back
	return newFunc
