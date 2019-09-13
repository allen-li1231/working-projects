"""
@Author: Allen Lee       2018-02-03
Better import this script as class
"""
import pandas as pd
from compile.my_crawler import NewManageCrawler
from compile.my_class import MyDate, MyPath, intro_data


def _set_path_param(work_path=None):
    global script_path
    if not work_path:
        script_path = MyPath().scriptpath
    else:
        script_path = work_path
    global raw_path
    raw_path = script_path + r'\excel.xls'
    global u_path
    u_path = script_path + r'\U_table.xlsx'
    global paper_contract_path
    paper_contract_path = script_path + r'\paper_contract.xls'

_set_path_param()


def download_raw_data(start_date=None, end_date=None, save_path=None):
    if start_date is None or end_date is None:
        dateclass = MyDate()
        start_date = dateclass.last_saved
        end_date = dateclass.yesterday

        confirm = input("Confirm:\t start date: %s, end date: %s\n[y]/n: " % (start_date, end_date))
        while confirm not in ['y', 'n', '']:
            confirm = input("[y]/n: ")
        if confirm != 'y' or '':
            start_date = input("Set start date: ")
            end_date = input("Set end date: ")

    if not save_path:
        save_path = raw_path
    req = NewManageCrawler()
    req.salesDetailExcel(start_date, end_date, save_path)


# TODO: complete performance of chuchuzhuan, yueyuejia:
def download_raw_data_eomonth(save_path):
    pass


def clean_raw_data(filename=raw_path, u_path=u_path, paper_contract_path=paper_contract_path,
                   sheet='销售人员统计明细报表', skiprow=1):
    raw_data = intro_data(filename, sheet, skiprow)
    raw_data.loc[:, '申请时间'] = raw_data.loc[:, '申请时间'].astype('datetime64[ns]')
    raw_data.loc[:, '申请时间'] = raw_data.loc[:, '申请时间'].apply(lambda x: x.strftime('%Y') + '/' +
                                                                   str(int(x.strftime('%m'))) + '/' +
                                                                   str(int(x.strftime('%d'))))
    raw_data.loc[:, '是否新投'] = raw_data.loc[:, '是否新投'].apply(lambda x: '新投资' if x == '是' else x)
    raw_data.loc[:, '是否新投'] = raw_data.loc[:, '是否新投'].apply(lambda x: '再投资' if x == '否' else x)

    def fake_counselor(data_row):
        if data_row.理财顾问 == '理财统计':
            return data_row.客户姓名
        else:
            return data_row.理财顾问

    raw_data.loc[:, '理财顾问'] = raw_data.apply(fake_counselor, axis=1)

    # Duplicated names should distinguish:
    raw_data.loc[:, '理财顾问'] = raw_data.loc[:, '理财顾问'].apply(lambda x: '王艳3' if x == '王艳' else x)
    raw_data.loc[:, '理财顾问'] = raw_data.loc[:, '理财顾问'].apply(lambda x: '张红2' if x == '张红' else x)
    raw_data.loc[:, '理财顾问'] = raw_data.loc[:, '理财顾问'].apply(lambda x: '赵鹏1' if x == '赵鹏' else x)
    raw_data = match_paper_contract(raw_data, paper_contract_path)
    raw_data = match_hierarchy(raw_data, u_path)

    raw_data.drop(['入职日期', '对应职级', '是否在职'], axis=1, inplace=True)
    return raw_data


def match_paper_contract(parse_data, contract_path=paper_contract_path):
    # find out investors that has already invested by paper contract:
    paper_contract = intro_data(contract_path, 'Sheet1', skiprow=2, header=None)

    paper_contract = paper_contract.iloc[:-1]

    def invest_status(data_row):
        if (data_row.loc['客户证件号'] in paper_contract.values) or (data_row.loc['投资产品'][2] == '赚'):
            return '再投资'
        else:
            return data_row.loc['是否新投']

    parse_data.loc[:, '是否新投'] = parse_data.apply(invest_status, axis=1)
    return parse_data


def match_hierarchy(parse_data, hierarchy_path=u_path, counselor_mobile_col='理财顾问手机号', customer_mobile_col='客户手机号'):
    parse_data.loc[:, [counselor_mobile_col, customer_mobile_col]] = \
        parse_data.loc[:, [counselor_mobile_col, customer_mobile_col]].astype('double')
    def fake_counselor_mobile_no(data_row):
        if data_row.loc[counselor_mobile_col] == 17818265159:
            return data_row.loc[customer_mobile_col]
        else:
            return data_row.loc[counselor_mobile_col]

    # Change fake role into real ones:
    parse_data.loc[:, counselor_mobile_col] = parse_data.apply(fake_counselor_mobile_no, axis=1)
    # match hierarchical relationship:
    hierarchy = intro_data(hierarchy_path, 'Sheet2')
    data = pd.merge(parse_data, hierarchy, how='left', on='理财顾问手机号')

    # team manager could be counselor itself
    def null_team_manager(data_row):
        if (data_row.第2层 == 0) or (pd.isnull(data_row.第2层)):
            return data_row.第1层
        else:
            return data_row.第2层

    data.loc[:, '第2层'] = data.apply(null_team_manager, axis=1)
    data.loc[:, '第3层'] = data.apply(lambda x: null_team_manager(x) if (pd.isnull(x.第3层) or x.第3层==0) else x.第3层, axis=1)
    return data


def data_to_paste(filename=raw_path, u_path=u_path, paper_contract_path=paper_contract_path,
                  sheetname='销售人员统计明细报表', skiprow=1):
    data = clean_raw_data(filename, u_path, paper_contract_path, sheetname, skiprow)
    paste_data = data.reindex(columns=['申请时间', 'empty1', '是否新投', 'empty2', '客户证件号',
                                       '客户姓名', '客户手机号', '投资金额', '投资产品', '业绩折算',
                                       '理财顾问', '第2层', '第3层', '第4层', '城市', '组织名称',
                                       'empty3', '申请时间', '到期时间'])
    def lishui(row):
        if row.第3层 == '溧水营业部经理':
            return '溧水'
        else:
            return row.第3层

    paste_data.loc[:, '第3层'] = paste_data.apply(lambda x: lishui(x), axis=1)
    paste_data.loc[:, '投资金额'] = paste_data.投资金额/10000
    paste_data.loc[:, '业绩折算'] = paste_data.业绩折算/10000
    paste_data.loc[:, '客户证件号'] = paste_data.客户证件号.astype('str')
    return paste_data


def area_performance(filename=raw_path, sheetname='销售人员统计明细报表', skiprow=1):
    data = clean_raw_data(filename, sheetname, skiprow)
    SH_data = data[data.loc[:, '城市'] == '上海市']
    SH_data = SH_data.reindex(columns=['申请时间', '客户姓名', '客户证件号', '客户手机号',
                                       '投资产品', '投资金额', '业绩折算', '理财顾问',
                                       '理财顾问手机号', '到期时间', '是否新投',
                                       '第2层', '第3层', '第4层', '城市', '组织名称'])
    NJ_data = data[data.loc[:, '城市'] == '南京市']
    NJ_data = NJ_data.reindex(columns=['申请时间', '客户姓名', '客户证件号', '客户手机号',
                                       '投资产品', '投资金额', '业绩折算', '理财顾问',
                                       '理财顾问手机号', '到期时间', '是否新投',
                                       '第2层', '第3层', '第4层', '城市', '组织名称'])
    return SH_data, NJ_data


def output_excel(data, filename, sheet_name='Sheet1', na_rep='',
                 float_format=None, columns=None, header=True, index=False,
                 index_label=None, startrow=0, startcol=0, engine=None,
                 merge_cells=True, encoding=None, inf_rep='inf', verbose=True,
                 freeze_panes=None):
    data_writer = pd.ExcelWriter(filename, date_format='YYYY/m/d', datetime_format='YYYY/m/d')
    data.to_excel(data_writer, sheet_name, na_rep,
                  float_format, columns, header, index,
                  index_label, startrow, startcol, engine,
                  merge_cells, encoding, inf_rep, verbose, freeze_panes)
    data_writer.close()
    print('\n%s output done.' % filename)


def area_data_output():  # duplicated, do not use!
    inpath = ''  # input('Set input path(script path as default):\n')
    outpath = ''  # input('Set output path(script path as default):\n')
    my_tool = MyDate()
    dirpath = script_path
    yesterday = my_tool.yesterday
    last_saved = my_tool.last_saved

    # output cleaned data:
    import os
    if os.path.isdir(outpath):
        dirpath = outpath

    if os.path.isfile(inpath):
        raw_path = inpath
        SH_data, NJ_data = area_performance(filename=raw_path)
    else:
        SH_data, NJ_data = area_performance()

    if yesterday == last_saved:
        output_excel(SH_data,
                     '%s\\线上业绩-%s上海.xlsx' % (dirpath, yesterday[5:7] + yesterday[8:]),
                     '销售人员统计明细报表')
        output_excel(NJ_data,
                     '%s\\线上业绩-%s江苏.xlsx' % (dirpath, yesterday[5:7] + yesterday[8:]),
                     '销售人员统计明细报表')
    else:
        output_excel(SH_data,
                     '%s\\线上业绩-%s-%s上海.xlsx' % (dirpath,
                                                last_saved[5:7] + last_saved[8:],
                                                yesterday[5:7] + yesterday[8:]),
                     '销售人员统计明细报表')
        output_excel(NJ_data,
                     '%s\\线上业绩-%s-%s江苏.xlsx' % (dirpath,
                                                last_saved[5:7] + last_saved[8:],
                                                yesterday[5:7] + yesterday[8:]),
                     '销售人员统计明细报表')


if __name__ == '__main__':
    print("Downloading raw data...")
    download_raw_data()
