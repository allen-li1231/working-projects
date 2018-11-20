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
sql_chuxin_invest = """
    SELECT DATE(d.invest_date),SUM(d.invest_amount) FROM cg_user_chuxin_plan_detail d
    WHERE d.disabled=0
    AND d.invest_flag=1
    GROUP BY DATE(d.invest_date);"""
sql_chuxin_withdraw = """
    SELECT DATE(p.quite_time),SUM(d.invest_amount) FROM cg_user_chuxin_plan_detail d
    LEFT JOIN cg_user_chuxin_planinfo p ON d.planinfo_id=p.id
    WHERE d.disabled=0
    AND d.invest_flag=1
    AND p.is_quite=1
    GROUP BY DATE(p.quite_time);"""

cur.execute(sql_chuxin_invest)
cx_inv = cur.fetchall()
cur.execute(sql_chuxin_withdraw)
cx_wd = cur.fetchall()
cur.close()

cx_inv = pd.DataFrame(list(cx_inv), columns=['date', 'invest'])
cx_wd = pd.DataFrame(list(cx_wd), columns=['date', 'withdraw'])

cx = to_timeseries('2017-12-01', '2018-03-22', cx_inv, cx_wd)
cx = cx.assign(vol=lambda x: x.invest-x.withdraw)

cx_inv.invest = cx_inv.invest.astype('float')
cx_wd.withdraw = cx_wd.withdraw.astype('float')
cx_inv.plot()
cx_wd.plot()


#####################################
#introducing ARIMA model:
cx.set_index('date', inplace=True, drop=True)
cx = cx.loc[:, 'vol']
plot_acf(cx).show()
#返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore

acorr_ljungbox(cx, lags=3)

ADF(cx)
pmax = int(len(cx)/10)
qmax = int(len(cx)/10)

#adjust parameters:
bic_matrix = []
for p in range(pmax+1):
    tmp = []
    for q in range(qmax+1):
        try:
            tmp.append(ARIMA(cx, (p, 0, q)).fit().bic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix)
p, q = bic_matrix.stack().idxmin()
#p=6, q=0


model = ARIMA(cx, (p, 0, q)).fit()
model.summary2()

model.forecast(7)