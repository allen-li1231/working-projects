from compile.my_crawler import nCoreCrawler
from compile.my_class import MyPath, intro_data, sql_connection
from offline_weekly_report.data_clean import match_hierarchy
import pandas as pd
import datetime
path = MyPath().scriptpath  # path = r'E:\Trustsaving\Python\withdrawal_rate'
OC_path = path + r'\OC.xls'
contract_path = path + r'\paper_contract_rate.xlsx'
maturity_report_path = path + r'\maturity.xls'


def download_contract_maturity_report(start_date, end_date):
    crawler = nCoreCrawler()
    crawler.paymentReport(output_filename=maturity_report_path)
    report = pd.read_excel(maturity_report_path, '划扣日表报', skiprows=1)
    report = report[(report.loc[:, '合同到期日'] >= start_date) & (report.loc[:, '合同到期日'] <= end_date)]
    report.to_excel(maturity_report_path, '划扣日报表', index=False)


def download_app_withdraw_report(start_date, end_date):
    withdraw_apply_sql = '''
    select a.create_date,u.mobile_no,c.real_name,u1.mobile_no,a.account_no,a.bank_name,
    a.cash_amount,a.service_fee,a.status,a.last_modify_date
    from t_bus_apply_cash a
    left join t_bus_user u on a.user_name=u.user_name
    left join t_bus_user_basic_info c on a.user_name=c.user_name
    LEFT JOIN t_bus_user_invite_log l ON a.user_name=l.invited_user_name
    left join t_bus_user u1 on u1.user_name=l.user_name
    where date(a.create_date)>=%s and date(a.create_date)<=%s
    and a.status in (109002,109001)
    AND u.role_id in ('ordinary','counselor')
    and u.sys_flag!=2
    order by date(a.create_date)'''
    cur = sql_connection()
    cur.execute(withdraw_apply_sql, [start_date, end_date])
    data = cur.fetchall()
    frame = pd.DataFrame(list(data), columns=['申请时间', '客户手机号', '客户姓名',
                                              '理财顾问手机号', '银行卡号', '开户行',
                                              '提现金额', '手续费', '状态', '划账时间'])
    frame.loc[:, '申请时间'] = frame.loc[:, '申请时间'].astype('datetime64[ns]')
    frame = match_hierarchy(frame)
    return frame


def app_withdraw_apply_output(start_date, end_date, output_path):
    frame = download_app_withdraw_report(start_date, end_date)
    frame.set_index('组织名称', drop=True, inplace=True)
    data = frame.loc[:, '提现金额'].groupby('组织名称').sum()
    data.to_excel(output_path)


def clean_paper_contract():
    contract_rate = intro_data(contract_path, 'Sheet1')
    report = intro_data(maturity_report_path, '划扣日报表')
    report = report[report.loc[:, '合同状态'] != '提前赎回']
    report = report.reindex(columns=['电话号码', '城市', '组织名称', '合同编号',
                                     '划扣日期', '合同到期日', '出借模式',
                                     '出借金额', '账单日', '到期本息'])
    report.loc[:, ['划扣日期', '合同到期日']] = report.loc[:, ['划扣日期', '合同到期日']].astype('datetime64[ns]')
    raw_data = pd.merge(report, contract_rate, 'left', on='合同编号')
    raw_data.loc[:, '到期本息'] = raw_data.apply(paper_interest_principal, axis=1)

    raw_data.set_index(raw_data.loc[:, '组织名称'], drop=True, inplace=True)
    #  data = raw_data.loc[:, '到期本息'].groupby(pd.TimeGrouper("D")).sum()
    data = raw_data.loc[:, '到期本息'].groupby('组织名称').sum()
    data.to_excel(r'output.xlsx')


def paper_interest_principal(data_row):
    if data_row.loc['出借模式'] in ['年月利_旧', '年月利']:
        if data_row.loc['账单日'] == 15:
            first_interest_date = data_row.loc['划扣日期'].replace(month=1 + data_row.loc['划扣日期'].month, day=15)
            day_diff = (first_interest_date - data_row.loc['划扣日期']).days
        elif data_row.loc['账单日'] == 30:
            first_interest_date = data_row.loc['划扣日期'].replace(day=30)
            day_diff = (first_interest_date - data_row.loc['划扣日期']).days

        first_interest = data_row.loc['出借金额'] * data_row.loc['年利率'] * day_diff / 365
        monthly_interest = data_row.loc['出借金额'] * data_row.loc['年利率'] * 30/360
        return data_row.loc['出借金额'] + monthly_interest - first_interest
    else:
        return data_row.loc['出借金额'] * (1 + data_row.loc['年利率'])


def main():
    pass


if __name__ == '__main__':
    start_date = input('Please set start date:')
    end_date = input('Please set end date:')
    path = input('Please set output path:')
    app_withdraw_apply_output(start_date, end_date, path)