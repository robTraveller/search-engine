#from django.test import TestCase
#from crawler import Crawler_client
from fetchData import getFetcher

# Create your tests here.


#client = Crawler_client("http://www.baidu.com", "t", "t")

fetch = getFetcher(addr = r'https://wiki.wdf.sap.corp/wiki/display/wikisys/All+Spaces', uid = 'i076639', upwd ='')
html = fetch.fetchData()

f = open('data.html', 'w')
f.write(html)
f.close()
