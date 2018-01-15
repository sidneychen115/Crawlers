# -*- coding:utf-8 -*-

import urllib2
import re

class Baidutieba:

    def __init__(self, pageURL):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.url = pageURL + "?see_lz=1"
        self.data = []

    def readPage(self):

        try:
            request = urllib2.Request(self.url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageData = response.read().decode("utf-8")

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None

        totalPage = self.countPage(pageData)
        if totalPage < 0:
            print u"读取页面失败，页面不存在, 请重新输入"
            return 1
        print u"共发现%d页楼主发布内容" % (totalPage)

    def countPage(self, pageData):
        pageCountPattern = re.compile('class="red">(\d+?)</span>', re.S)
        match = re.search(pageCountPattern,pageData)

        if not match:
            return -1
        return int(match.group(1))


print u"百度贴吧爬虫程序，请输入页面编码如 https://tieba.baidu.com/p/xxxxxxxx"

url = "https://tieba.baidu.com/p/" + str(raw_input("https://tieba.baidu.com/p/"))

tiebaReader = Baidutieba(url)
tiebaReader.readPage()

print u"程序结束" \
      u""