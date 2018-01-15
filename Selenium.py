#coding:utf-8
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class seleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def testEle(self):
        driver = self.driver
        driver.get('http://www.douyu.com/directory/all')
        soup = BeautifulSoup(driver.page_source, 'xml')
        page = 1
        while True:
            print "------------------On Page {}-------------------".format(page)
            parent = soup.find('div', id='live-list-content')
            titles = parent.find_all('h3', {'class': 'ellipsis'})
            nums = parent.find_all('span', {'class': 'dy-num fr'})
            for title, num in zip(titles, nums):
                print title.get_text().strip(), num.get_text()
            if driver.page_source.find('shark-pager-disable-next') != -1:
                print "--------------------Last Page now--------------"
                break
            elem = driver.find_element_by_class_name('shark-pager-next')
            time.sleep(1)
            if not elem is None:
                elem.click()
                time.sleep(3)
            else:
                print "Next button not found"

            page += 1
            soup = BeautifulSoup(driver.page_source, 'xml')

    def tearDown(self):
        print 'down'

if __name__ == "__main__":
    unittest.main()
