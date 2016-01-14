# __author__ = 'root'
# from parseHtml import ParseHtml
# from parseHtmlWiki import ParseHtmlWiki
# from parseHtmlJam import ParseHtmlJam
# from parserPdf import PDFParser
#
# # Can be reused!!! enum ds
# # Usage:  Numbers = enum(ONE=1, TWO=2, THREE=3)
# def enum(**enums):
# 	return type('Enum', (object,), enums)
#
# ParseInputDS	= enum(RAWDATA			= 'input_dict_rawdata',
# 					   LOCALPATH 		= 'input_dict_filepath',
# 					   RESOURCEADDR		= 'input_dict_resourceaddr',
# 					   TYPE				= 'input_dict_type')
#
# # Old version of enum
# # class ParseInputDS(object):
# # 	RAWDATA			= 'input_dict_rawdata'
# # 	LOCALPATH 		= 'input_dict_filepath'
# # 	RESOURCEADDR		= 'input_dict_resourceaddr'
# # 	TYPE				= 'input_dict_type'
#
# ParseInputType	= enum(HTML	=	1,
# 							JAM		=	2,
# 						 	WIKI	=	3,
# 						 	SF		=	4,
# 						 	PDF		=	5,
# 						 	TXT		=	6)
#
# # Old version of enum
# # class ParseInputType(object):
# # 	HTML	=	1
# # 	JAM		=	2
# # 	WIKI	=	3
# # 	SF		=	4
# # 	PDF		=	5
# # 	TXT		=	6
#
# # Parser factory
# class ParserFactory(object):
# 	parsers = {}
# 	parsers[ParseInputType.HTML] = ParseHtml()
# 	parsers[ParseInputType.JAM] = ParseHtmlJam()
# 	parsers[ParseInputType.WIKI] = ParseHtmlWiki()
# 	# parsers[ParseInputType.SF] =
# 	parsers[ParseInputType.PDF] = PDFParser()
#
# 	def parseContent(self, dictInput):
# 		type = dictInput[ParseInputDS.TYPE]
# 		if type in ParserFactory.parsers:
# 			return ParserFactory[type].parseContent(dictInput)
# 		else:
# 			print 'Parse input type undefined!'