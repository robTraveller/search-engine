__author__ = 'root'



############################################### For Parsers ########################################
# Can be reused!!! enum ds
# Usage:  Numbers = enum(ONE=1, TWO=2, THREE=3)
def enum(**enums):
	return type('Enum', (object,), enums)

# ParseInputDS	= enum(RAWDATA			= 'input_dict_rawdata',
# 					   RESOURCEADDR		= 'input_dict_resourceaddr',
# 					   TYPE				= 'input_dict_type')

# Old version of enum
class ParseInputDS(object):
	RAWDATA			= 'input_dict_rawdata'
	RESOURCEADDR		= 'input_dict_resourceaddr'
	TYPE				= 'input_dict_type'

# ParseInputType	= enum(HTML	=	1,
# 							JAM		=	2,
# 							WIKI	=	3,
# 							SF		=	4,
# 							PDF		=	5,
# 							TXT		=	6)
#
################### deprecated, use const_file_type instead now ##################
# # Old version of enum
# class ParseInputType(object):
# 	HTML	=	1
# 	JAM		=	2
# 	WIKI	=	3
# 	SF		=	4
# 	PDF		=	5
# 	TXT		=	6


################################### Parsers Super ######################################
# Parsers' super class
# Abstract class
# Can not be used directly
# Super class of parsers
class ParserSuper(object):

	def __init__(self):
		self._title = None

	# Interface: parse content
	def parseContent(self, dicInput):
		raise UnboundLocalError("Exception raised, no strategy 'parseContent' supplied to parser.")

	# # Interface: parse title
	# def getTitle(self):
	# 	if self._title:
	# 		return self._title
	# 	else:
	# 		return 'Default title ' + str(hash(unicode(self)))

	# Interface: parse sub links
	def getSublinks(self, rawdata, baseurl):
		return []
		# raise UnboundLocalError("Exception raised, no strategy 'getSublinks' supplied to parser.")