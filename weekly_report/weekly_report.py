"""
@Author: Allen Lee     2018-01-19
"""
import pandas as pd
import datetime
from compile.my_class import sql_connection, to_timeseries, MyDate, MyPath
"""
#index:
#1, coin_purse: invest and withdraw: coin purse (and march1,march2).
#2, old_fixed: invest and withdraw: xinshoubiao, lianliankan, duiduipeng, lulushun, mantanghong, nianyueli, chuchuzhuan.
#              other_statistics: commulative invest and withdraw of product mentioned above before time horizon
#3, cg_fixed: invest and withdraw: 1-12 self.month deposit fixed income product.
#4, cg_chuxin_plan: invest and withdraw on chuxin_plan product.
#5, cg_current: invest, withdraw and volumn on deposit chuyizhuan product.
#6, cg_other_statistic: cg_new_register, cg_new regester_and_investor, cg_annual_mean_rate,
#                       cg_new_investor, cg_new_register_investor, cg_total_invest
"""


class WeeklyReportSummary:
    def __init__(self,  old_start_date='2017-04-17', cg_start_date='2017-08-10', end_date=""):
        self.old_start_date = old_start_date
        self.cg_start_date = cg_start_date
        self.to_the_beginning = '2000-01-01'
        mydate = MyDate()
        mytool = MyPath()
        if end_date == "":
            self.endate = mydate.yesterday
        else:
            self.endate = end_date
        self.month = self.endate[:8] + '01'
        
        old_day_before_start = datetime.datetime.strptime(self.old_start_date, '%Y-%m-%d')
        old_day_before_start = old_day_before_start-datetime.timedelta(days=1)
        self.old_day_before_start = old_day_before_start.strftime('%Y-%m-%d')

        self.to_csv = mytool.to_csv

    def old_coin_purse(self):
        cur = sql_connection()
        print('loading coin_purse_invest...')
        sql_online_invest = "SELECT tbm.product_name,DATE(tbfd.create_date),SUM(tbfd.expenditure) \
                FROM t_bus_financial_details tbfd\
                LEFT JOIN t_bus_user tbu ON tbfd.user_name=tbu.user_name\
                LEFT JOIN t_bus_match tbm ON tbm.product_no=tbfd.product_no\
                WHERE tbu.role_id not in ('ordinary','counselor','special')\
                AND DATE(tbfd.create_date)>=%s\
                AND DATE(tbfd.create_date)<=%s\
                AND tbfd.details_type in ('104022','104028','104038')\
                AND tbu.sys_flag!=2\
                GROUP BY DATE(tbfd.create_date),tbm.product_name;"

        sql_offline_invest = \
            "SELECT tbm.product_name,DATE(tbfd.create_date),SUM(tbfd.expenditure) FROM t_bus_financial_details tbfd\
            LEFT JOIN t_bus_user tbu ON tbfd.user_name=tbu.user_name \
            LEFT JOIN t_bus_match tbm ON tbm.product_no=tbfd.product_no \
            WHERE tbu.role_id in ('ordinary','counselor') \
            AND DATE(tbfd.create_date)>=%s\
            AND DATE(tbfd.create_date)<=%s\
            and tbfd.user_name not in ('AB4E6DAFAF504037BA58F76E728CD887',\
                                        '2EEC41510A864256A8BE93BF9F3D5276',\
                                        '987A08A3797147949528FEF5D7C0E90C')\
            AND tbfd.details_type in ('104022','104028','104038')\
            AND tbu.sys_flag!=2\
            GROUP BY DATE(tbfd.create_date),tbm.product_name;"

        cur.execute(sql_online_invest, [self.old_start_date, self.endate])
        online = pd.DataFrame(list(cur.fetchall()), columns=['type', 'date', 'invest'])
        cur.execute(sql_offline_invest, [self.old_start_date, self.endate])
        offline = pd.DataFrame(list(cur.fetchall()), columns=['type', 'date', 'invest'])

        online_coin_purse_invest = online[online.iloc[:, 0] == '零钱包'].iloc[:, 1:]
        # match1_invest = online[online.iloc[:, 0] == '火柴计划产品'].iloc[:, 1:]
        # match2_invest = online[online.iloc[:, 0] == '火柴计划二号'].iloc[:, 1:]
        offline_coin_purse_invest = offline[offline.iloc[:, 0] == '零钱包'].iloc[:, 1:]

        print('loading coin_purse_interest...')
        sql_online_purse_interest = \
            "SELECT DATE(mi.create_date),SUM(mi.interest) FROM t_bus_match_three_interest mi\
            LEFT JOIN t_bus_user u ON u.user_name=mi.user_name\
            WHERE u.role_id not in ('ordinary','counselor','special')\
            AND DATE(mi.create_date)>=%s\
            AND DATE(mi.create_date)<=%s\
            AND u.sys_flag!=2\
            GROUP BY DATE(mi.create_date);"

        sql_offline_purse_interest = \
            "SELECT DATE(mi.create_date),SUM(mi.interest) FROM t_bus_match_three_interest mi\
            LEFT JOIN t_bus_user u ON u.user_name=mi.user_name\
            WHERE u.role_id in ('ordinary','counselor')\
            AND DATE(mi.create_date)>=%s\
            AND DATE(mi.create_date)<=%s\
            and mi.user_name not in ('AB4E6DAFAF504037BA58F76E728CD887',\
                                    '2EEC41510A864256A8BE93BF9F3D5276',\
                                    '987A08A3797147949528FEF5D7C0E90C')\
            AND u.sys_flag!=2\
            GROUP BY DATE(mi.create_date);"

        cur.execute(sql_online_purse_interest, [self.old_start_date, self.endate])
        online_interest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'interest'])
        cur.execute(sql_offline_purse_interest, [self.old_start_date, self.endate])
        offline_interest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'interest'])

        print('loading coin_purse_withdraw...')
        sql_online_purse_withdraw =\
            "SELECT tbm.product_name,date(tbmw.create_date),SUM(tbmw.withdraw) \
            FROM t_bus_match_withdraw tbmw\
            LEFT JOIN t_bus_match tbm ON tbm.product_no=tbmw.product_no\
            LEFT JOIN t_bus_user tbu ON tbu.user_name=tbmw.user_name\
            WHERE tbu.role_id not in ('ordinary','counselor','special')\
            AND tbu.sys_flag !=2 \
            AND DATE(tbmw.create_date)>=%s\
            AND DATE(tbmw.create_date)<=%s\
            GROUP BY date(tbmw.create_date),tbm.product_name;"

        sql_offline_withdraw = \
            "SELECT tbm.product_name,date(tbmw.create_date),SUM(tbmw.withdraw) \
            FROM t_bus_match_withdraw tbmw\
            LEFT JOIN t_bus_match tbm ON tbm.product_no=tbmw.product_no\
            LEFT JOIN t_bus_user tbu ON tbu.user_name=tbmw.user_name\
            WHERE tbu.role_id in ('ordinary','counselor')\
            and tbu.user_name not in ('AB4E6DAFAF504037BA58F76E728CD887',\
                                    '2EEC41510A864256A8BE93BF9F3D5276',\
                                    '987A08A3797147949528FEF5D7C0E90C')\
            AND tbu.sys_flag !=2 \
            AND DATE(tbmw.create_date)>=%s\
            AND DATE(tbmw.create_date)<=%s\
            GROUP BY date(tbmw.create_date),tbm.product_name;"

        cur.execute(sql_online_purse_withdraw, [self.old_start_date, self.endate])
        online_withdraw = pd.DataFrame(list(cur.fetchall()), columns=('type', 'date', 'withdraw'))
        cur.execute(sql_offline_withdraw, [self.old_start_date, self.endate])
        offline_withdraw = pd.DataFrame(list(cur.fetchall()), columns=('type', 'date', 'withdraw'))
        cur.close()

        online_purse_withdraw = online_withdraw[online_withdraw.type == '零钱包'].iloc[:, 1:]
        offline_purse_withdraw = offline_withdraw[offline_withdraw.type == '零钱包'].iloc[:, 1:]

        no1_match_plan = online_withdraw[online_withdraw.type == '火柴计划产品'].iloc[:, 1:]
        no2_match_plan = online_withdraw[online_withdraw.type == '火柴计划二号'].iloc[:, 1:]

        purse_data = to_timeseries(self.old_start_date, self.endate,
                                   online_coin_purse_invest,
                                   online_interest,
                                   online_purse_withdraw,
                                   offline_coin_purse_invest,
                                   offline_interest,
                                   offline_purse_withdraw,
                                   no1_match_plan, no2_match_plan)
        return purse_data

    def old_fixed(self):
        cur = sql_connection()
        print('loading old fixed invest...')
        sql_invest = \
            "SELECT date(d.create_date),f.finance_type,SUM(d.expenditure) FROM t_bus_financial_details d\
            LEFT JOIN t_bus_user u ON d.user_name=u.user_name\
            LEFT JOIN t_bus_finance f ON d.product_no=f.finance_no\
            WHERE date(d.create_date)>=%s\
            AND date(d.create_date)<=%s\
            AND d.details_type='104042'\
            AND u.sys_flag!=2\
            AND u.role_id not in ('ordinary','counselor','special')\
            GROUP BY date(d.create_date),f.finance_type;"

        cur.execute(sql_invest, [self.old_start_date, self.endate])
        fixed_invest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'type', 'invest'])

        i_xinshoubiao = fixed_invest[fixed_invest.type == '106024'].drop('type', axis=1)
        i_lianliankan = fixed_invest[fixed_invest.type == '106020'].drop('type', axis=1)
        i_duiduipeng = fixed_invest[fixed_invest.type == '106022'].drop('type', axis=1)
        i_lulushun = fixed_invest[fixed_invest.type == '106023'].drop('type', axis=1)
        i_mantanghong = fixed_invest[fixed_invest.type == '106026'].drop('type', axis=1)
        i_nianyueli360 = fixed_invest[fixed_invest.type == '106019'].drop('type', axis=1)
        i_xinshouzhuan = fixed_invest[fixed_invest.type == '300000'].drop('type', axis=1)
        i_yueyuezhuan = fixed_invest[fixed_invest.type == '300001'].drop('type', axis=1)
        i_jijizhuan = fixed_invest[fixed_invest.type == '300002'].drop('type', axis=1)
        i_bannianzhuan = fixed_invest[fixed_invest.type == '300003'].drop('type', axis=1)
        i_huodongbiao = fixed_invest[fixed_invest.type == '106027'].drop('type', axis=1)

        sql_withdraw = \
            "SELECT DATE(shuhui.date),tbf.finance_type,SUM(tbfd.expenditure) FROM t_bus_financial_details tbfd\
            LEFT JOIN t_bus_user tbu ON tbfd.user_name=tbu.user_name\
            LEFT JOIN t_bus_finance tbf ON tbfd.product_no=tbf.finance_no\
            LEFT JOIN (\
            SELECT date(lock_over_date) date,finance_no FROM t_bus_finance \
            WHERE date(lock_over_date)<=%s\
            ) shuhui ON shuhui.finance_no=tbf.finance_no\
            WHERE tbu.sys_flag!=2\
            AND tbfd.details_type='104042'\
            AND shuhui.date is NOT NULL\
            AND DATE(tbfd.create_date)>=%s\
            AND DATE(tbfd.create_date)<=%s\
            AND tbu.role_id not in ('ordinary','counselor','special')\
            GROUP BY DATE(shuhui.date),tbf.finance_type;"

        sql_chuchuzhuan_withdraw = \
            "SELECT DATE(tbfc.modify_date),tbfc.finance_type,SUM(tbfc.has_repay_amount) \
            FROM t_bus_finance_collection tbfc\
            left join t_bus_user u on u.user_name=tbfc.user_name\
            LEFT JOIN t_bus_finance tbf ON tbfc.finance_no=tbf.finance_no\
            WHERE date(tbfc.modify_date)>=%s\
            and date(tbfc.modify_date)<=%s\
            AND tbf.finace_parent_type='chuchuzhuan'\
            and u.role_id not in ('counselor','ordinary','special')\
            GROUP BY DATE(tbfc.modify_date),tbfc.finance_type;"

        sql_nianyueli_interest = \
            "SELECT DATE(tbfc.modify_date),SUM(tbfc.has_repay_interest)FROM t_bus_finance_collection tbfc\
            left join t_bus_user u on u.user_name=tbfc.user_name\
            WHERE date(tbfc.modify_date)>=%s\
            and date(tbfc.modify_date)<=%s\
            AND tbfc.finance_type='106019'\
            AND u.role_id not in ('ordinary','counselor','special')\
            GROUP BY DATE(tbfc.modify_date);"

        sql_yueyuejia = \
            "SELECT DATE(shuhui.create_date),SUM(income),SUM(mli.amount),SUM(mli.interest) FROM(\
            SELECT user_name,create_date,income FROM t_bus_financial_details tbfd\
            WHERE tbfd.details_type='104037')shuhui\
            LEFT JOIN t_bus_match_link_invest mli \
            ON shuhui.user_name=mli.user_name AND shuhui.create_date=mli.clearing_date\
            LEFT JOIN t_bus_user tbu ON tbu.user_name=shuhui.user_name\
            WHERE date(mli.clearing_date)>=%s\
            and date(mli.clearing_date)<=%s\
            AND tbu.sys_flag!=2\
            and tbu.role_id not in ('ordinary','counselor','special')\
            GROUP BY DATE(shuhui.create_date);"

        sql_yueyuejia_vol = \
            "SELECT SUM(mli.amount),SUM(mli.interest) FROM t_bus_match_link_invest mli\
            LEFT JOIN t_bus_financial_details tbfd \
            ON mli.product_no=tbfd.product_no AND mli.create_date=tbfd.create_date and mli.user_name=tbfd.user_name\
            WHERE (mli.clearing_date>%s OR mli.clearing_date IS NULL)\
            AND mli.user_name in (" \
            "select user_name from t_bus_user where role_id in ('cgOrdinary', 'cgSuper'));"

        sql_old_mean_annual_rate = \
            "SELECT SUM(a.`存量利率积`)/SUM(a.`存量和`) FROM (\
            SELECT remain.finance_type,SUM(remain.sum) 存量和,remain.`存量利率积` FROM(\
            SELECT f.finance_type,SUM(i.total_amount) sum,ROUND(SUM(f.apr/100*i.total_amount),2)存量利率积\
            FROM t_bus_finance_invest i\
            LEFT JOIN t_bus_finance f ON i.finance_no=f.finance_no\
            left join t_bus_user u on u.user_name=i.user_name\
            WHERE date(f.lock_over_date)>%s\
            AND date(i.create_date)<=%s\
            AND u.role_id in ('cgOrdinary','cgSuper')\
            AND f.finance_type NOT in('300000','300001','300002','300003')\
            GROUP BY f.finance_type\
            UNION\
            SELECT m.product_type,SUM(m3i.clearing_amount),ROUND(SUM(m.apr/100*m3i.clearing_amount),2)\
            FROM t_bus_match_three_interest m3i\
            LEFT JOIN t_bus_match m ON m3i.product_no=m.product_no\
            left join t_bus_user u on u.user_name=m3i.user_name\
            WHERE DATE(m3i.create_date)=DATE(%s)\
            AND u.role_id in ('cgOrdinary','cgSuper')\
            GROUP BY m.product_type\
            )remain\
            GROUP BY remain.finance_type)a;"

        cur.execute(sql_withdraw, [self.endate, self.to_the_beginning, self.endate])
        fixed_withdraw = pd.DataFrame(list(cur.fetchall()), columns=['date', 'type', 'withdraw'])

        cur.execute(sql_chuchuzhuan_withdraw, [self.old_start_date, self.endate])
        chuchuzhuan_withdraw = pd.DataFrame(list(cur.fetchall()), columns=['date', 'type', 'withdraw'])

        cur.execute(sql_nianyueli_interest, [self.old_start_date, self.endate])
        interest_nianyueli = pd.DataFrame(list(cur.fetchall()), columns=['date', 'interest'])

        cur.execute(sql_yueyuejia, [self.to_the_beginning, self.endate])
        yueyuejia = pd.DataFrame(list(cur.fetchall()), columns=['date', 'invest', 'withdraw', 'interest'])
        yueyuejia_slice_date = datetime.date(int(self.old_start_date[:4]), int(self.old_start_date[5:7]), int(self.old_start_date[8:]))
        yueyuejia_main = yueyuejia[yueyuejia.date >= yueyuejia_slice_date]
        yueyuejia_withdraw = yueyuejia_main.loc[:, ['date', 'withdraw']]

        w_xinshoubiao = fixed_withdraw[fixed_withdraw.type == '106024'].drop('type', axis=1)
        w_lianliankan = fixed_withdraw[fixed_withdraw.type == '106020'].drop('type', axis=1)
        w_duiduipeng = fixed_withdraw[fixed_withdraw.type == '106022'].drop('type', axis=1)
        w_lulushun = fixed_withdraw[fixed_withdraw.type == '106023'].drop('type', axis=1)
        w_mantanghong = fixed_withdraw[fixed_withdraw.type == '106026'].drop('type', axis=1)
        w_nianyueli360 = fixed_withdraw[fixed_withdraw.type == '106019'].drop('type', axis=1)
        w_xinshouzhuan = chuchuzhuan_withdraw[chuchuzhuan_withdraw.type == '300000'].drop('type', axis=1)
        w_yueyuezhuan = chuchuzhuan_withdraw[chuchuzhuan_withdraw.type == '300001'].drop('type', axis=1)
        w_jijizhuan = chuchuzhuan_withdraw[chuchuzhuan_withdraw.type == '300002'].drop('type', axis=1)
        w_bannianzhuan = chuchuzhuan_withdraw[chuchuzhuan_withdraw.type == '300003'].drop('type', axis=1)
        w_huodongbiao = fixed_withdraw[fixed_withdraw.type == '106027'].drop('type', axis=1)

        old_invest = to_timeseries(self.old_start_date, self.endate,
                                   i_xinshoubiao, w_xinshoubiao,
                                   i_lianliankan, w_lianliankan,
                                   i_duiduipeng, w_duiduipeng,
                                   i_lulushun, w_lulushun,
                                   i_mantanghong, w_mantanghong,
                                   i_nianyueli360,  w_nianyueli360, interest_nianyueli,
                                   i_xinshouzhuan, w_xinshouzhuan,
                                   i_yueyuezhuan, w_yueyuezhuan,
                                   i_jijizhuan, w_jijizhuan,
                                   i_bannianzhuan, w_bannianzhuan,
                                   i_huodongbiao, w_huodongbiao,
                                   yueyuejia_withdraw)
        label = ['date', 'i_xinshoubiao', 'w_xinshoubiao',
                 'i_lianliankan', 'w_lianliankan',
                 'i_duiduipeng', 'w_duiduipeng',
                 'i_lulushun', 'w_lulushun',
                 'i_mantanghong', 'w_mantanghong',
                 'i_nianyueli360', 'w_nianyueli360', 'interest_nianyueli',
                 'i_xinshouzhuan', 'w_xinshouzhuan',
                 'i_yueyuezhuan', 'w_yueyuezhuan',
                 'i_jijizhuan', 'w_jijizhuan',
                 'i_bannianzhuan', 'w_bannianzhuan',
                 'i_huodongbiao', 'w_huodongbiao',
                 'yueyuejia_withdraw']
        # old_invest.set_axis(axis=1, labels=label)
        old_invest.columns = label

        # other statistics:
        print('loading other old statistics...')
        cur.execute(sql_nianyueli_interest, [self.to_the_beginning, self.old_day_before_start])
        nianyueli_cumminterest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'interest'])
        nianyueli_cumminterest = float(sum(nianyueli_cumminterest.interest))

        cur.execute(sql_invest, [self.to_the_beginning, self.old_day_before_start])
        chuchuzhuan_cumminvest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'type', 'invest'])

        cur.execute(sql_chuchuzhuan_withdraw, [self.to_the_beginning, self.old_day_before_start])
        chuchuzhuan_cummwithdraw = pd.DataFrame(list(cur.fetchall()), columns=['date', 'type', 'withdraw'])

        cur.execute(sql_yueyuejia_vol, self.old_day_before_start)
        yueyuejia_vol = cur.fetchall()
        yueyuejia_vol = float(yueyuejia_vol[0][0])

        cur.execute(sql_old_mean_annual_rate, [self.endate, self.endate, self.endate])
        old_mean_annual_rate = cur.fetchone()[0]
        cur.close()

        huodongbiao_cumminvest = chuchuzhuan_cumminvest[chuchuzhuan_cumminvest.type == '106027']
        huodongbiao_cummwithdraw = chuchuzhuan_cummwithdraw[chuchuzhuan_cummwithdraw.type == '106027']
        huodongbiao_vol = float(sum(huodongbiao_cumminvest.invest) - sum(huodongbiao_cummwithdraw.withdraw))

        xinshouzhuan_cumm = chuchuzhuan_cumminvest[chuchuzhuan_cumminvest.type == '300000']
        xinshouzhuan_cumminvest = float(xinshouzhuan_cumm.invest.sum())
        xinshouzhuan_cumm = chuchuzhuan_cummwithdraw[chuchuzhuan_cummwithdraw.type == '300000']
        xinshouzhuan_cummwithdraw = float(xinshouzhuan_cumm.withdraw.sum())

        yueyuezhuan_cumm = chuchuzhuan_cumminvest[chuchuzhuan_cumminvest.type == '300001']
        yueyuezhuan_cumminvest = float(yueyuezhuan_cumm.invest.sum())
        yueyuezhuan_cumm = chuchuzhuan_cummwithdraw[chuchuzhuan_cummwithdraw.type == '300001']
        yueyuezhuan_cummwithdraw = float(yueyuezhuan_cumm.withdraw.sum())

        jijizhuan_cumm = chuchuzhuan_cumminvest[chuchuzhuan_cumminvest.type == '300002']
        jijizhuan_cumminvest = float(jijizhuan_cumm.invest.sum())
        jijizhuan_cumm = chuchuzhuan_cummwithdraw[chuchuzhuan_cummwithdraw.type == '300002']
        jijizhuan_cummwithdraw = float(jijizhuan_cumm.withdraw.sum())

        bannianzhuan_cumm = chuchuzhuan_cumminvest[chuchuzhuan_cumminvest.type == '300003']
        bannianzhuan_cumminvest = float(bannianzhuan_cumm.invest.sum())
        bannianzhuan_cumm = chuchuzhuan_cummwithdraw[chuchuzhuan_cummwithdraw.type == '300003']
        bannianzhuan_cummwithdraw = float(bannianzhuan_cumm.withdraw.sum())

        cumm_stats = [old_mean_annual_rate, nianyueli_cumminterest,
                      xinshouzhuan_cumminvest, xinshouzhuan_cummwithdraw,
                      yueyuezhuan_cumminvest, yueyuezhuan_cummwithdraw,
                      jijizhuan_cumminvest, jijizhuan_cummwithdraw,
                      bannianzhuan_cumminvest, bannianzhuan_cummwithdraw,
                      huodongbiao_vol, yueyuejia_vol]
        cumm_label = ['old_mean_annual_rate', 'nianyueli_cumminterest',
                      'xinshouzhuan_cumminvest', 'xinshouzhuan_cummwithdraw',
                      'yueyuezhuan_cumminvest', 'yueyuezhuan_cummwithdraw',
                      'jijizhuan_cumminvest', 'jijizhuan_cummwithdraw',
                      'bannianzhuan_cumminvest', 'bannianzhuan_cummwithdraw',
                      'huodongbiao_vol', 'yueyuejia_vol']
        return old_invest, cumm_stats, cumm_label

    def cg_fixed(self):
        cur = sql_connection()
        print('loading cg fixed income...')
        sql_fixed_invest = \
            "SELECT DATE(i.invest_time),\
            SUM(CASE i.plan_code WHEN 'DQ001' THEN i.amount ELSE 0 END)/10000 '1',\
            SUM(CASE i.plan_code WHEN 'DQ002' THEN i.amount ELSE 0 END)/10000 '2',\
            SUM(CASE i.plan_code WHEN 'DQ003' THEN i.amount ELSE 0 END)/10000 '3',\
            SUM(CASE i.plan_code WHEN 'DQ004' THEN i.amount ELSE 0 END)/10000 '4',\
            SUM(CASE i.plan_code WHEN 'DQ005' THEN i.amount ELSE 0 END)/10000 '5',\
            SUM(CASE i.plan_code WHEN 'DQ006' THEN i.amount ELSE 0 END)/10000 '6',\
            SUM(CASE i.plan_code WHEN 'DQ007' THEN i.amount ELSE 0 END)/10000 '7',\
            SUM(CASE i.plan_code WHEN 'DQ008' THEN i.amount ELSE 0 END)/10000 '8',\
            SUM(CASE i.plan_code WHEN 'DQ009' THEN i.amount ELSE 0 END)/10000 '9',\
            SUM(CASE i.plan_code WHEN 'DQ010' THEN i.amount ELSE 0 END)/10000 '10',\
            SUM(CASE i.plan_code WHEN 'DQ011' THEN i.amount ELSE 0 END)/10000 '11',\
            SUM(CASE i.plan_code WHEN 'DQ012' THEN i.amount ELSE 0 END)/10000 '12' \
            FROM cg_user_invest i\
            WHERE i.plan_code!='LQB01'\
            ANd date(i.invest_time)>=%s\
            AND date(i.invest_time)<=%s\
            GROUP BY DATE(i.invest_time);"

        sql_fixed_withdraw = \
            "SELECT DATE(DATE_ADD(i.end_interest_date,INTERVAL 1 DAY)),\
            SUM(CASE i.plan_code WHEN 'DQ001' THEN i.amount ELSE 0 END)/10000 '1',\
            SUM(CASE i.plan_code WHEN 'DQ002' THEN i.amount ELSE 0 END)/10000 '2',\
            SUM(CASE i.plan_code WHEN 'DQ003' THEN i.amount ELSE 0 END)/10000 '3',\
            SUM(CASE i.plan_code WHEN 'DQ004' THEN i.amount ELSE 0 END)/10000 '4',\
            SUM(CASE i.plan_code WHEN 'DQ005' THEN i.amount ELSE 0 END)/10000 '5',\
            SUM(CASE i.plan_code WHEN 'DQ006' THEN i.amount ELSE 0 END)/10000 '6',\
            SUM(CASE i.plan_code WHEN 'DQ007' THEN i.amount ELSE 0 END)/10000 '7',\
            SUM(CASE i.plan_code WHEN 'DQ008' THEN i.amount ELSE 0 END)/10000 '8',\
            SUM(CASE i.plan_code WHEN 'DQ009' THEN i.amount ELSE 0 END)/10000 '9',\
            SUM(CASE i.plan_code WHEN 'DQ010' THEN i.amount ELSE 0 END)/10000 '10',\
            SUM(CASE i.plan_code WHEN 'DQ011' THEN i.amount ELSE 0 END)/10000 '11',\
            SUM(CASE i.plan_code WHEN 'DQ012' THEN i.amount ELSE 0 END)/10000 '12' \
            FROM cg_user_invest i\
            WHERE i.plan_code!='LQB01'\
            AND DATE_ADD(date(i.end_interest_date),INTERVAL 1 DAY)>=%s\
            AND DATE_ADD(date(i.end_interest_date),INTERVAL 1 DAY)<=%s\
            GROUP BY DATE(DATE_ADD(date(i.end_interest_date),INTERVAL 1 DAY));"

        cur.execute(sql_fixed_invest, [self.cg_start_date, self.endate])
        fixed_invest = pd.DataFrame(list(cur.fetchall()), columns=['date', '1', '2', '3', '4', '5', '6',
                                                                   '7', '8', '9', '10', '11', '12'])
        cur.execute(sql_fixed_withdraw, [self.cg_start_date, self.endate])
        fixed_withdraw = pd.DataFrame(list(cur.fetchall()), columns=['date', '1', '2', '3', '4', '5', '6',
                                                                     '7', '8', '9', '10', '11', '12'])
        cur.close()

        cg_fixed = to_timeseries(self.cg_start_date, self.endate, fixed_invest, fixed_withdraw)
        cg_fixed = cg_fixed.reindex(columns=['date', '1_x', '1_y', '2_x', '2_y', '3_x', '3_y', '4_x', '4_y',
                                             '5_x', '5_y', '6_x', '6_y', '7_x', '7_y', '8_x', '8_y',
                                             '9_x', '9_y', '10_x', '10_y', '11_x', '11_y', '12_x', '12_y'])
        return cg_fixed

    def cg_chuxin_plan(self):
        cur = sql_connection()
        print('loading chuxin plan...')
        sql_chuxin_invest = \
            "SELECT DATE(invest_date),SUM(invest_amount)/10000\
            FROM cg_user_chuxin_plan_detail\
            WHERE disabled=0\
            and DATE(invest_date)>=%s\
            and DATE(invest_date)<=%s\
            AND invest_flag=1\
            GROUP BY DATE(invest_date);"

        sql_chuxin_withdraw = \
            "SELECT DATE(a.quite_time),SUM(a.amount)/10000 FROM(\
            SELECT p.quite_time,p.id,SUM(d.invest_amount) amount \
            FROM cg_user_chuxin_plan_detail d\
            LEFT JOIN cg_user_chuxin_planinfo p ON p.id=d.planinfo_id\
            WHERE d.disabled=0\
            AND p.is_quite=1\
            AND d.invest_flag=1\
            GROUP BY p.id\
            )a\
            where (DATE(a.quite_time)>=%s\
                   and DATE(a.quite_time)>='2017-11-01')\
            and DATE(a.quite_time)<=%s\
            GROUP BY DATE(a.quite_time);"

        cur.execute(sql_chuxin_invest, [self.cg_start_date, self.endate])
        chuxin_invest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'invest'])

        cur.execute(sql_chuxin_withdraw, [self.cg_start_date, self.endate])
        chuxin_withdraw = pd.DataFrame(list(cur.fetchall()), columns=['date', 'withdraw'])
        cur.close()

        cg_chuxin = to_timeseries(self.cg_start_date, self.endate, chuxin_invest, chuxin_withdraw)
        return cg_chuxin

    def cg_current(self):
        cur = sql_connection()
        print('loading cg current...')
        sql_current = \
            "SELECT DATE(LQB.date),SUM(LQB.recharge+LQB.replace_recharge+LQB.interest+LQB.doublewin+DQback+CXback) 入,\
            SUM(LQB.deduct+LQB.withdraw+(LQB.DQtotal-LQB.DQdirect)+LQB.CXpurse) 出,\
            SUM(LQB.recharge+LQB.replace_recharge+LQB.interest+LQB.doublewin+DQback-LQB.deduct-LQB.withdraw\
            -(LQB.DQtotal-LQB.DQdirect)-LQB.CXpurse+CXback) 增量\
            FROM (\
            SELECT DATE(transaction_time) date,SUM(amount) recharge,0 replace_recharge,0 deduct,\
              0 withdraw,0 DQtotal,0 DQdirect,0 interest,0 doublewin,0 DQback,0 CXpurse,0 CXback\
            FROM cg_recharge_detail\
            WHERE disabled = 0\
            AND bus_sataus = 1\
            AND recharge_type=0\
            GROUP BY DATE(transaction_time)\
             UNION\
            SELECT DATE(modify_time),0,SUM(operation_amount) replace_recharge,0,0,0,0,0,0,0,0,0\
            FROM cg_replace_recharge\
            WHERE disabled = 0\
            AND apply_status=2\
            GROUP BY DATE(modify_time)\
             UNION\
            SELECT DATE(modify_time),0,0,SUM(operation_amount) deduct,0,0,0,0,0,0,0,0\
            FROM cg_deduct_apply\
            WHERE disabled = 0\
            AND apply_status=2\
            GROUP BY DATE(modify_time)\
             UNION\
            SELECT DATE(transaction_time),0,0,0, SUM(amount) withdraw,0,0,0,0,0,0,0\
            FROM cg_withdraw_apply\
            WHERE disabled = 0\
            AND bus_sataus = 1\
            GROUP BY DATE(transaction_time)\
             UNION\
            SELECT DATE(invest_time),0,0,0,0,SUM(amount) AS DQtotal,0,0,0,0,0,0\
            FROM cg_user_invest\
            WHERE disabled = 0\
            AND plan_code != 'LQB01'\
            GROUP BY DATE(invest_time)\
             UNION\
            SELECT DATE(transaction_time),0,0,0,0,0,SUM(amount) AS DQdirect,0,0,0,0,0\
            FROM cg_recharge_detail\
            WHERE disabled = 0\
            AND recharge_type = 1\
            AND bus_sataus = 1\
            GROUP BY DATE(transaction_time)\
             UNION\
            SELECT DATE(create_time),0,0,0,0,0,0,SUM(operation_amount) interest,0,0,0,0\
            FROM cg_user_capital_account_detail\
            WHERE disabled = 0\
            AND biz_type in('interestRegular','interestCallBack','interestAddJxq','interestTyj','interestSalary')\
            GROUP BY DATE(create_time)\
             UNION\
            SELECT DATE(create_time),0,0,0,0,0,0,SUM(everyday_interest) interest,0,0,0,0\
            FROM cg_lingqianbao_income_detail\
            WHERE disabled = 0\
            AND interestStatus = 2\
            GROUP BY DATE(create_time)\
             UNION\
            SELECT DATE(use_time),0,0,0,0,0,0,0,SUM(ticket_amount) AS doublewin,0,0,0\
            FROM cg_card_ticket\
            WHERE disabled=0\
            AND ticket_type_code in ('SYHBLYH','SYHBXYH')\
            AND `status`=8\
            GROUP BY DATE(use_time)\
             UNION\
            SELECT DATE(DATE_ADD(end_interest_date,INTERVAL 1 DAY)),0,0,0,0,0,0,0,0,SUM(amount) AS DQback,0,0\
            FROM cg_user_invest\
            WHERE disabled = 0\
            AND plan_code != 'LQB01'\
            GROUP BY DATE(DATE_ADD(end_interest_date,INTERVAL 1 DAY))\
            UNION\
            SELECT DATE(create_time),0,0,0,0,0,0,0,0,0,SUM(operation_amount) AS CXpurse,0\
            FROM cg_user_capital_account_detail\
            WHERE disabled = 0\
            AND biz_type = 'switchChuxin'\
            GROUP BY DATE(create_time) \
            UNION\
            SELECT DATE(a.quite_time),0,0,0,0,0,0,0,0,0,0,SUM(a.amount) AS CXback\
            FROM\
            (SELECT p.quite_time,p.id,SUM(d.invest_amount) amount\
            FROM cg_user_chuxin_plan_detail d\
            LEFT JOIN cg_user_chuxin_planinfo p ON p.id = d.planinfo_id\
            WHERE d.disabled = 0\
            AND p.is_quite = 1\
            AND d.invest_flag = 1\
            GROUP BY p.id\
            ) a\
            GROUP BY\
            DATE(a.quite_time)\
            ) LQB\
            WHERE DATE(LQB.date) <= DATE(NOW())\
            GROUP BY LQB.date;"

        cur.execute(sql_current)
        cg_current = pd.DataFrame(list(cur.fetchall()), columns=['date', 'in', 'out', 'delta'])
        cur.close()

        cg_current.delta = cg_current.delta.cumsum()
        cg_current.date = cg_current.date.astype('datetime64[ns]')
        cg_current.iloc[:, 1:] = cg_current.iloc[:, 1:].apply(lambda x: x/10000)
        return cg_current

    def cg_other_statistic(self):
        cur = sql_connection()
        print('loading other cg statistics...')
        sql_cg_annual_mean_rate = \
            "SELECT SUM(a.`存量利率积`)/SUM(a.`存量和`)*100 FROM (\
            SELECT remain.plan_code,SUM(remain.sum) 存量和,remain.`存量利率积` FROM(\
            SELECT i.plan_code,SUM(i.amount) sum,\
            ROUND(SUM(i.cal_invest_rate/100*i.amount),2)存量利率积 FROM cg_user_invest i\
            WHERE i.plan_code!='LQB01'\
            AND DATE_ADD(i.end_interest_date,INTERVAL 1 DAY)>%s\
            AND i.invest_time<=%s\
            AND i.user_name not in (\
            select user_name from t_bus_user \
            where role_id in ('counselor','ordinary'))\
            GROUP BY i.plan_code\
            UNION\
            SELECT 'ChuxinPlan',SUM(d.interest_amount) sum,\
            ROUND(SUM(d.interest_rate/100*d.interest_amount),2) 存量利率积\
            FROM cg_chuxinplan_income_detail d\
            WHERE d.disabled=0\
            AND DATE(d.income_date)=%s\
            UNION\
            SELECT 'LQB01',SUM(LQB.current_amount)+SUM(LQB.frozen_amount) sum,\
            ROUND(SUM((LQB.current_amount+LQB.frozen_amount)/100*6.8),2) FROM (\
            SELECT DATE(d.create_time),d.user_name,d.current_amount,d.frozen_amount \
            FROM cg_user_capital_account_detail d\
            LEFT JOIN (\
            SELECT DATE(d.create_time),d.user_name,MAX(id) id\
            FROM cg_user_capital_account_detail d\
            GROUP BY DATE(d.create_time),d.user_name\
            )maxid ON maxid.id=d.id\
            WHERE DATE(d.create_time)=%s\
            AND maxid.id is NOT NULL\
            )LQB\
            )remain\
            GROUP BY remain.plan_code)a;"

        sql_new_register = "SELECT DATE(create_date),COUNT(user_name) FROM t_bus_user\
                            WHERE role_id='cgOrdinary'\
                            AND DATE(create_date)>=%s\
                            AND DATE(create_date)<=%s\
                            GROUP BY DATE(create_date);"

        sql_new_cg_register = "SELECT DATE(depository_create_time),COUNT(user_name) FROM cg_user_info\
                              WHERE user_name NOT in(\
                              SELECT user_name FROM t_bus_account\
                              where create_time<=%s)\
                              GROUP BY DATE(depository_create_time);"

        sql_new_investor = \
            "SELECT COUNT(DISTINCT a.user_name) FROM (\
            SELECT user_name FROM t_bus_financial_details\
            WHERE date(create_date)>=%s\
            AND date(create_date)<=%s\
            AND details_type in('104007','104022','104028','104030','104031','104032','104036','104038','104042')\
            UNION\
            SELECT user_name FROM cg_user_invest\
            WHERE date(invest_time)>=%s\
            AND date(invest_time)<=%s\
            AND amount>=3\
            )a\
            LEFT JOIN t_bus_user u ON u.user_name=a.user_name\
            WHERE u.role_id='cgOrdinary'\
            AND a.user_name NOT in (\
            SELECT user_name FROM t_bus_financial_details\
            WHERE date(create_date)<=%s\
            AND details_type in('104007','104022','104028','104030','104031','104032','104036','104038','104042')\
            );"

        sql_new_register_investor = \
            "SELECT COUNT(DISTINCT a.user_name) FROM (\
            SELECT user_name FROM t_bus_financial_details\
            WHERE date(create_date)>=%s\
            AND date(create_date)<=%s\
            AND details_type in('104007','104022','104028','104030','104031','104032','104036','104038','104042')\
            UNION\
            SELECT user_name FROM cg_user_invest\
            WHERE date(invest_time)>=%s\
            AND date(invest_time)<=%s\
            AND amount>=3\
            )a\
            LEFT JOIN t_bus_user u ON u.user_name=a.user_name\
            WHERE u.role_id='cgOrdinary'\
            AND a.user_name NOT in (\
            SELECT user_name FROM t_bus_financial_details\
            WHERE date(create_date)<=%s\
            AND details_type in('104007','104022','104028','104030','104031','104032','104036','104038','104042')\
            )\
            AND date(u.create_date)>=%s\
            AND date(u.create_date)<=%s;"

        sql_cg_total_invest = \
            "SELECT SUM(a.amount) amount FROM(\
            SELECT SUM(amount) amount FROM cg_user_invest\
            WHERE date(invest_time)>=%s\
            AND date(invest_time)<=%s\
            AND amount>=3\
            UNION\
            SELECT SUM(invest_amount) amount FROM cg_user_chuxin_plan_detail\
            WHERE disabled=0\
            AND invest_flag=1\
            AND date(invest_date)>=%s\
            AND date(invest_date)<=%s\
            UNION\
            SELECT SUM(expenditure) amount FROM t_bus_financial_details tbfd\
            left join t_bus_user u on u.user_name=tbfd.user_name\
            WHERE tbfd.details_type in \
            ('104007','104022','104028','104030','104031','104032','104036','104038','104042')\
            AND date(tbfd.create_date)>=%s\
            AND date(tbfd.create_date)<=%s\
            AND role_id='cgOrdinary')a;"

        # TODO: the number of new investors in a week is remain developing...
        cur.execute(sql_cg_annual_mean_rate, [self.endate, self.endate, self.endate, self.endate])
        cg_annual_mean_rate = float(cur.fetchall()[0][0])

        cur.execute(sql_new_register, [self.cg_start_date, self.endate])
        new_register = pd.DataFrame(list(cur.fetchall()), columns=['date', 'new_register'])

        cur.execute(sql_new_cg_register, self.endate)
        new_cg_register = pd.DataFrame(list(cur.fetchall()), columns=['date', 'new_cg_register'])

        cur.execute(sql_new_investor, [self.month, self.endate, self.month, self.endate, self.endate])
        new_investor = int(cur.fetchall()[0][0])

        cur.execute(sql_new_register_investor,
                    [self.month, self.endate, self.month, self.endate, self.endate, self.month, self.endate])
        new_register_investor = int(cur.fetchall()[0][0])

        cur.execute(sql_cg_total_invest, [self.month, self.endate, self.month, self.endate, self.month, self.endate])
        cg_total_invest = float(cur.fetchall()[0][0])
        cur.close()

        new_reginvest = to_timeseries(self.cg_start_date, self.endate, new_register, new_cg_register)
        label = ['平均年化利率', '当月新投资用户', '当月新注册并投资用户', '当月有效投资金额']
        statnum = [cg_annual_mean_rate, new_investor, new_register_investor, cg_total_invest]
        return new_reginvest, statnum, label


if __name__ == '__main__':
    print("@Author: Allen Lee\n")
    import datetime
    old_start_date = input('Please set old app start date\n'
                           '(2017-04-17 as default for old version)\npress Enter to continue:\n')
    cg_start_date = input('Please set cg start date\n'
                          '(2017-08-10 as default for cg version)\npress Enter to continue:\n')

    if old_start_date == '':
        old_start_date = '2017-04-17'
        old_day_before_start = '2017-04-16'
    else:
        old_day_before_start = datetime.datetime.strptime(old_start_date, '%Y-%m-%d')
        old_day_before_start = old_day_before_start-datetime.timedelta(days=1)
        old_day_before_start = old_day_before_start.strftime('%Y-%m-%d')

    if cg_start_date == '':
        cg_start_date = '2017-08-10'

    end_date = input('Please set end date\n'
                     'press Enter to continue (Yesterday as default):')
    if end_date == '':
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        endate = yesterday.strftime('%Y-%m-%d')
    else:
        endate = end_date

    to_the_beginning = '2000-01-01'
    month = endate[:8] + '01'
    # weeknum = datetime.datetime.strptime(self.endate,'%Y-%m-%d')

    report = WeeklyReportSummary(old_start_date, cg_start_date, endate)
    old_purse = report.old_coin_purse()
    old_fixed_invest, old_commulate, commlabel = report.old_fixed()
    cg_fixed = report.cg_fixed()
    cg_current = report.cg_current()
    cg_chuxin_plan = report.cg_chuxin_plan()
    cg_new_reginvest, cg_statnum, cg_statlabel = report.cg_other_statistic()

    mytool = MyPath()
    path = mytool.path
    cg_report = to_timeseries(cg_start_date, endate, cg_fixed, cg_current, cg_chuxin_plan)
    cg_report.to_csv(path + '\cg_data.csv', header=True, index=False)

    old_app = to_timeseries(old_start_date, endate, old_purse, old_fixed_invest)
    old_app.to_csv(path + '\old_app_data.csv', header=True, index=False)

    cg_new_reginvest.to_csv(path + '\cg_new_reginvest.csv', header=True, index=False)

    mytool.to_csv('cg_statistic', [cg_statnum], cg_statlabel)
    mytool.to_csv('old_app_begin_commulate_data', [old_commulate], commlabel)

    print('All weekly data extract finished.')
