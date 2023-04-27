import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from sklearn.preprocessing import PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression , ElasticNet , Lasso , Ridge
from sklearn.metrics import r2_score
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from lightgbm import LGBMRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split


plt.style.use('fivethirtyeight')
colors=['#ffcd94','#eac086','#ffad60','#ffe39f']
sns.set_palette(sns.color_palette(colors))

data = pd.read_csv("data/bodyfat.csv")


X = data.drop(['BodyFat','Density'],axis=1)
X['Bmi']=703 * X['Weight']/(X['Height']*X['Height'])
X['ACratio'] = X['Abdomen']/X['Chest']
X['HTratio'] = X['Hip']/X['Thigh']
#X.drop(['Weight','Height','Abdomen','Chest','Hip','Thigh'],axis=1,inplace=True)

y = data['Density']
#print(X.iloc[1], "\nDensity", y.iloc[1], "\nBf", data["BodyFat"].iloc[1]) 

z = np.abs(stats.zscore(X))

#only keep rows in dataframe with all z-scores less than absolute value of 3 
X_clean = X[(z<3).all(axis=1)]
y_clean = y[(z<3).all(axis=1)]

X_train,X_test,y_train,y_test = train_test_split(X_clean,y_clean,random_state=42)

trans = PowerTransformer()
X_train = trans.fit_transform(X_train)
X_test = trans.transform(X_test)

kernel = KernelRidge()
lgbm = LGBMRegressor()
random = RandomForestRegressor()
linear = LinearRegression()
elastic = ElasticNet()
lasso  = Lasso()
ridge = Ridge()
svr=SVR()
grad = GradientBoostingRegressor()
sgd = SGDRegressor()
bay = BayesianRidge()
clf = [linear,elastic,lasso,ridge,svr,grad,sgd,bay,random,kernel,lgbm]
hashmap={}

def compute(model):
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    r2=r2_score(y_test,y_pred)
    rmse=np.sqrt(mean_squared_error(y_test,y_pred))
    hashmap[str(model)]=(r2,rmse)

for i in clf:
    compute(i)

score=pd.DataFrame(hashmap)
score = score.transpose()
score.columns=['R2_score','RMSE']
score = score.sort_values('R2_score',ascending=False)

print(score)

def predict(values):
    density = ridge.predict(values)
    fat = ((4.95/density[0]) - 4.5)*100
    print(f'Density: {density[0]} g/cc\nPercentage Body Fat: {fat} % {y_test.iloc[1]}\n')

import pickle
pickle.dump(trans,open('transformer.pkl','wb'))
pickle.dump(ridge,open('model.pkl','wb'))

y_pred = ridge.predict(X_test)

def density_to_bf(density):
    return ((4.95/density) - 4.5)*100

expected = list(map(density_to_bf, list(y_test)))
recieved = list(map(density_to_bf, list(y_pred)))
diffs = [ abs(expected[i] - recieved[i]) for i in range(len(expected))]

print(f"min {min(diffs)} max {max(diffs)}")

# for test, pred in zip(map(density_to_bf, list(y_test)), map(density_to_bf, list(y_pred))):
#     print(f"Expected {test} => recieved {pred}")