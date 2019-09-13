# -*- coding: utf-8 -*-
import urllib2, urllib, re, cookielib


class ElectSysSpider:
    def __init__(self, url):
        self.url = url
        self.txtUserName = "xxxxxxxx"
        self.txtPwd = "xxxxxxxx"
        self.rbtnLst = "1"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36",
                        "Referer": "http://electsys.sjtu.edu.cn/edu/",
                        "Origin": "http://electsys.sjtu.edu.cn"}
        self.cookie = cookielib.CookieJar()
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)

    def getRaw(self):
        opener = urllib2.build_opener(self.cookie_handler)
        req = urllib2.Request(self.url)
        res = opener.open(req)
        return res.read()
    raw = getRaw()
    def getVIEWSTATE(self, raw):
        pattern = re.compile('id="__VIEWSTATE" value="(.*?)"', re.S)
        content = pattern.search(raw)
        # print "VIEWSTATE: " + content.group(1) + '\n'
        return content.group(1)

    def getVIEWSTATEGENERATOR(self, raw):
        pattern = re.compile('id="__VIEWSTATEGENERATOR" value="(.*?)"', re.S)
        content = pattern.search(raw)
        # print "VIEWSTATEGENERATOR: " + content.group(1) + '\n'
        return content.group(1)

    def getEVENTVALIDATION(self, raw):
        pattern = re.compile('id="__EVENTVALIDATION" value="(.*?)"', re.S)
        content = pattern.search(raw)
        # print "EVENTVALIDATION: " + content.group(1) + '\n'
        return content.group(1)

    def getData(self):
        value = {"__VIEWSTATE": self.getVIEWSTATE(self.getRaw()),
                 "__VIEWSTATEGENERATOR": self.getVIEWSTATEGENERATOR(self.getRaw()),
                 "__EVENTVALIDATION": self.getEVENTVALIDATION(self.getRaw()),
                 "txtUserName": self.txtUserName, "txtPwd": self.txtPwd, "rbtnLst": self.rbtnLst,
                 # In Python, Chinese strings should be acclaimed as unicode,
                 # then transferred into gb2312/gbk, etc..
                 "Button1": u"登陆".encode("gb2312")}
        data = urllib.urlencode(value)
        return data

    def virtualLogin(self):
        opener = urllib2.build_opener(self.cookie_handler)
        req = urllib2.Request(self.url, self.getData(), self.headers)
        res = opener.open(req)
        # print res.read()

    def getHomePage(self):
        curl = "http://electsys.sjtu.edu.cn/edu/newsboard/newsinside.aspx"
        opener = urllib2.build_opener(self.cookie_handler)
        req = urllib2.Request(curl)
        res = opener.open(req)
        # print res.read()
        return res.read()

    def wrtClass(self):
        fileName = "Class.txt"
        f = file("E:\PyDoc\SpiderTest\SJTUElectSysTest\\" + fileName, "a")
        page = self.getHomePage()
        print(page)
        pattern = re.compile('<tr class="tdcolour.">\s+<td>(\S+?)\s+</td><td>(\S+?)\s+</td><td class="en" align="center">(.*?)</td><td align="center">', re.S)
        items = pattern.findall(page)
        f.write("This is the class list for this semester: " + "\n")
        format = "%-25s, %-25s, %-25s"
        f.write(format % ("ID", "NAME", "CREDIT") + "\n")
        for item in items:
            f.write(format % item + "\n")
        f.close()

if __name__ == '__main__':
    elsSpider = ElectSysSpider("http://electsys.sjtu.edu.cn/edu/index.aspx")
    elsSpider.virtualLogin()
    elsSpider.wrtClass()