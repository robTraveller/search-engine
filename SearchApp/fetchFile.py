# -*- encoding: utf-8 -*-

from fetchDataBase import FetchDataBase
import base64, os
#from parserPdf import exportPDF
from smb.SMBConnection import SMBConnection
from const_file_type import *

PLACEHOLDER_START = '//'
PLACEHOLDER = '/'
SF_TEMPPATH = "./temp/"

class FetchFile(FetchDataBase):
	_localFolder = ''
	_serverName = ''
	_rootNode = ''
	_subPath = ''
	_conn = None
	_filename = ''
	#_folderList = []
	#_fileList = []
	def __init__(self, addr, uid, upwd):
		#super(FetchFile, self).__init__(addr, uid, upwd)
		# print 'addr:', addr
		try:
			# FetchDataBase.__init__(self, r'//CNST50066074/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/java/m2ebook-pdf.pdf', uid.lower(), upwd)
			FetchDataBase.__init__(self, str(addr), uid.lower(), upwd)
			self._genPath()
		except Exception as e:
			self._responseCode = 430
			print 'init error....'
			raise e

	def _genPath(self):
		rootPath = self._addr
		self._localFolder = self._addr
		#skip first domain path, ie "\\servername\path\
		# print 'self._addr:', self._addr
		if self._addr.startswith(PLACEHOLDER_START):
			if len(self._addr) <= 2:
				raise Exception('not support"', self._addr, '"root path')
			else:
				rootPath = self._addr[2:]

			#get servername
			index = rootPath.find(PLACEHOLDER)
			if index > 0:
				self._serverName = rootPath[0:index]
				rootPath = rootPath[index+1:]
			else:
				#ie \\servername\
				self._serverName = rootPath
				rootPath = ''
		else:
			raise Exception('invalid net work path')

		#local temp path
		self._localFolder = base64.b64encode(self._addr)

		#find root path, ie path\
		index = rootPath.find(PLACEHOLDER)
		if index > 0:
			self._rootNode = rootPath[0:index]
			self._subPath = rootPath[index:]
		else:
			self._rootNode = rootPath
			self._subPath = ''
			#raise Exception('invalid path ')
		#print 'rootNode', self._rootNode
		#print 'subpath', self._subPath

	def _connToServer(self):
		try:
			#print 'id:', self._uid
			# print 'servername', self._serverName
			self._conn = SMBConnection(self._uid, self._upwd, '', self._serverName) #use_ntlm_v2 = True
			if not self._conn.connect(self._serverName): #port = 139
				raise Exception('connect failure:', self._serverName)
		except Exception as e:
			print str(e)

	def _connClose(self):
		self._conn.close()

	FOLDERLIST = 'folderlist'
	FILELIST = 'filelist'
	def _getFileList(self, subFolder = ''):
		if subFolder == '':
			subFolder = self._subPath
		print 'rootnode:', self._rootNode
		print 'subFolder:', subFolder
		list = self._conn.listPath(self._rootNode, subFolder)
		folderList = []
		fileList = []
		for f in list:
			if f.filename in ['.','..','Thumbs.db']:
				continue
			if f.isDirectory:
				folderList.append(f.filename)
			else:
				fileList.append(f.filename)
		folderList.append('')
		#print folderList, fileList
		return {self.FOLDERLIST:folderList, self.FILELIST:fileList}

	def _getLastFilePath(self, path):
		index = path.rfind(PLACEHOLDER)
		#print 'getlastfilepath index:', index
		if index < 0:
			return {'path':'', 'file':path}
			#raise Exception('not found last path')
		if index + 1 == len(path):
			#print 'index', index
			#print 'len(path):', len(path), path
			path = path[0:index]
			return self._getLastFilePath(path)
		else:
			return {'path':path[0:index+1], 'file':path[index+1:]}


	#TYPE_FOLDER = 'folder'
	#TYPE_FILE = 'file'
	# folder or file
	def _getFileType(self):
		#get path
		dpath = self._getLastFilePath(self._subPath)
		path = dpath['path']
		file = dpath['file']
		#print 'path', path
		#print 'file', file
		self._filename = file
		#
		dlist = self._getFileList(path)
		folderList = dlist[self.FOLDERLIST]
		fileList = dlist[self.FILELIST]

		if file.decode('utf-8') in folderList:
			self._resourceType = TYPE_FOLDER
			return TYPE_FOLDER
		if file.decode('utf-8') in fileList:
			self._resourceType = TYPE_FILE
			return TYPE_FILE
		return None

	#if folder return filelist, if file return filepath.
	def _getContent(self):
		type = self._getFileType()
		#print 'content type', type
		if type == TYPE_FOLDER:
			dfiles = self._getFileList()
			#print 'dfiles', dfiles
			#dfiles['type'] = TYPE_FOLDER
			files = []
			files.extend(dfiles[self.FOLDERLIST])
			files.extend(dfiles[self.FILELIST])
			return TYPE_FOLDER, str(files)
		elif type == TYPE_FILE:
			# return {'filepath':self._retrieveFile()}
			tempResult = self._retrieveFile()
			# return TYPE_FILE, self._retrieveFile()
			return TYPE_FILE, tempResult
		else:
			return None, None

	def _retrieveFile(self):
		tempPath = SF_TEMPPATH
		self.mkdir(tempPath)
		import os
		filename =  self._addr.replace('/', '_')
		tempPath = os.path.realpath(tempPath + filename)
		import tempfile
		with open(tempPath, 'wb+') as fo:
			#fp = tempfile.NamedTemporaryFile()
			fa, filesize = self._conn.retrieveFile(self._rootNode, self._subPath, fo)
			#print 'filesize', filesize
			#for line in fp:
			#	fo.write(line)
			#fp.close()
			fo.close()
		return tempPath

	def _detectFileType(self, fileType):
		from const_file_type import GLOBAL_FILE_TYPE
		if fileType == TYPE_FOLDER:
			return GLOBAL_FILE_TYPE.SF
		elif fileType == TYPE_FILE:
			if self._addr.lower().endswith('.pdf'):
				return GLOBAL_FILE_TYPE.PDF
			elif self._addr.lower().endswith('.doc'):
				return  GLOBAL_FILE_TYPE.DOC
			elif self._addr.lower().endswith('.docx'):
				return GLOBAL_FILE_TYPE.DOCX
			elif self._addr.lower().endswith('.ppt'):
				return GLOBAL_FILE_TYPE.PPT
		return GLOBAL_FILE_TYPE.OTHERS

	def fetchData(self):
		try:
			self._connToServer()
			fileType, content = self._getContent()
			#print 'content', content
			self._connClose()
			if content == None:
				self._responseCode = 430
				e = Exception()
				e.code = 430
				e.message = "Wrong url, can not fetch url"
				raise e
			self._responseCode = 200
			return content, self._addr, self._detectFileType(fileType)
		except Exception as e:
			self._responseCode = 430
			e.code = 430
			raise e


	#using mount to open share folder, not working at now.
	def _openShareFolder(self):
		#//10.58.0.100/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/Effective STL.pdf
		tempPath = "../temp/"
		tempPath += self._localFolder
		self.mkdir(tempPath)

		#print 'absolute path'
		tempPath = os.path.realpath(tempPath)
		print tempPath

		command = r"sudo mount.cifs " + self._addr + " " + tempPath + "/ -o user=" + self._uid + r",password="
		print command
		try:
			os.system(command + self._upwd)
		except Exception, e:
			print e
			raise e

	def mkdir(self, path):
		if not os.path.exists(path):
			os.makedirs(path)


	def _getFolderList(self):
		if self._localFolder == '':
			return
		for path in os.walk(self._localFolder):
			if not os.path.isdir(path):
				print path


#for testing purpose
def main(argv):
    import getopt
    def usage():
        print ("usage: %s [-u user] [-p password] [-d dir]"
               " file ..." % argv[0])
        return 100

    try:
        opts, args = getopt.getopt(argv[1:], "ho:v", ["user=", "password=", "dir="])
    except getopt.GetoptError as err:
        print str(err)
        return usage()
    #print opts
    if not opts: return usage()
    user = ""
    password = ""
    dir = ''
    print 'opts', opts
    for (k, v) in opts:
        if k in ("-u", "--user") : user = v
        elif k in ("-p", "--password") : password = v
        elif k in ('-d', "--dir") : dir = v
    if password == '':
        import getpass
        password = getpass.getpass()

    #openShareFolder(user, password)
    #path = r'\\10.58.0.100\Root\Business_One\Projects\Dev\SDK\KnowledgeWarehouse\_Ebook\java'
    # path = r'//CNST50066074/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/java/m2ebook-pdf.pdf'
    path = r'//CNST50066074/Root/Business_One/Projects/Dev/SDK/KnowledgeWarehouse/_Ebook/'
    fetcher = FetchFile(path, user, password) #openShareFolder()
    try:
    	s = fetcher.fetchData()
    	print type(s)
    	print s
    except Exception as e:
    	print 'exception.....', str(e)
    # s = fetcher.fetchData()
    # print type(s)
    # print s
    print 'code: ',fetcher.getResponseCode()
    #print 'user', user
    #dir = path
    #print 'dir', dir
    #print FetchFile(dir, user, password).getFolderList()

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
#sys.exit(openShareFolder(r"Application Architecture Guide v2.pdf", r"result.txt"))
