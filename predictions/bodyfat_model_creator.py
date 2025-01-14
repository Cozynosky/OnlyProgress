import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statistics

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

# conf plot
plt.style.use('fivethirtyeight')
colors=['#ffcd94','#eac086','#ffad60','#ffe39f']
sns.set_palette(sns.color_palette(colors))

# read data
data = pd.read_csv("static/data/datasets/bodyfat.csv")

z_data = np.abs(stats.zscore(data))
data_clean = data[(z_data<3).all(axis=1)]

# show pre cleaned data
plt.figure(figsize=(20,10), facecolor='white')
sns.boxplot(data=data)
plt.grid()
plt.show()

# show cleaned data
plt.figure(figsize=(20,7), facecolor='white')
sns.boxplot(data=data_clean)
plt.grid()
plt.show()




X = data_clean.drop(['BodyFat','Density'],axis=1)
X['Bmi']=703 * X['Weight']/(X['Height']*X['Height'])
X['ACratio'] = X['Abdomen']/X['Chest']
X['HTratio'] = X['Hip']/X['Thigh']
#X.drop(['Weight','Height','Abdomen','Chest','Hip','Thigh'],axis=1,inplace=True)

y = data_clean['Density']


X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42)

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
svr= SVR()
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
    
y_pred = ridge.predict(X_test)
sns.scatterplot(x=y_test,y=y_pred)
plt.plot([1.02, 1.10], [1.02, 1.10], color = 'black',linestyle='--',linewidth=1)
plt.xlabel("Actual Density (gm/cm^3)")
plt.ylabel("Predicted Density (gm/cm^3)")
plt.title("Actual Vs Predicted")
plt.show()

y_pred = ridge.predict(X_test)

def density_to_bf(density):
    return ((4.95/density) - 4.5)*100

expected = list(map(density_to_bf, list(y_test)))
recieved = list(map(density_to_bf, list(y_pred)))

for i in range(10):
    print(f"Expected: {round(expected[i],2)} -> Recieved: {round(recieved[i],2)}")

diffs = [ abs(expected[i] - recieved[i]) for i in range(len(expected))]
print(f"min {min(diffs)} max {max(diffs)} mean {statistics.mean(diffs)}")

# import pickle
# pickle.dump(trans,open('static/data/transformer.pkl','wb'))
# pickle.dump(ridge,open('static/data/model.pkl','wb'))