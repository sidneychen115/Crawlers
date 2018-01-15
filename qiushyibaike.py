# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class QSBK:

    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.pageIndex = 1
        self.headers = {'User-Agent' : self.user_agent}
        self.stories = []
        self.baseURL = 'http://www.qiushibaike.com/hot/page/'
        self.enable = False

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage(self.pageIndex)
        while self.enable:
            input = raw_input()
            if input =='Q':
                return
            if len(self.stories) == 0:
                self.pageIndex += 1
                self.loadPage(self.pageIndex)
            story = self.stories[0]
            print u"第%d页\t发布者:%s\t赞:%s\n%s" %(self.pageIndex, story[0], story[2], story[1])
            del self.stories[0]

    def loadPage(self, pageIndex):
        print u"正在加载第%d页" %(pageIndex)
        items = self.getStoryOnPage(pageIndex)
        for item in items:
            if item[2].strip()=='':
                replaceBR = re.compile('<br/>')
                content = re.sub(replaceBR, '\n', item[1])
                self.stories.append([item[0].strip(), content.strip(), item[3].strip()])
        print u"第%d页加载完毕" %(pageIndex)


    def getPageContent(self, pageIndex):
        pageURL = self.baseURL + str(pageIndex)
        request = urllib2.Request(pageURL, headers = self.headers)
        try:
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
           if hasattr(e, "reason"):
               print u"连接失败，错误原因", e.reason
               return None

    def getStoryOnPage(self, pageIndex):
        pageCode = self.getPageContent(pageIndex)
        if not pageCode:
            print u"页面加载失败"
            return None
        pattern = re.compile('<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<!--.*?-->(.*?)<div class="stats.*?"number">(.*?)</i>', re.S)
        items = re.findall(pattern,pageCode)
        return items

spider = QSBK()
spider.start()