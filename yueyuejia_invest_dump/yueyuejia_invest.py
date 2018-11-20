import pandas as pd
import datetime
from compile.my_class import sql_connection, MyDate

mytool = MyDate()
cur = sql_connection()
sql_yueyuejia_invest = \
    """
    select date(tbm.create_date),u.mobile_no,tbm.basic_lock_month,tbm.amount
    from t_bus_match_link_invest tbm
    left join t_bus_user u on u.user_name=tbm.user_name
    where (date(tbm.clearing_date)>%s
    or tbm.clearing_date is null)
    and status=159002
    and u.role_id in ('ordinary','counselor')
    ;"""

last_month_floor = mytool.last_month_floor
last_month_ceil = mytool.last_month_ceil
this_month = last_month_ceil.strftime('%Y-%m-%d')

cur.execute(sql_yueyuejia_invest, this_month)
yueyuejia_invest = pd.DataFrame(list(cur.fetchall()), columns=['date', 'mobile_no', 'basic_lock_month', 'amount'])
cur.close()

mindate = yueyuejia_invest.date.min()
max_iter = int((last_month_floor - mindate).days/30)
last_month_investor = pd.DataFrame()
month_range = datetime.timedelta(30)

# formular: create_time + (basic_lock_month*30n) = [2017.1.1-2017.1.31]
for i, row in enumerate(yueyuejia_invest.values):
    for t in range(max_iter+1):
        if (row[0] + row[2]*month_range*t >= last_month_floor) and (row[0] + row[2]*month_range*t <= last_month_ceil):
            last_month_investor = last_month_investor.append(yueyuejia_invest.iloc[i, :])

last_month_investor.to_csv("last_month_investor.csv", index=False)


for iow in last_month_investor.itertuples():
    print(type(iow.amount))
    last_month_investor.append(iow)
