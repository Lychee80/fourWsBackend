from sklearn.linear_model import LinearRegression
import random

feature_set = []
target_set = []

# 200 rows of data
number_of_rows = 200
random_number_limit = 2000

for i in range(0, number_of_rows):
    x= random.randint(0, random_number_limit)
    y= random.randint(0, random_number_limit)
    z= random.randint(0, random_number_limit)

    # linear function
    function = (10*x)+(2*y)+(3*z)

    feature_set.append([x,y,z])
    target_set.append(function)

# linear regression model
model = LinearRegression()
model.fit(feature_set, target_set)

# create test data set
# expected output is (10*8) + (2*10) + (3*0) = 100
test_set = [[8, 10, 0]] 
prediction = model.predict(test_set)

print("Prediction:" + str(prediction) + "Coefficients:" + str(model.coef_))
# it predicted it!