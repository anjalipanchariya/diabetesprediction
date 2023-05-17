import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pickle

# data = pd.read_csv("Diab_pyth_data.csv")

# data = data.dropna(subset=['Glucose Before fasting', 'Glucose Anytime', 'BMI', 'Blood Pressure',
#                            'Age', 'Sex', 'Family member with Diabetes past or present', 'Pregnancies'], how='any')
# # print(data.isnull().sum(axis=0))
# # print(data.shape)
# le = preprocessing.LabelEncoder()
# data['Sex'] = le.fit_transform(data.Sex.values)

# X = data.iloc[:, :8]
# Y = data.iloc[:, 8:]
# X_train, X_test, Y_train, Y_test = train_test_split(
#     X, Y, train_size=0.7, test_size=0.3)

# regressor = LinearRegression()
# regressor.fit(X_train, Y_train)
# y_pred = regressor.predict(X_test)
# filename = 'model.sav'
# pickle.dump(regressor, open(filename, 'wb'))
# print(r2_score(Y_test, y_pred))

# y = regressor.predict([[123, 123, 25, 0, 1, 0, 20, 1]])
# print(y)

# def predict(a,b,c,d,e,f,g,h):
#   loaded_model = pickle.load(open(filename, 'rb'))
#   y = loaded_model.predict([[a,b,c,d,e,f,g,h]])
#   print(y)

def predict(pre, post, bmi, bp, age, gender, family, preg):
			loaded_model = pickle.load(open('model.sav', 'rb'))
			y = loaded_model.predict([[pre, post, bmi, bp, age, gender, family, preg]])
			return y[0][0]

print(predict(123, 123, 25, 0, 1, 0, 20, 1))
