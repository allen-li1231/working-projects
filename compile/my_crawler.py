"""
@Author: Allen Lee       2018-03-28
"""
import requests
import re
from bs4 import BeautifulSoup as soup
import pylab
from PIL import Image
import pandas as pd
from compile.my_class import MyPath


class DateArangeCrawler:
    def __init__(self, start_date, end_date=None, due=0):
        self.count_url = 'http://www.fynas.com/workday/count'
        self.calendar_url = 'http://www.fynas.com/workday/end'
        self.header = {
            'Connection': 'keep-alive',
            'Content-Length': '41',
            'Accept': '*/*',
            'Origin': 'http://www.fynas.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like\
Gecko) Chrome/63.0.3239.132 Safari/537.36 OPR/50.0.2762.67',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://www.fynas.com/workday',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'Hm_lvt_0fa7b8c467469bd8f2eaddd5dc1d440d=1518338629,1518491507,1519357193;\
Hm_lpvt_0fa7b8c467469bd8f2eaddd5dc1d440d=1519363419'
        }
        self.payload = {'start_date': start_date, 'end_date': end_date}
        self.due = {'start_date': start_date, 'days': due+1}

    @property
    def calendar(self):
        try:
            content = requests.post(self.calendar_url, data=self.due, headers=self.header).text
            collect = eval(content)
            return collect['data']
        except:
            print("Warning: crawler function failed.")

    @property
    def _collection(self):
        try:
            content = requests.post(self.count_url, data=self.payload, headers=self.header).text
            collect = eval(content)
            return collect['data']
        except:
            print("Warning: crawler function failed.")

    @property
    def total(self):
        return self._collection['total']

    @property
    def weekend(self):
        '''
        Notes: weekend returned is based on calendar weekend, holiday shift excluded.
        '''
        return self._collection['weekend']

    @property
    def holiday(self):
        return self._collection['holiday']

    @property
    def holiday_shift(self):
        return self._collection['extra']

    @property
    def workday(self):
        return self._collection['workday']


class NewManageCrawler:
    def __init__(self, user='13671724254', password='chuxin123456', valid_code=None):
        self.user = user
        self.password = password
        self.validCode = valid_code
        if not isinstance(valid_code, str) and valid_code:
            try:
                self.validCode = str(valid_code)
            except:
                print('valid_code typeError: expect string or integer.')

        self.loginUrl = 'http://newmanage.chuxindai.com//user/login.do?loginName=%s&loginPwd=%s&validCode=%s'
        self.validCodeUrl = 'http://newmanage.chuxindai.com//user/getAdminPhoneVerifyCode.do?phone=%s' % user

        self.cookies = {
            'Host': 'newmanage.chuxindai.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 OPR/51.0.2830.55',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://newmanage.chuxindai.com/page/account/workBord.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
                        }
        self.ssn = requests.session()
        self.login()

    def login(self):
        if not self.validCode:
            self.ssn.post(self.validCodeUrl)
            self.validCode = input("Please set vaild code: \n")

        self.loginUrl = self.loginUrl % (self.user,
                                         self.password,
                                         self.validCode)
        self.ssn.get(url=self.loginUrl, cookies=self.cookies)

    def salesDetailExcel(self, start_date, end_date, output_filename=None, sales_mobile_no=None):
        if not output_filename:
            output_filename = MyPath().scriptpath+r'\excel.xls'
        uxls = 'http://newmanage.chuxindai.com/report/exportSalesStstisDetailExcel.do?salesRole=counselor&salesMobileNO=%s&startDate=%s&endDate=%s'
        responseXLS = self.ssn.get(url=uxls % (sales_mobile_no,
                                               start_date,
                                               end_date),
                                   stream=True)
        if isinstance(responseXLS.content, bytes):
            with open(output_filename, "wb") as file:
                file.write(responseXLS.content)
                file.close()
        else:
            return print('Failure occured, response content:\n%s' % responseXLS.content)

    def creditAssignment(self):
        ucal = 'http://newmanage.chuxindai.com//page/cgBidManager/cgTransferBidList.html'
        content = self.ssn.get(url=ucal).content


class nCoreCrawler:
    def __init__(self):
        self.loginUrl = 'http://ncore.trustsaving.com:8888/login'
        self.ssn = requests.session()
        self._login()

    def _login(self):
        payload = {'username': 'XY0104000103',
                   'password': '123456'}
        self.ssn.post(self.loginUrl, data=payload)

    def continueInvestReport(self, start_date, end_date, output_filename=None):
        if not output_filename:
            output_filename = MyPath().scriptpath+r'\OC.xls'
        ulst = 'http://ncore.trustsaving.com:8888/operation_manage/continueInvestReport/list'
        uexl = 'http://ncore.trustsaving.com:8888/serviceoperation/continueInvestReport/exportExcle'
        payload = {'startTime': start_date.replace('-', ''),
                   'endTime': end_date.replace('-', '')}

        print("This may take long due to your network.\npath: %s" % MyPath().scriptpath)
        self.ssn.post(ulst, payload)
        responseXLS = self.ssn.post(uexl)
        with open(output_filename, 'wb') as file:
            file.write(responseXLS.content)
            file.close()

    def paymentReport(self, start_date='2015-05-19', end_date='2017-07-31', output_filename=None):
        if not output_filename:
            output_filename = MyPath().scriptpath+r'\maturity.xls'
        ulst = 'http://ncore.trustsaving.com:8888/operation_manage/paymentReport/list'
        uexl = 'http://ncore.trustsaving.com:8888/serviceoperation/paymentReport/getPaymentReportsExcel'
        payload = {'startTime': start_date.replace('-', ''),
                   'endTime': end_date.replace('-', '')}

        print("This may take long due to your network.\npath: %s" % output_filename)
        stat = int()
        while stat != 200:
            stat = self.ssn.post(ulst, payload).status_code
            print(stat)

        payload = {'exportType': '4'}
        responseXLS = self.ssn.post(uexl, payload, stream=True)
        with open(output_filename, 'wb') as file:
            for chunk in responseXLS.iter_content(1024):
                file.write(chunk)
            file.close()

