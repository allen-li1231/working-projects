"""
@Author: Allen Lee       2018-01-24
"""
import pandas as pd
import matplotlib.pyplot as plt
from compile.my_class import sql_connection, to_timeseries
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.tsa.arima_model import ARIMA

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


cur = sql_connection()
sql_withdraw_apply = '''SELECT date(a.create_time),sum(a.arrival_amount)
                FROM cg_withdraw_apply a
                left join t_bus_user u on a.user_name=u.user_name
                left join t_bus_user_basic_info b on a.user_name=b.user_name
                WHERE disabled = 0
                AND bus_sataus = 1
                /*AND date(a.create_time)>='2017-10-19' 
                AND date(a.create_time)<='2017-10-19'*/
                group by date(a.create_time)
                ORDER BY a.create_time ASC'''

sql_withdraw_success = '''SELECT date(a.transaction_time),sum(a.arrival_amount)
                FROM cg_withdraw_apply a
                left join t_bus_user u on a.user_name=u.user_name
                left join t_bus_user_basic_info b on a.user_name=b.user_name
                WHERE disabled = 0
                AND bus_sataus = 1
                /*AND date(a.transaction_time)>='2017-10-19' 
                AND date(a.transaction_time)<='2017-10-19'*/
                group by date(a.transaction_time)
                ORDER BY a.transaction_time ASC'''

sql_withdrawable = '''select DATE(create_time),sum(current_amount)
                from cg_user_capital_account_detail where id in(
                select max(id)
                from cg_user_capital_account_detail
                GROUP BY date(create_time),user_name
                )
                GROUP BY DATE(create_time);'''



cur.execute(sql_withdraw_success)
cg_withdraw = pd.DataFrame(list(cur.fetchall()), columns=['date', 'withdraw'])
cur.execute(sql_withdrawable)
cg_withdrawable = pd.DataFrame(list(cur.fetchall()), columns=['date', 'withdrawable'])
cur.close()

cg_withdraw.to_csv(r'E:\Trustsaving\Python\retain_fund_predict\raw_data\cg_withdraw.csv', index=False)
cg_withdrawable.to_csv(r'E:\Trustsaving\Python\retain_fund_predict\raw_data\cg_withdrawable.csv', index=False)
withdraw = to_timeseries('2017-11-20', '2018-01-21', cg_withdraw, cg_withdrawable)


#####################################
#drop white noise, dimention interference:
withdraw.index = withdraw.date
withdraw.drop('date', axis=1, inplace=True)
#withdraw.loc['2018-01-08', 'withdraw'] = 1394326.78
withdraw.loc['2018-01-09', 'withdraw'] = 1394326.78
withdraw.loc[:, 'withdraw_rate'] = withdraw.withdraw / withdraw.withdrawable
withdraw.plot()
withdraw_rate = withdraw.loc[:, 'withdraw_rate']
withdraw_rate.plot()


#####################################
#drop data with no reference value:
withdraw_rate.drop(withdraw_rate.index[withdraw_rate == 0], inplace=True)
drop_test = withdraw_rate.index[(withdraw_rate.index >= '2017-12-25') & (withdraw_rate.index <= '2018-01-07')]
withdraw_rate.drop(drop_test, inplace=True)
fake_idx = pd.date_range(end='2018-01-21', periods=withdraw_rate.shape[0])
withdraw_rate.reset_index(drop=True)
withdraw_rate.index = fake_idx


#####################################
#introducing ARIMA model:
plot_acf(withdraw_rate).show()

acorr_ljungbox(withdraw_rate, lags=1)

ADF(withdraw_rate)
pmax = int(len(withdraw_rate)/10)
qmax = int(len(withdraw_rate)/10)

#adjust parameters:
bic_matrix = []
for p in range(pmax+1):
    tmp = []
    for q in range(qmax+1):
        try:
            tmp.append(ARIMA(withdraw_rate, (p, 1, q)).fit().bic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix)
p, q = bic_matrix.stack().idxmin()
#p=6, q=0


model = ARIMA(withdraw_rate, (p, 1, q)).fit()
model.summary()

model.forecast(7)

'''446338.8958668 ,  447178.72828716,  448018.56070751,
         448858.39312786,  449698.22554822'''