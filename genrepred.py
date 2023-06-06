import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
data = pd.read_csv("responses.csv")
data.head()

# Add Target Variables
df = data.iloc[:,0:19]
# Add Predictor Variables
df["Age"] = data["Age"]
df["Height"] = data["Height"]
df["Weight"] = data["Weight"]
df["Siblings"] = data["Number of siblings"]
df["Gender"] = data["Gender"]
df["Education"] = data["Education"]
df["Location"] = data["Village - town"]

# Git rid of rows with null data
df.dropna(inplace = True)
df.reset_index(drop=True,inplace=True)

# Change column types to int
for each in range(0,26) :
    if type(df.iloc[1,each]) == np.float64 :
        df[df.columns[each]] = df[df.columns[each]].astype(int)
    else :
        df[df.columns[each]] = df[df.columns[each]]

# Remove all rows with people who said they liked music 3 or less
filtre = df.Music < 4
filt_list = list(df[filtre].index)
i=0
for each in filt_list:
    df.drop(df.index[each-i], inplace=True)
    i=i+1
df.reset_index(drop=True,inplace=True)
row = len(df.index)

# Get rid of music col because its not predictor nor target
df.drop(['Music'], axis=1,inplace = True)

# Treating  categorical variables
# let education be represented as 0,1,2,...
for education in range(0,row) :
    if df.loc[education,'Education'] == 'currently a primary school pupil' :
        df.loc[education,'Education'] = 0
    elif df.loc[education,'Education'] == 'primary school':
        df.loc[education,'Education'] = 1
    elif df.loc[education,'Education'] == 'secondary school':
        df.loc[education,'Education'] = 2
    elif df.loc[education,'Education'] == 'college/bachelor degree':
        df.loc[education,'Education'] = 3
    elif df.loc[education,'Education'] == 'masters degree':
        df.loc[education,'Education'] = 4
    elif df.loc[education,'Education'] == 'doctorate degree':
        df.loc[education,'Education'] = 5
    # in case i missed any
    else :
        df.loc[education,'Education'] = 6
df['Education'] = df['Education'].astype(int)
# let gender and location be represented in one column as 0 or 1
dummies1 = pd.get_dummies(df.Gender, dtype=int)
dummies2 = pd.get_dummies(df.Location, dtype=int)
df = pd.concat([df, dummies1, dummies2], axis='columns')
df.drop(['Gender','Location'], axis='columns',inplace = True)
df['Gender'] = df['female']
df['Location'] = df['city']
df.drop(['female', 'male', 'city', 'village'], axis='columns',inplace = True)

# Change each rating to 0-1 by dividing by 5
for target in df.columns[:18]:
    df[target] = df.apply(lambda row : row[target]/5, axis = 1)

# Separate train and test sets
# Separate Target Variable and Predictor Variables
TargetVariable=df.columns[:18]
Predictors=df.columns[18:]

X=df[Predictors].values
y=df[TargetVariable].values

### Sandardization of data ###
from sklearn.preprocessing import StandardScaler
PredictorScaler=StandardScaler()
TargetVarScaler=StandardScaler()

# Storing the fit object for later reference
PredictorScalerFit=PredictorScaler.fit(X)
TargetVarScalerFit=TargetVarScaler.fit(y)

# Generating the standardized values of X and y
X=PredictorScalerFit.transform(X)
y=TargetVarScalerFit.transform(y)

# Split the data into training and testing set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=69420)

# Hyperparameter tuning if needed
## hyperparameter tuning: dont run
run = False
if run:
    # Function to generate Deep ANN model 
    def make_regression_ann(Optimizer_trial):
        from keras.models import Sequential
        from keras.layers import Dense
        
        model = Sequential()
        model.add(Dense(units=64, input_dim=7, kernel_initializer='normal', activation='relu'))
        model.add(Dense(units=64, kernel_initializer='normal', activation='tanh'))
        model.add(Dense(units=64, kernel_initializer='normal', activation='relu'))
        model.add(Dense(18, kernel_initializer='normal'))
        model.compile(loss='mean_squared_error', optimizer=Optimizer_trial)
        return model

    ###########################################
    from sklearn.model_selection import GridSearchCV
    from keras.wrappers.scikit_learn import KerasRegressor

    # Listing all the parameters to try
    Parameter_Trials={'batch_size':[16,32,64,128,256,512],
                        'epochs':[5,10,20,50,100],
                        'Optimizer_trial':['adam', 'rmsprop']
                    }

    # Creating the regression ANN model
    RegModel=KerasRegressor(make_regression_ann, verbose=0)

    ###########################################
    from sklearn.metrics import make_scorer

    # Defining a custom function to calculate accuracy
    def Accuracy_Score(orig,pred):
        MAPE = np.mean(100 * (np.abs(orig-pred)/orig))
        print('#'*70,'Accuracy:', 100-MAPE)
        return(100-MAPE)

    custom_Scoring=make_scorer(Accuracy_Score, greater_is_better=True)

    #########################################
    # Creating the Grid search space
    # See different scoring methods by using sklearn.metrics.SCORERS.keys()
    grid_search=GridSearchCV(estimator=RegModel, 
                            param_grid=Parameter_Trials, 
                            scoring=custom_Scoring, 
                            cv=5)

    #########################################
    # Measuring how much time it took to find the best params
    import time
    StartTime=time.time()

    # Running Grid Search for different paramenters
    grid_search.fit(X,y, verbose=1)

    EndTime=time.time()
    print("########## Total Time Taken: ", round((EndTime-StartTime)/60), 'Minutes')

    print('### Printing Best parameters ###')
    grid_search.best_params_

# Training and testing the neural network
# importing the libraries
from keras.models import Sequential
from keras.layers import Dense, Dropout
 
# create ANN model
model = Sequential()

# Dropout layer
model.add(Dropout(0.2, input_shape=(7,)))

# Defining the Input layer and FIRST hidden layer, both are same!
model.add(Dense(units=64, input_dim=7, kernel_initializer='normal', activation='relu'))
 
# Defining the Second layer of the model
# after the first layer we don't have to specify input_dim as keras configure it automatically
model.add(Dense(units=64, kernel_initializer='normal', activation='tanh'))

# Third layer
model.add(Dense(units=64, kernel_initializer='normal', activation='relu'))
 
# The output neuron is a single fully connected node 
model.add(Dense(18, kernel_initializer='normal'))
 
# Compiling the model
model.compile(loss='mean_squared_error', optimizer='adam')
 
# Fitting the ANN to the Training set
model.fit(X_train, y_train ,batch_size = 512, epochs = 5, verbose=1)

## Saving model
model.save("genrepredmodel")

# Generating Predictions on testing data
Predictions=model.predict(X_test)
 
# Scaling the predicted Price data back to original price scale
Predictions=TargetVarScalerFit.inverse_transform(Predictions)
 
# Scaling the y_test Price data back to original price scale
y_test_orig=TargetVarScalerFit.inverse_transform(y_test)
 
# Scaling the test data back to original scale
Test_Data=PredictorScalerFit.inverse_transform(X_test)
 
TestingData=pd.DataFrame(data=Test_Data, columns=Predictors)
TestingData[df.columns[:18]]=y_test_orig
PredNames = ['Predicted ' + target for target in df.columns[:18]]
TestingData[PredNames]=Predictions

# Computing the absolute percent error
APEs = []
for col in df.columns[:18]:
    APE = 100*(abs(TestingData[col]-TestingData['Predicted ' + col])/TestingData[col])
    APEs.append(APE)
    TestingData[col + ' APE'] = APE
 
print('The Accuracy of ANN model is:', 100-np.mean(APEs))
TestingData.head()