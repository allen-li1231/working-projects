"""
@Author: Allen Lee       2018-02-27
"""
import xlwings as xw
from offline_weekly_report import data_clean as dc
from compile.my_class import MyDate, MyPath
import pandas as pd
import os
import win32api


dc._set_path_param('E:\Trustsaving\Python\offline_weekly_report')
def data_timeRange(drop_zero=True):
    raw_data = dc.clean_raw_data(dc.raw_path, dc.u_path, dc.paper_contract_path)
    sorted_data = pd.to_datetime(raw_data.loc[:, '申请时间']).sort_values()
    mintime, maxtime = sorted_data.head(1).values[0], sorted_data.tail(1).values[0]
    if drop_zero:
        mindate = str(mintime)[:4] + '/' + \
                  str(int(str(mintime)[5:7])) + '/' +\
                  str(int(str(mintime)[8:10]))
        maxdate = str(maxtime)[:4] + '/' + \
                  str(int(str(maxtime)[5:7])) + '/' +\
                  str(int(str(maxtime)[8:10]))
        return mindate, maxdate
    else:
        mindate = pd.datetime.strptime(str(mintime)[:10], '%Y-%m-%d')
        maxdate = pd.datetime.strptime(str(maxtime)[:10], '%Y-%m-%d')
        return mindate.strftime('%Y/%m/%d'), maxdate.strftime('%Y/%m/%d')


def xl_workdays(sheet, workday_pos):
    mydate = MyDate()
    last_saved = mydate.last_saved
    workday, totalworkdays = mydate.workdays_of_month(last_saved)

    sht = xw.Book.caller().sheets[sheet]
    sht.range(workday_pos).value = workday


def xl_totalworkday(sheet, position):
    mydate = MyDate()
    last_saved = mydate.last_saved
    workday, totalworkdays = mydate.workdays_of_month(last_saved)
    sht = xw.Book.caller().sheets[sheet]
    sht.range(position).value = totalworkdays


def xl_workdayremain(sheet, position):
    mydate = MyDate()
    last_saved = mydate.last_saved
    workday, totalworkdays = mydate.workdays_of_month(last_saved)
    remainworkday = totalworkdays - workday
    sht = xw.Book.caller().sheets[sheet]
    sht.range(position).value = remainworkday


def xl_clean_data_paste(sheet, startrow):
    sht = xw.Book.caller().sheets[sheet]
    data = dc.data_to_paste(dc.raw_path, dc.u_path, dc.paper_contract_path).values
    sht.range('A'+str(startrow)).value = data


def xl_SH_data():
    data = dc.data_to_paste(dc.raw_path, dc.u_path, dc.paper_contract_path)
    SH_data = data[data.城市 == "上海市"]
    return SH_data.values


def xl_NJ_data():
    data = dc.data_to_paste(dc.raw_path, dc.u_path, dc.paper_contract_path)
    NJ_data = data[data.城市 == "南京市"]
    return NJ_data.values


def xl_datarange(mindate_position, maxdate_position, sheet=0):
    sht = xw.Book.caller().sheets[sheet]
    mindate, maxdate = data_timeRange()
    sht.range(mindate_position).value = mindate
    sht.range(maxdate_position).value = maxdate

# xw.Book('E:\Trustsaving\Python\offline_weekly_report\汇总表及划扣明细.xlsm').set_mock_caller()
# sheet='日报明细'
# datePosition='v1'
def xl_dateRange_in_filename(sheet=None, datePosition=None):
    mindate, maxdate = data_timeRange()

    if sheet and datePosition:
        sht = xw.Book.caller().sheets[sheet]
        if mindate == maxdate:
            sht.range(datePosition).value = maxdate[5:].replace('/', '.')
        else:
            dateRng = mindate[5:] + "-" + maxdate[5:]
            sht.range(datePosition).value = dateRng.replace('/', '.')
    else:
        if mindate == maxdate:
            return maxdate[5:].replace('/', '.')
        else:
            dateRng = mindate[5:] + "-" + maxdate[5:]
            return dateRng.replace('/', '.')


# 追加
def xl_append_data(data_to_append, target_excel=None, sheetname=None):
    if not target_excel:
        try:
            wb_target = xw.Book.caller()
            sht_target = wb_target.sheets[sheetname]
        except:
            print("couldn't find target excel, please set target excel path.")
            return -1
    else:
        wb_target = xw.Book(target_excel)
        sht_target = wb_target.sheets(sheetname)

    nrow = sht_target.range("A1048576").end(3).row
    # nrow2 = sht_target.api.UsedRange.Rows.count
    # if nrow2 > nrow1 and nrow2 != 1048576:
    #    nrow = nrow2
    # else:E:\Trustsaving\Python\compile\profile.txt
    #    nrow = nrow1

    print('Rows count: %d' % nrow)
    startrange = sht_target.range('A' + str(nrow + 1))
    if callable(data_to_append):
        try:
            # xw.range
            startrange.value = data_to_append.value
            return 0
        except AttributeError:
            try:
                # pd.DataFrame
                startrange.value = data_to_append.values
                return 0
            except:
                print('Warning: data not understood.')
                return -1
        finally:
            wb_target.save()
            wb_target.close()
    else:
        try:
            startrange.value = data_to_append
            return 0
        except:
            print('Warning: data not understood.')
            return -1
        finally:
            wb_target.save()
            wb_target.close()


# 覆盖
def xl_override_data(data_to_override, target_excel=None, sheetname=None, startrow=0, startcol=0):
    if not target_excel:
        try:
            wb_target = xw.Book.caller()
            sht_target = wb_target.sheets[sheetname]
        except:
            print("couldn't find excel available, please set target excel path.")
            return -1
    else:
        wb_target = xw.Book(target_excel)
        sht_target = wb_target.sheets(sheetname)

    sht_target.clear_contents()
    startrange = sht_target.range(cell1=(1, 1), cell2=(startrow+1, startcol+1))
    if callable(data_to_override):
        try:
            startrange.value = data_to_override.value
            return 0
        except AttributeError:
            try:
                startrange.value = data_to_override.values
            except:
                print('Warning: data not understood.')
                return -1
        finally:
            wb_target.save()
            wb_target.close()
    else:
        try:
            startrange.value = data_to_override
            return 0
        except:
            print('Warning: data not understood.')
            return -1
        finally:
            wb_target.save()
            wb_target.close()


# 另存为：
def xl_save_as(template_path, sheetname, data, save_as):
    wb_template = xw.Book(template_path)
    sht_template = wb_template.sheets(sheetname)

    sht_template.range('A1').value = list(data.columns)
    sht_template.range('A2').value = data.values

    xw.Book(template_path).save(save_as)
    xw.Book(save_as).close()


def xl_area_performance_output(template_path=None):
    my_tool = MyDate()
    yesterday = my_tool.yesterday
    last_saved = my_tool.last_saved
    dirpath = MyPath().scriptpath

    if not template_path:
        template_path = dirpath+r'\area_template.xls'
    else:
        dirpath = os.path.split(template_path)[0]
    SH_data, NJ_data = dc.area_performance(dc.raw_path)
    SH_data = SH_data.astype('str')
    NJ_data = NJ_data.astype('str')

    if yesterday == last_saved:
        xl_save_as(template_path=template_path, sheetname='销售人员统计明细报表', data=SH_data,
                   save_as=r'%s\output\线上业绩-%s上海.xls' % (dirpath, yesterday[5:7] + yesterday[8:]))
        xl_save_as(template_path=template_path, sheetname='销售人员统计明细报表', data=NJ_data,
                   save_as=r'%s\output\线上业绩-%s江苏.xls' % (dirpath, yesterday[5:7] + yesterday[8:]))
    else:
        xl_save_as(template_path=template_path, sheetname='销售人员统计明细报表', data=SH_data,
                   save_as=r'%s\output\线上业绩-%s-%s上海.xls'
                           % (dirpath, last_saved[5:7] + last_saved[8:], yesterday[5:7] + yesterday[8:]))
        xl_save_as(template_path=template_path, sheetname='销售人员统计明细报表', data=NJ_data,
                   save_as=r'%s\output\线上业绩-%s-%s江苏.xls'
                           % (dirpath, last_saved[5:7] + last_saved[8:], yesterday[5:7] + yesterday[8:]))


def xl_trace_performance_output(template_path=None):
    """target_excel{template sheetname: {'data': data, 'path': target excel path, 'sheet': target sheetname}}"""
    scriptpath = MyPath(True).scriptpath
    daterng = xl_dateRange_in_filename()
    if not template_path:
        template_path = scriptpath + r'\output\全国理财报表-'+daterng+'.xlsx'

    target_excel = {'上海日报': {'data': xl_SH_data(), 'path': scriptpath+r'\(操作)每日团队业绩追踪表上海.xlsx', 'sheet': '业绩-SH'},
                    '江苏日报': {'data': xl_NJ_data(), 'path': scriptpath+r'\(操作)每日团队业绩追踪表江苏.xlsx', 'sheet': '业绩-JS'}}

    for idx in target_excel:
        try:
            overrider = xw.Book.caller()
        except:
            overrider = xw.Book(template_path)

        overrider.app.display_alerts = False
        overrider.app.screen_updating = False
        overrider.app.calculation = 'manual'

        shtname = target_excel[idx]['sheet']
        shtpath = target_excel[idx]['path']

        sht = overrider.sheets(shtname)
        nrow = sht.api.UsedRange.Rows.count
        ncol = sht.api.UsedRange.Columns.count
        override_rng = sht.range(cell1=(1, 1), cell2=(nrow, ncol))

        # override nation table to trace table
        xl_override_data(override_rng, shtpath, idx)

        # append performance data to trace table
        xl_append_data(target_excel[idx]['data'], shtpath, '划扣日报')

        # extend formula columns to fit new data
        performance_sht = xw.Book(shtpath).sheets('划扣日报')
        for dcol in ['U', 'V']:
            formula = performance_sht.range('%s2' % dcol).formula
            drow = performance_sht.range('A1').expand('down').rows.count
            performance_sht.range('%s2:%s%d' % (dcol, dcol, drow)).value = formula

        # save and clear statistics that set up for double checking
        daterange = xl_dateRange_in_filename()
        savepath = scriptpath + r'\output\每日团队业绩追踪表-%s' % daterange + shtpath[-7:]
        xw.Book(shtpath).save(savepath)
        xw.Book(savepath).sheets[0].range('O18:Q27').clear_contents()

        overrider.app.screen_updating = True
        overrider.app.display_alerts = True

        for sheet in xw.Book(savepath).sheets:
            try:
                sheet.api.UsedRange.value = sheet.api.UsedRange.value
            except :
                e_msg = win32api.FormatMessage(-2147352566)
                print("Error occured in %s: %s" % (sheet.name, e_msg))
        xw.Book(savepath).save()
        xw.Book(savepath).close()


if __name__ == '__main__':
    scriptpath = MyPath(True).scriptpath
    print(r"output path: %s\output" % scriptpath)

    xl_area_performance_output()
    xl_trace_performance_output()
