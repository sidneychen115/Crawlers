# -*- coding:utf-8 -*-
import urllib2
import re

url = "https://www.walmart.com/browse/jewelry/3891?grid=true&page=1#searchProductResult"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
headers = {"user-agent": user_agent}

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
pageData = response.read().decode('utf-8')

pattern = re.compile('{"productId":(.*?)},', re.S)
#match = re.search(pattern,pageData)

#print match.group(1)


productList = re.findall(pattern,pageData)
print "There are %d items" %(len(productList))


for item in productList:
    print item

'''
match = re.search('<span class="product-sales.*?(\d+\.\d{2}?)</s', productList[0], re.S)

if match is None:
    print "Not Found"
    exit(1)

test_string = match.group(1)

print test_string
'''