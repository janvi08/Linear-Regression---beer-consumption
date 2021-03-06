
import numpy as np 
import pandas as pd 

import os
for dirname, _, filenames in os.walk('/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df = pd.read_csv('/kaggle/input/beer-consumption-sao-paulo/Consumo_cerveja.csv')
df=df.rename(columns={"Temperatura Media (C)": "Temp median", "Temperatura Minima (C)": "Temp min",  "Temperatura Maxima (C)": "Temp max","Precipitacao (mm)": "Precipitation", "Consumo de cerveja (litros)":"Beer in litres","Final de Semana":"Weekend" })
df.head()

#Replace all the commas with dots to make it a proper number and convert them to float

for i in df.columns[1:5]:
  df[i] = df[i].str.replace(",",".")
  df[i] = df[i].astype("float")
df.head()

#Remove null values and the Date column

df= df.dropna()
df = df.drop("Data",axis=1)
df.describe()

#Find correlation between the attributes

import seaborn as sns
sns.heatmap(df.corr(), annot = True)
df.plot.scatter(x="Weekend", y = "Beer in litres")

#Beer consumption is seen to have maximum correlation with Max Temperature. Though the beer the consumption is a little high on weekends, the beer consumption on weekdays is also good enough.

sns.pairplot(df, x_vars=['Temp max'], y_vars='Beer in litres', size=7, aspect=0.7, kind='reg')
X = df.drop("Beer in litres", axis=1)
y = df['Beer in litres']

#Split data into train data and test data

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=123)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
print("Score: {:.4f}".format(model.score(X_test, y_test)))

y_pred = model.predict(X_test)

print("Coefficient is : {}\n".format(model.coef_))
print("Intercept is : {}\n".format(model.intercept_))

cost = sum((y_pred - y_test)**2) / (2*y_pred.size)
print("Cost is : {}\n".format(cost))

from yellowbrick.regressor import PredictionError

visualizer = PredictionError(model)
visualizer.fit(X_train, y_train)  
visualizer.score(X_test, y_test)  
visualizer.show()  

#If we predict Beer consumption only based on max temperature :

X1 = df['Temp max']
y1 = df['Beer in litres']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X1, y1, train_size=0.8, random_state=123)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train.values.reshape(-1,1), y_train.values.reshape(-1,1))
print("Score: {:.4f}".format(model.score(X_test.values.reshape(-1,1), y_test.values.reshape(-1,1))))

y_pred = model.predict(X_test.values.reshape(-1,1))
print("Coefficient is : {}\n".format(model.coef_))
print("Intercept is : {}\n".format(model.intercept_))

cost = sum((y_pred - y_test.values.reshape(-1,1))**2) / (2*y_pred.size)
print("Cost is : {}\n".format(cost))
