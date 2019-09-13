"""
@Author: Allen Lee       2018-03-20
"""
from compile.my_class import MyMail, MyPath, MyDate
from offline_weekly_report import VBATool
import pandas as pd
import os
import base64
# TODO: Boss Yang's mailbox can't read text body, find out the reason!


def nation_main():
    date = VBATool.xl_dateRange_in_filename()
    nation_name = "全国理财报表-"+date+".xlsx"

    mindate, maxdate = VBATool.data_timeRange(drop_zero=False)
    zmindate, zmaxdate = VBATool.data_timeRange(drop_zero=True)

    mydate = MyDate()
    workday, totalworkday = mydate.workdays_of_month(maxdate.replace('/', '-'))
    time_proc = workday/totalworkday*100

    path = MyPath().scriptpath

    att_path = path+'\\output\\'+nation_name
    receiver, ccreceiver = ['lizhonghao@trustsaving.com'], []
    #receiver = ['jiangmingjie@trustsaving.com', 'yangruijun@trustsaving.com', 'renzhuxin@trustsaving.com']
    #ccreceiver = ['yanzhenzhen@trustsaving.com', 'linbinhua@trustsaving.com', 'lizhonghao@trustsaving.com']

    parse1 = pd.read_excel(path+"\汇总表及划扣明细.xlsm", sheetname='日报数据1', index_col='营业部')
    p1_new_invest = parse1.loc['全国总计', '绩效业绩']
    p1_reinvest = parse1.loc['全国总计', 'Unnamed: 3']
    p1_perf = parse1.loc['全国总计', 'Unnamed: 4']
    p1_arrival = parse1.loc['全国总计', '到账业绩']

    parse2 = pd.read_excel(path+"\汇总表及划扣明细.xlsm", sheetname='日报数据2', index_col='营业部')
    p2_new_invest = float(parse2.loc['全国总计', '绩效业绩'])
    p2_reinvest = float(parse2.loc['全国总计', 'Unnamed: 3'])
    p2_perf = float(parse2.loc['全国总计', 'Unnamed: 4'])
    p2_arrival = float(parse2.loc['全国总计', '到账业绩'])
    achieve_rate = parse2.loc['全国总计', '达成率']

    text1 = """<html>    <p><span lang=3D"EN-US" style="font-size: 16px; font-family: 'Microsoft YaHei UI', Tahoma;">
    各位领导好：<br/><br/>
    截至<strong>%s</strong>时间进度为<strong>%.1f</strong>%%，绩效业绩进度为<strong>%s</strong>；<br/><br/>
    <strong>%s</strong>：<strong>绩效业绩</strong>为<strong>%.1f万：</strong>新投资<strong>%.1f万</strong>，再投资<strong>%.1f万</strong>；<strong>到账业绩</strong>为<strong>%.1f万</strong>；<br/><br/>
    <strong>%s月总计</strong>：<strong>绩效业绩</strong>为<strong>%.1f万：</strong>新投资<strong>%.1f万</strong>，再投资<strong>%.1f万</strong>；<strong>到账业绩</strong>为<strong>%.1f万</strong>；
    </span></p>

    <p>
    <span lang=3D"EN-US" style="background:yellow; font-size: 18px;"><strong>%s：</strong></span>
    </p></html>
    """ % (zmaxdate.replace('/', '.'), time_proc, achieve_rate,
           date, p1_perf, p1_new_invest, p1_reinvest, p1_arrival,
           int(maxdate[5:7]), p2_perf, p2_new_invest, p2_reinvest, p2_arrival,
           date)

    text2 = """<html><p>
    <span lang=3D"EN-US" style="background:yellow; font-size: 17px;"><strong>%s月累计：</strong></span>
    </p>
    </html>""" % int(maxdate[5:7])

    msg = MyMail(receiver=receiver, cc=ccreceiver, subject=os.path.splitext(nation_name)[0])

    msg.set_html_format_table(path+r'\mail\日报数据1.htm')
    msg.set_table_data(path+r'\汇总表及划扣明细.xlsm', sheetname='日报数据1', float_decimal=1)
    tb1 = msg.add_html_table(inplace=False)

    msg.set_html_format_table(path+r'\mail\日报数据2.htm')
    msg.set_table_data(path+r'\汇总表及划扣明细.xlsm', sheetname='日报数据2', float_decimal=1)
    tb2 = msg.add_html_table(inplace=False)

    pic_path = path+r'\mail\signature.png'
    f = open(pic_path, 'rb')
    img64 = base64.encodebytes(f.read()).decode()
    f.close()
    suffix = pic_path.split('.')[-1]
    img = '''<hr /><p>
    <img src="data:image/%s;base64,%s" width="370" height="130">
    </p>'''\
           % (suffix, img64)

    msg.add_plain_text(text1+tb1+text2+tb2)
    # msg.add_attach(att_path)
    # msg.add_sig_to_text(path+r'\mail\signature.png')
    msg.send()


if __name__ == '__main__':
    nation_main()
    print('E-mail sent successfully!')