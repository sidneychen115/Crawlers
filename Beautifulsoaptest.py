import urllib
from bs4 import BeautifulSoup
import re


urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

url_ = 'http://bt.askyaya.com/index.php?r=files/index&kw=snis-111'
html = urllib.urlopen(url_).read()
soap = BeautifulSoup(html,"lxml")

tables = soap.select('li[class="col-xs-12 list-group-item"]')

if len(tables) == 0:
    print "Not Found"

size = tables[0].find_all(class_=re.compile('warning'))[0].string

size = re.split('\s',size)

print size[0]
print size[1]


'''
pattern = re.compile("/view.*?=(.*)", re.S)
match = re.search(pattern,link)
magnet = "magnet:?xt=urn:btih:" + match.group(1)
print magnet
'''
print "Done"
