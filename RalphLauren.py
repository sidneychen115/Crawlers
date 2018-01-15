import urllib2
import re
import xlrd
from xlutils.copy import copy
import xlwt

class ExcelUtils:

    def __init__(self, filename):
        self.filename = filename

    def createExcel(self):
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        sheet1.write(0, 0, 'Brand Name')
        sheet1.write(0, 1, 'Product Name')
        sheet1.write(0,2, 'Standard Price')
        sheet1.write(0,3, 'Sale Price')
        sheet1.write(0,4, 'Saved')
        sheet1.write(0,5, 'Discount')
        sheet1.write(0,6, 'Link')
        workbook.save(self.filename)

    def writeExcel(self, data):
        rexcel = xlrd.open_workbook(self.filename)
        rows = rexcel.sheets()[0].nrows
        excel = copy(rexcel)
        table = excel.get_sheet(0)
        while len(data) > 0:
            writeContent = data[0]
            for column in range(0,7):
                table.write(rows,column,writeContent[column])
            rows += 1
            del data[0]
        excel.save(self.filename)


class RalphLauren:

    def __init__(self):
        self.url = "https://www.ralphlauren.com/kids?prefn1=SaleFlag&srule=top-sellers&sz=60&start=0&prefv1=Sale"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        self.headers = {"user-agent": self.user_agent}
        self.productData = []
        self.excelFileName = "D:\\tmp\\ralphlauren.xls"


    def startRead(self):
        startPos = 0
        itemNumber = 1

        excelWriter = ExcelUtils("D:\\tmp\\test.xls")
        excelWriter.createExcel()

        while itemNumber > 0:
            self.url = "https://www.ralphlauren.com/kids?prefn1=SaleFlag&srule=top-sellers&sz=60&start=%d&prefv1=Sale" % (startPos)
            pageData = self.loadPage(self.url)
            productList = self.getProductItem(pageData)
            if productList:
                itemNumber = len(productList)
            else:
                break
            for product in productList:
                productInfo = self.getProductInfo(product)
                if productInfo is None:
                    continue
                self.productData.append(productInfo)
            excelWriter.writeExcel(self.productData)
            startPos += itemNumber





    def loadPage(self, pageURL):
        request = urllib2.Request(pageURL, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    def getProductItem(self, pageData):
        pattern = re.compile('<li class="grid.*?>(.*?)</div>\n</li>', re.S)
        return re.findall(pattern,pageData)

    def getProductInfo(self, product):
        product_info = {}
        info_pattern_dict = {"StandardPrice": '<span class="product-standard.*?(\d+\.\d{2}?)</s',
                             "SalePrice": '<span class="product-sales.*?(\d+\.\d{2}?)</s',
                             "ProductName": '"product-n.*?>\n<a.*?>(.*?)</a>',
                             "ProductLink": '"product-n.*?href="(.*?)"',
                             "BrandName": '"brand-name">(.*?)</d'}
        standardPrice = self.getInfo(product,info_pattern_dict['StandardPrice'])
        if not standardPrice:
            return None
        salePrice = self.getInfo(product,info_pattern_dict['SalePrice'])
        productName = self.getInfo(product,info_pattern_dict['ProductName']).strip()
        productLink = "https://www.ralphlauren.com/" + self.getInfo(product, info_pattern_dict['ProductLink'])
        brandName = self.getInfo(product, info_pattern_dict['BrandName']).strip()
        saveInfo = self.calculateDiscount(standardPrice,salePrice)
        product_info = {0: brandName,
                        1: productName,
                        2: standardPrice,
                        3: salePrice,
                        4: saveInfo[0],
                        5: saveInfo[1],
                        6: productLink}
        return product_info

    def getInfo(self, product, patternStr):
        pattern = re.compile(patternStr, re.S)
        match = re.search(pattern,product)
        if match:
            return match.group(1)
        return None

    def calculateDiscount(self, standardPrice, salePrice):
        f_standardprice = float(standardPrice)
        f_saleprice = float(salePrice)
        priceSave = float(f_standardprice - f_saleprice)
        discount = round(priceSave / f_standardprice,2)
        result = [priceSave, discount]
        return  result



pageReader = RalphLauren()
pageReader.startRead()
