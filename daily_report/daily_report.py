"""
@Author: Allen Lee     2018-01-24
"""
import pandas as pd
from weekly_report.weekly_report import WeeklyReportSummary
from compile.my_class import sql_connection, to_timeseries, MyDate, MyPath


class DailyReportSummary:
    def __init__(self):
        mypath = MyPath()
        mydate = MyDate()
        global WeeklyReport
        WeeklyReport = WeeklyReportSummary()
        # import necessary datetime
        self.yesterday = mydate.yesterday
        self.path = mypath.path
        self.last_saved = mydate.last_saved
        self.curdate = mydate.curdate

    def operating_expense(self):
        sql_operating_expense = """
        SELECT b.date,SUM(b.interest+b.doublewin)
        FROM (
        SELECT DATE(create_time) date,SUM(operation_amount) interest,0 doublewin
        FROM cg_user_capital_account_detail
        WHERE disabled = 0
        AND biz_type in(/*'interestCurrent',*/'interestRegular','interestCallBack','interestAddJxq',
        'interestTyj','interestSalary')
        GROUP BY DATE(create_time)
         UNION
        SELECT DATE(create_time),SUM(everyday_interest) interest,0 doublewin
        FROM cg_lingqianbao_income_detail
        WHERE disabled = 0
        AND interestStatus = 2
        GROUP BY DATE(create_time)
         UNION
        SELECT DATE(use_time),0 interest,SUM(ticket_amount) AS doublewin 
        FROM cg_card_ticket
        WHERE disabled=0
        AND (ticket_type_code='SYHBLYH' OR ticket_type_code='SYHBXYH')
        AND `status`=8
        GROUP BY DATE(use_time)
        )b
        GROUP BY b.date;"""

        cur = sql_connection()
        cur.execute(sql_operating_expense)
        operating_expense = cur.fetchall()
        cur.close()
        operating_expense = pd.DataFrame(list(operating_expense), columns=['date', 'amount'])
        return operating_expense

    def product_and_jxq(self):
        sql_product_jxq = """
        SELECT b.date,SUM(b.interest+b.doublewin)
        FROM (
        SELECT DATE(create_time) date,SUM(operation_amount) interest,0 doublewin
        FROM 
          cg_user_capital_account_detail
        WHERE 
          disabled = 0
        AND biz_type in(/*'interestCurrent',*/'interestRegular','interestCallBack','interestAddJxq',
        'interestTyj','interestSalary')
        GROUP BY DATE(create_time)
         UNION
        SELECT DATE(create_time),SUM(everyday_interest) interest,0 doublewin
        FROM 
          cg_lingqianbao_income_detail
        WHERE 
          disabled = 0
        AND 
          interestStatus = 2
        GROUP BY DATE(create_time)
         UNION
        SELECT DATE(use_time),0 interest,SUM(ticket_amount) AS doublewin 
        FROM 
          cg_card_ticket
        WHERE 
          disabled=0
        AND (ticket_type_code='SYHBLYH' OR ticket_type_code='SYHBXYH')
        AND `status`=8
        GROUP BY DATE(use_time)
        )b
        GROUP BY b.date;"""

        cur = sql_connection()
        cur.execute(sql_product_jxq)
        cur.close()
        product_jxq = pd.DataFrame(list(cur.fetchall()), columns=['date', 'interest'])
        product_jxq.set_index('date')
        return product_jxq

    def product_jxq_interest_payable(self):
        sql_product_jxq_interest = """
        SELECT /*SUM(a.interest)/SUM(a.amount)*365*/a.date,SUM(a.interest) FROM (
        SELECT DATE_FORMAT(income_date,'%%Y-%%m') date,SUM(everyday_interest) interest,SUM(total_amount) amount 
        FROM cg_lingqianbao_income_detail
        WHERE DATE(income_date)<=%s
        AND disabled=0
        GROUP BY date
        UNION 
        SELECT DATE_FORMAT(income_date,'%%Y-%%m') date,SUM(everyday_interest) interest,SUM(interest_amount) amount 
        FROM cg_chuxinplan_income_detail
        WHERE DATE(income_date)<=%s
        AND disabled=0
        GROUP BY date
        UNION
        SELECT DATE_FORMAT(income_date,'%%Y-%%m') date,SUM(everyday_interest) interest,SUM(total_amount) amount 
        FROM cg_product_income_detail
        WHERE DATE(income_date)<=%s
        AND disabled=0
        GROUP BY date
        UNION
        SELECT DATE_FORMAT(income_date,'%%Y-%%m') date,SUM(interest_amount) interest,0 amount 
        FROM cg_card_ticket_income_detail
        WHERE disabled=0
        AND ticket_type=1
        AND DATE(income_date)<=%s
        GROUP BY date
        )a
        GROUP BY a.date;"""

        cur = sql_connection()
        cur.execute(sql_product_jxq_interest, [self.curdate, self.curdate, self.curdate, self.curdate])
        payable = cur.fetchall()
        cur.close()
        interest_payable = pd.DataFrame(list(payable), columns=['date', 'interest_payable'])
        return interest_payable

    def cg_fixed_vol(self):
        fixed_income = WeeklyReport.cg_fixed()
        fixed_income.set_index('date', inplace=True)
        # create accumulative fixed income volume
        fixed_income = fixed_income.groupby(pd.TimeGrouper(freq='M')).sum()

        make_vol = "vol_%d = (fixed_income.loc[:, '%d_x'] - fixed_income.loc[:, '%d_y']).cumsum()"
        val = []
        for i in range(1, 13):
            exec(make_vol % (i, i, i))
            val.append(eval("vol_%d" % i))

        fixed_vol = pd.DataFrame(val, index=range(1, 13))
        fixed_vol = fixed_vol.T
        return fixed_vol

    def cg_recharge_withdraw_vol_daily(self):
        from recharge_withdraw.recharge_and_withdraw import cg_recharge, cg_withdraw
        # import necessary datetime:
        last_saved = self.last_saved
        today = self.curdate
        to_the_beginning = '2017-08-10'

        # output necessary data:
        recharge = cg_recharge(to_the_beginning, today)
        withdraw = cg_withdraw(to_the_beginning, today)
        fixed_income = WeeklyReport.cg_fixed()
        recharge = pd.DataFrame(list(recharge), columns=['date', 'mobile_no', 'name', 'amount'])
        withdraw = pd.DataFrame(list(withdraw), columns=['date', 'mobile_no', 'name', 'amount'])

        # data cleaning:
        recharge.set_index('date', inplace=True)
        withdraw.set_index('date', inplace=True)
        fixed_income.set_index('date', inplace=True)
        recharge = recharge.amount.groupby(pd.TimeGrouper(freq='D')).sum()
        withdraw = withdraw.amount.groupby(pd.TimeGrouper(freq='D')).sum()
        recharge_and_withdraw = to_timeseries(to_the_beginning, last_saved, recharge, withdraw)
        return recharge_and_withdraw

    def cg_chuxin_vol_monthly(self):
        chuxin = WeeklyReport.cg_chuxin_plan()
        chuxin.set_index('date', inplace=True)
        chuxin_delta = chuxin.groupby(pd.TimeGrouper(freq='m')).sum()
        chuxin_delta = chuxin_delta.invest - chuxin_delta.withdraw
        chuxin_vol = chuxin_delta.cumsum()
        chuxin_vol.name = 'chuxin'
        return chuxin_vol


def main():
    report = DailyReportSummary()

    yesterday = MyDate().yesterday
    path = report.path
    recharge_and_withdraw = report.cg_recharge_withdraw_vol_daily()
    interest = report.product_and_jxq()
    interest.interest = interest.interest / 10000
    recharge_and_withdraw.iloc[:, 1:] = recharge_and_withdraw.iloc[:, 1:] / 10000
    recharge_and_withdraw = to_timeseries('2017-08-10', yesterday, recharge_and_withdraw, interest)

    fixed_vol = report.cg_fixed_vol()
    chuxin_vol = report.cg_chuxin_vol_monthly()
    fixed_vol.index = fixed_vol.index.strftime('%Y-%m')
    chuxin_vol.index = chuxin_vol.index.strftime('%Y-%m')

    interest_payable = report.product_jxq_interest_payable()
    interest_payable.interest_payable = interest_payable.interest_payable / 10000
    interest_payable = interest_payable.set_index('date')
    product_vol = pd.concat([interest_payable, fixed_vol, chuxin_vol], axis=1)

    recharge_and_withdraw.to_csv(path + r'\recharge_and_withdraw.csv', index=False)
    product_vol.to_csv(path + r'\product_vol.csv', index=True)


if __name__ == '__main__':
    main()