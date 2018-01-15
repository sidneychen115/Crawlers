# -*- coding: utf-8 -*-
import urllib2
import re
import xlrd
from xlutils.copy import copy
import xlwt


class ExcelUtils:

    def __init__(self, filename):
        self.filename = filename

    def createExcel(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        sheet1.write(0, 0, 'Product Name')
        sheet1.write(0, 1, 'Standard Price')
        sheet1.write(0, 2, 'Sale Price')
        sheet1.write(0, 3, 'Saved')
        sheet1.write(0, 4, 'Discount')
        sheet1.write(0, 5, 'Link')

        workbook.save(self.filename)

    def writeExcel(self, data):
        rexcel = xlrd.open_workbook(self.filename,  encoding_override="utf-8")
        rows = rexcel.sheets()[0].nrows
        excel = copy(rexcel)
        table = excel.get_sheet(0)
        while len(data) > 0:
            writeContent = data[0]
            for column in range(0, 6):
                table.write(rows,column,writeContent[column])
            rows += 1
            del data[0]
        excel.save(self.filename)


class Walmart:

    def __init__(self, URL, maxPage):
        self.url = URL
        self.maxPage = maxPage
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        self.headers = {"user-agent": self.user_agent}
        self.productData = []
        self.excelFileName = "D:\\tmp\\walmart.xls"

    def startRead(self):

        excelWriter = ExcelUtils(self.excelFileName)
        excelWriter.createExcel()

        for page in range(1,self.maxPage+1):
            replaceStr = "page=%d" %(page)
            print "page: "+ str(page)
            currentPageURL = re.sub('page=\d+', replaceStr, self.url)
            pageData = self.loadPage(currentPageURL)
            productList = self.getProductItem(pageData)

            for product in productList:
                productInfo = self.getProductInfo(product)
                if productInfo is None:
                    continue
                self.productData.append(productInfo)
            excelWriter.writeExcel(self.productData)


    def loadPage(self, pageURL):
        request = urllib2.Request(pageURL, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    def getProductItem(self, pageData):
        pattern = re.compile('{"productId":(.*?)},', re.S)
        return re.findall(pattern, pageData)

    def getProductInfo(self, product):
        product_info = {}
        info_pattern_dict = {"StandardPrice": '"listPrice":(.*?),',
                             "SalePrice": '"offerPrice":(.*?),',
                             "ProductName": '"title":"(.*?)",',
                             "ProductLink": '"productPageUrl":"(.*?)",',
                             "SavingAmount": '"savingsAmount":(.*?),'}
        savingAmount = self.getInfo(product, info_pattern_dict['SavingAmount'])
        if not savingAmount:
            return None
        print "saving amount: " + savingAmount
        standardPrice = self.getInfo(product, info_pattern_dict['StandardPrice'])
        print "Offer price: " + standardPrice
        salePrice = self.getInfo(product, info_pattern_dict['SalePrice'])
        productName = self.getInfo(product, info_pattern_dict['ProductName'])
        productLink = "https://www.walmart.com" + self.getInfo(product, info_pattern_dict['ProductLink'])
        discount = self.calculateDiscount(standardPrice, savingAmount)
        product_info = {0: productName,
                        1: standardPrice,
                        2: salePrice,
                        3: savingAmount,
                        4: discount,
                        5: productLink}
        return product_info

    def getInfo(self, product, patternStr):
        pattern = re.compile(patternStr, re.S)
        match = re.search(pattern, product)
        if match:
            return match.group(1)
        return None

    def calculateDiscount(self, standardPrice, savingamount):
        f_standardprice = float(standardPrice)
        f_savingamount = float(savingamount)
        discount = round(f_savingamount / f_standardprice, 2)
        return discount

#reload(sys)
#sys.setdefaultencoding('utf8')

print sys.getdefaultencoding()

URL = raw_input("type URL:\n")
page = int(raw_input("type maximum page:\n"))



walmartCrawler = Walmart(URL,page)
walmartCrawler.startRead()