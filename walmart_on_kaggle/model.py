import os
import pandas as pd
import numpy as np
import math
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

os.chdir(r'E:\working\Python\Project\Walmart')
features = pd.read_csv('features.csv')
stores = pd.read_csv('stores.csv')
datesales = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

features.Date = features.Date.astype('datetime64')
datesales.Date = datesales.Date.astype('datetime64')
test.Date = test.Date.astype('datetime64')

data = pd.merge(features, stores, on='Store', how='left')
dumplabel = LabelEncoder()
data.Type = dumplabel.fit_transform(data.Type)
'''
columns in data:['Store', 'Date', 'Temperature', 'Fuel_Price', 'MarkDown1', 'MarkDown2',
                 'MarkDown3', 'MarkDown4', 'MarkDown5', 'CPI', 'Unemployment',
                 'IsHoliday', 'Type', 'Size']
                 
columns in datesales:['Store', 'Dept', 'Date', 'Weekly_Sales', 'IsHoliday']
'''
#may need to add a column illustrating the week before or after these holiday weeks
super_bowl = ['2010-02-12', '2011-02-11', '2012-02-10', '2013-02-08']
Labor = ['2010-09-10', '2011-09-09', '2012-09-07', '2013-09-06']
Thksgiving = ['2010-11-26', '2011-11-25', '2012-11-23', '2013-11-29']
Christmas = ['2010-12-31', '2011-12-30', '2012-12-28', '2013-12-27']

def nan_to_0(num):
    if math.isnan(num):
        num = 0
    return num

bool_to_int = lambda x:int(x)

storeNO = np.unique(data.Store)
for i in storeNO:
    exec('store%d = pd.merge(\
    data[data.Store == i].drop("IsHoliday", axis=1), \
    datesales[datesales.Store == i], on=["Store", "Date"], how="right")' % i)
    for j in range(1, 6):
        exec('store%d.MarkDown%d = store%d.MarkDown%d.apply(nan_to_0)' % (i, j, i, j))
#    exec('store%d.IsHoliday = store%d.IsHoliday.apply(bool_to_int)' % (i, i))

allstore = pd.DataFrame()
for i in storeNO:
    exec('allstore = pd.concat([allstore, store%d], axis=0)' % i)

#note that every store.Date ranges from 2010-02-05 to 2012-11-01
'''
columns in store:['Store', 'Date', 'Temperature', 'Fuel_Price', 'MarkDown1', 'MarkDown2',
            	  'MarkDown3', 'MarkDown4', 'MarkDown5', 'CPI', 'Unemployment', 'Type',
	    		  'Size', 'Dept', 'Weekly_Sales', 'IsHoliday']
'''

#building recession model:
trainstore = allstore.drop(['Store', 'Date', 'Weekly_Sales'], axis=1)
y_train = allstore.Weekly_Sales
teststore = pd.merge(test, data.drop('IsHoliday', axis=1), how='left', on=['Store', 'Date'])
teststore = teststore.drop(['Store', 'Date'], axis=1)
teststore = teststore.reindex(columns=trainstore.columns)
trainstore = xgb.DMatrix(trainstore, label=y_train)
teststore = xgb.DMatrix(teststore)

params={'booster':'gbtree',
	    'objective': "reg:linear",
	    'eval_metric':'mae',
	    'gamma':0.1,
	    'min_child_weight':1.1,
	    'max_depth':8,
	    'lambda':2,
	    'subsample':0.7,
	    'colsample_bytree':0.5,
	    'colsample_bylevel':1,
	    'eta': 0.01,
	    'tree_method':'exact',
	    'seed':0,
	    'nthread':4
	    }

watchlist = [(trainstore, 'train')]
model = xgb.train(params, trainstore, num_boost_round=1000, evals=watchlist)
y_test = model.predict(teststore)

test.Date = test.Date.astype('str')
test.Dept = test.Dept.astype('str')
test.Store = test.Store.astype('str')
output_col = test.Store + '_' + test.Dept + '_' + test.Date
output = pd.DataFrame([output_col, y_test], index=['Id', 'Weekly_Sales']).T
output.to_csv('Submission.csv', index=None)