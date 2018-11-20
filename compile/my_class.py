"""
@Author: Allen Lee       2018-02-12
"""
import sys
import os
import re
import time
import xlrd
import datetime
from calendar import monthrange
import smtplib
import base64
from email.utils import formataddr
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pandas import DataFrame, date_range, merge, read_excel, to_datetime, datetime as pdatetime


def sql_connection(DB='trustsaving_web'):
    import pymysql
    try:
        conn = pymysql.connect(host='rr-bp1l8v780l24ndjobo.mysql.rds.aliyuncs.com', user='youqian_read',
                               password='rr6NyP!uB8zJ', port=3306,
                               database=DB, charset='utf8')
        cur = conn.cursor()
        return cur
    except:
        print("Please check your network environment.")
        sys.exit()


def to_timeseries(start_date, end_date, *dataframes):
    timeSeries = date_range(start_date, end_date, freq='D')
    data = DataFrame(timeSeries, columns=['date'])
    for frame in dataframes:
        try:
            frame = frame.astype('float64')
            if frame.shape[0] != 0:
                # datetime series is in index, strech datetime out of index:
                frame = frame.reset_index()
        except:
            # if not:
            frame.iloc[:, 1:] = frame.iloc[:, 1:].astype('float64')
        # now that frame.date is available:
        try:
            frame.date = frame.date.astype('datetime64[ns]')
        except:
            print('Warning: date column type mismatch.')
        data = merge(data, frame, how='left', on='date')
    data = data.fillna(0)
    return data


def intro_data(filename, sheet, skiprow=0, header=0):
    while not os.path.isfile(filename):
        filename = input('Raw data path incorrect, path given:\n%s\nPlease try again:\n'
                         % filename)
    suffix = os.path.splitext(filename)[1]
    if suffix in ['.xls', '.xlsx', '.xlsm']:
        data = read_excel(filename, sheet, skiprows=skiprow, header=header)
    elif suffix == '.csv':
        from pandas import read_csv
        data = read_csv(filename, skiprows=skiprow, header=header)
    # Hence, data is Dataframe structured
    return data


class MyPath:
    # dirpath is where this script locates:
    dirpath = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, script_path=False):
        # get output path, scriptpath is the path where .py running locates:
        if 'PyCharm' in sys.argv[0] or sys.argv[0] == '':
            file = open(MyPath.dirpath+'\profile.txt', 'r')
            file.readline()
            self.scriptpath = file.readline().strip()
            file.close()
        else:
            self.scriptpath = os.path.dirname(sys.argv[0])
        try:
            # check whether sys.argv[1] is available:
            self.path = sys.argv[1]
            try:
                # if opened by pycharm, reset default path:
                int(self.path)
                self.path = MyPath.dirpath
            except ValueError:
                # make sure that self.path physically exists:
                try:
                    os.mkdir(self.path)
                except FileExistsError:
                    pass
        except IndexError:
            pass

    def to_csv(self, filename, data, columns=list()):
        try:
            open(r'%s\%s.csv' % (self.path, filename), 'w')
        except FileNotFoundError:
            try:
                os.makedirs(r"%s" % self.path)
            except FileExistsError:
                pass
        file = open(r'%s\%s.csv' % (self.path, filename), 'w')
        file.write(','.join(columns) + '\n')
        for i in data:
            i = [str(x) for x in i]
            file.write(','.join(i) + '\n')
        file.close()


class MyDate:
    last_saved = str()
    day_after_last_saved = str()
    this_month_floor = str()
    this_month_ceil = str()
    to_the_beginning = '2000-01-01'

    def __init__(self, refresh=True):
        # datetime to use afterwards:
        now = datetime.datetime.now()
        self.curdate = now.strftime('%Y-%m-%d')
        self.yesterday = now - datetime.timedelta(days=1)
        self.yesterday = self.yesterday.strftime('%Y-%m-%d')

        # datetime below is based on today:
        today = datetime.date.today()
        last_month_date = today - datetime.timedelta(days=monthrange(today.year, today.month)[1])
        self.last_month_floor = datetime.date.replace(last_month_date, day=1)
        self.last_month_ceil = self.last_month_floor + \
                               datetime.timedelta(days=monthrange(self.last_month_floor.year,
                                                                  self.last_month_floor.month)[1] - 1)
        self.dirpath = MyPath().dirpath
        self._reload_time(refresh)

    def _init_profile(self):
        # initializing profile.txt, make sure profile exists first:d
        try:
            open(r"%s\profile.txt" % self.dirpath, 'r', encoding="utf8")
        except FileNotFoundError:
            print('profile not found, making new profile in %s' % self.dirpath)
            # set yesterday and today as default:
            profile = open(r"%s\profile.txt" % self.dirpath, 'w', encoding="utf8")
            profile.write('0,%s,%s' % (self.yesterday, self.curdate))
            profile.close()

        profile_info, usr_path = self.read_profile()
        freq = int(profile_info[0])

        if self.curdate == profile_info[2]:
            freq += 1
        else:
            profile_info[1] = profile_info[2]
            profile_info[2] = self.curdate
            freq = 0
        profile = open(r"%s\profile.txt" % self.dirpath, 'w', encoding="utf8")
        profile.writelines("%d,%s,%s\n" % (freq, profile_info[1], profile_info[2]))
        profile.writelines(usr_path)
        profile.close()

    def read_profile(self, reload_profile=False):
        if reload_profile:
            self._init_profile()
        profile = open(r"%s\profile.txt" % self.dirpath, 'r', encoding="utf8")
        # modify static values in main class
        profile_info = profile.readline().strip().split(',')
        usr_path = profile.readline().strip()
        profile.close()
        return profile_info, usr_path

    def _reload_time(self, reload_profile=True):
        # datetime below is based on profile.txt:
        if reload_profile:
            self._init_profile()
        profile_info, usr_path = self.read_profile()
        MyDate.last_saved = profile_info[1]
        MyDate.day_after_last_saved = datetime.datetime.strptime(MyDate.last_saved, '%Y-%m-%d')
        MyDate.day_after_last_saved = MyDate.day_after_last_saved + datetime.timedelta(days=1)
        MyDate.day_after_last_saved = MyDate.day_after_last_saved.strftime('%Y-%m-%d')
        MyDate.this_month_floor = profile_info[2][:8] + '01'
        this_month = datetime.datetime.strptime(MyDate.this_month_floor, '%Y-%m-%d')
        monthdays = datetime.timedelta(days=monthrange(this_month.year, this_month.month)[1]-1)
        MyDate.this_month_ceil = (this_month + monthdays).strftime('%Y-%m-%d')
        MyDate.to_the_beginning = '2000-01-01'

    def monthrange(self, date_parse):
        month = datetime.datetime.strptime(date_parse, '%Y-%m-%d')
        monthdays = datetime.timedelta(days=monthrange(month.year, month.month)[1]-1)
        return monthdays

    def eomonth(self, date_parse):
        date_parse = date_parse[:8] + '01'
        month = datetime.datetime.strptime(date_parse, '%Y-%m-%d')
        monthdays = datetime.timedelta(days=monthrange(month.year, month.month)[1]-1)
        month_ceil = (month + monthdays).strftime('%Y-%m-%d')
        return month_ceil

    def workdays_of_month(self, date_parse):
        from compile.my_crawler import DateArangeCrawler
        month_floor = date_parse[:8] + '01'
        month_ceil = self.eomonth(date_parse)
        wdata = DateArangeCrawler(month_floor, date_parse)
        workday = wdata.workday
        tdata = DateArangeCrawler(month_floor, month_ceil)
        totalworkdays = tdata.workday
        return workday, totalworkdays

    def workday_calendar(self, start_date, end_date, due=0):
        from compile.my_crawler import DateArangeCrawler
        # end_date = start_date[:-5]+'12-31'
        datelst = date_range(start_date, end_date).strftime('%Y-%m-%d')
        Tday = []
        for day in datelst:
            crawler = DateArangeCrawler(start_date=day, due=due)
            Tday.append(crawler.calendar)
            time.sleep(0.1)
        Tframe = DataFrame(Tday, index=datelst, columns=['T+'+str(due)])
        return Tframe


class MyMail:
    def __init__(self, account=None, password=None, server=None, port=25, receiver=None, cc=None, subject=None, charset='utf-8'):
        if not account:
            self.account = 'lizhonghao@trustsaving.com'
        else:
            self.account = account
        if not password:
            self.passwd = 'chuxin123456'
        else:
            self.passwd = password
        if not server:
            self.server = 'mail.trustsaving.com'
        else:
            self.server = server
        if receiver:
            if not isinstance(receiver, list):
                self.receiver = [receiver, ]
            else:
                self.receiver = receiver
        else:
            self.receiver = [self.account, ]

        self.cc = cc
        if not isinstance(cc, list) and cc:
            self.cc = [cc, ]

        self.charset = charset
        self.table_data = None
        self.html_format_table = None
        self.subject = subject
        self.port = port

        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr(['李中豪', self.account])
        VTo = []
        for addr in self.receiver:
            VTo.append(formataddr([addr, addr]))
        msg['To'] = ','.join(VTo)
        msg['Subject'] = subject
        if cc:
            VCc = []
            for addr in self.cc:
                VCc.append(formataddr([addr, addr]))
            msg['Cc'] = ','.join(VCc)
        self.message = msg

    def simple_mail(self, text):
        msg = MIMEText(text, _charset=self.charset)
        msg['From'] = formataddr(['Allen Lee', self.account])
        VTo = []
        for addr in self.receiver:
            VTo.append(formataddr([addr, addr]))
        msg['To'] = ','.join(VTo)
        msg['Subject'] = self.subject
        if not self.cc:
            VCc = []
            for addr in self.cc:
                VCc.append(formataddr([addr, addr]))
            msg['Cc'] = ','.join(VCc)
        self.message = msg

    def add_attach(self, file_path, _encode='gb2312'):
        # 附件：
        att = MIMEApplication(open(file_path, 'rb').read())
        file_name = os.path.basename(file_path)
        file_name64 = base64.encodebytes(file_name.encode(_encode)).decode(_encode)
        file_name64 = file_name64.replace('\n', '')
        att.add_header('Content-Disposition', 'attachment; filename="=?'+_encode+'?B?'+file_name64+'?="')
        self.message.attach(att)

    def add_pic(self, pic_path):
        f = open(pic_path, 'rb')
        pic = MIMEImage(f.read())
        f.close()
        # 加上必要的头信息:
        filename = os.path.split(pic_path)[-1]
        pic.add_header('Content-Disposition', 'attachment', filename=(self.charset, '', filename))
        pic.add_header('Content-ID', '<%s>' % filename)
        pic.add_header('X-Attachment-Id', '%s' % filename)
        pic.set_charset(self.charset)
        self.message.attach(pic)

    def add_sig_to_text(self, pic_path):
        f = open(pic_path, 'rb')
        img64 = base64.encodebytes(f.read()).decode()
        f.close()
        suffix = pic_path.split('.')[-1]
        body = '''<html><body><p>
        <img src="data:image/%s;base64,%s" width="370" height="130"/>
        </p></body></html>'''\
               % (suffix, img64)
        pic_text = MIMEText(body, 'html', self.charset)
        self.message.attach(pic_text)

    def add_plain_text(self, text):
        self.message.attach(MIMEText(text, 'html', self.charset))

    def set_table_data(self, table_path=None, sheetname='Sheet1', float_decimal=2):
        while not os.path.isfile(table_path):
            table_path = input('Please set a reachable table path:\n')
        wb = xlrd.open_workbook(table_path)
        if isinstance(sheetname, str):
            sht = wb.sheet_by_name(sheetname)
        else:
            sht = wb.sheet_by_index(sheetname)

        nrow = sht.nrows
        vol = []
        for row in range(nrow):
            rowval = sht.row_values(row)
            for cell in rowval[:]:
                if cell == '':
                    rowval.remove(cell)
            vol += rowval

        for i, data in enumerate(vol):
            try:
                vol[i] = round(data, float_decimal)
            except:
                pass
        self.table_data = tuple(vol)

    def set_html_format_table(self, html_file_path):
        html_file = open(html_file_path, 'r', encoding=self.charset)
        text = html_file.read()
        html_file.close()
        html_text = re.sub('%', '%%', text)
        html_text = re.sub('>.+?</td>', '>%s</td>', html_text)
        html_text = re.sub('<div.*?align=.*?>', '<div align=left>', html_text)
        self.html_format_table = html_text

    def add_html_table(self, inplace=True):
        if inplace:
            if self.html_format_table and self.table_data:
                self.message.attach(MIMEText(self.html_format_table % self.table_data, 'html', self.charset))
            else:
                print("Please set html format table and table data first.")
        else:
            return self.html_format_table % self.table_data

    def send(self):
        try:
            smtpObj = smtplib.SMTP(host=self.server, port=self.port)
            smtpObj.login(self.account, self.passwd)
            if self.cc:
                smtpObj.sendmail(self.account, self.receiver+self.cc, self.message.as_string())
            else:
                smtpObj.sendmail(self.account, self.receiver, self.message.as_string())
        except smtplib.SMTPRecipientsRefused:
            print('Error: Recipient refused.')
        except smtplib.SMTPAuthenticationError:
            print('Error: Authentication error.')
        except smtplib.SMTPSenderRefused:
            print('Error: Sender refused.')
        except smtplib.SMTPException:
            print("Error: unable to send e-mail.")


def data_timeRange(filename, sheet=0, skiprow=0, date_range_column='date', drop_zero=True):
    raw_data = read_excel(filename=filename,
                          sheet=sheet,
                          skiprow=skiprow)
    sorted_data = to_datetime(raw_data.loc[:, date_range_column]).sort_values()
    mintime, maxtime = sorted_data.head(1).values[0], sorted_data.tail(1).values[0]
    if drop_zero:
        mindate = str(mintime)[:4] + '/' + \
                  str(int(str(mintime)[5:7])) + '/' + \
                  str(int(str(mintime)[8:10]))
        maxdate = str(maxtime)[:4] + '/' + \
                  str(int(str(maxtime)[5:7])) + '/' + \
                  str(int(str(maxtime)[8:10]))
        return mindate, maxdate
    else:
        mindate = pdatetime.strptime(str(mintime)[:10], '%Y-%m-%d')
        maxdate = pdatetime.strptime(str(maxtime)[:10], '%Y-%m-%d')
        return mindate.strftime('%Y/%m/%d'), maxdate.strftime('%Y/%m/%d')


if __name__ == '__main__':
    print('path: '+MyPath().path)
    print('dirpath: '+MyPath().dirpath)
    print('script path: '+MyPath().scriptpath)

