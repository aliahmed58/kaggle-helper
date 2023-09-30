""" Utils file that contains necessary methods used in data preprocessing and fitting models """

import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, RepeatedKFold, GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.feature_selection import SequentialFeatureSelector
import numpy as np

def drop_columns(df: pd.DataFrame, *columns):
    """
    Drop given columns 
    Args:
        df (pd.DataFrame): _description_
    """
    df.drop(list(columns), axis=1, inplace=True)


def impute_numericals(df: pd.DataFrame, strategy: str):
    """Impute numerical columns using a given strategy, also filters categorical columns from numerical columns

    Args:
        df (pd.DataFrame): the data frame object
        strategy (str): strategy of imputing i.e mean, mode, knn etc
    """
    # get numerical columns from the data frame exclude the columns which have unique values less than 10
    numerical_columns = df.select_dtypes(include='number').columns
    
    # remove columns that have less than 10 unique values and impute if strategy is mean
    for col in numerical_columns:
        if len(df[col].unique()) < 6:
            numerical_columns = numerical_columns.drop(col)
        else:
            if strategy == 'mean':
                df[col].fillna(df[col].median(), inplace=True)
    
    # if strategy is knn use a KNN Imputer
    if strategy == 'knn':
        knn_imputer = KNNImputer(n_neighbors=2001)
        knn_imputer = knn_imputer.fit(df[numerical_columns].values)
        df[numerical_columns] = knn_imputer.transform(df[numerical_columns].values)
        

def impute_categoricals(df: pd.DataFrame):
    """Impute categorical columns of type object using mode

    Args:
        df (pd.DataFrame): the python data frame that has to be imputed
    """
    # check for columns with type object or less than 10 unique values and impute missing values using mode
    for col in df.columns:
        if df[col].dtype == object or len(df[col].unique()) < 6:
            df[col].fillna(df[col].mode()[0], inplace=True)


def scale_numericals(df: pd.DataFrame, strategy: str):
    # get numerical columns from the data frame exclude the columns which have unique values less than 10
    numerical_columns = df.select_dtypes(include='number').columns
    
    for col in numerical_columns:
        if len(df[col].unique()) < 6:
            numerical_columns = numerical_columns.drop(col)
            
    if strategy == 'minmax':
        mms = MinMaxScaler()
        df[numerical_columns] = mms.fit_transform(df[numerical_columns])
    elif strategy == 'standard':
        std_scaler = StandardScaler()
        df[numerical_columns] = std_scaler.fit_transform(df[numerical_columns])


def encode_dataset(df: pd.DataFrame, strategy: str) -> pd.DataFrame:

    if strategy == 'one_hot':
        object_cols = df.select_dtypes(include='object').columns
        df = pd.get_dummies(df, prefix='isin', prefix_sep='_', columns=list(object_cols), drop_first=False, dtype=np.uint8)
    
    if strategy == 'label':
        pass

    return df

def select_features(X, Y, n_features, model) -> list:
    """Returns the best features for a given model 

    Args:
        X (_type_): train data set X values (rest columns)
        Y (_type_): train data set Y values (hopsital_death)
        n_features (_type_): best no. of features
        model (_type_): model object 

    Returns:
        list: list of column names that are selected
    """
    sfs = SequentialFeatureSelector(model, direction='forward',n_features_to_select=n_features, scoring='roc_auc')
    sfs.fit(X, Y)
    return list(sfs.get_feature_names_out())

# method to fit the model
def fit_model(X, Y, model, model_name):
    """
    Fit the model on given training data set
    Args:
        X (_type_): X values
        Y (_type_): Y values (hospital death)
        model (_type_): model object
        model_name (_type_): string of model name

    Returns:
        _type_: model object 
    """
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.3)
    # pass train x 
    model.fit(trainX, trainY)
    # get the probabilities
    md_probs = model.predict_proba(testX)
    # change array shape
    md_probs = md_probs[:,1]
    # calcualte score
    md_auc = roc_auc_score(testY, md_probs)
    
    print(model_name, " : ", md_auc)
    
    return model

def predict(test_df: pd.DataFrame, model):
    """
    Predict on test data set
    Args:
        test_df (pd.DataFrame): the test data frame
        model (_type_): the model that is fitted

    Returns:
        _type_: array of probabilites 
    """
    probs = model.predict_proba(test_df)
    
    probs = probs[:,1]
    
    return probs


def grid_search(params, model, X, Y):
    """

    Args:
        params (_type_): dictionary of parameter
        model (_type_): _description_
        X (_type_): _description_
        Y (_type_): _description_

    Returns:
        _type_: _description_
    """
    cv = RepeatedKFold(n_splits=10, n_repeats=1)#, random_state=1)
    grid_search = GridSearchCV(model, params, cv=cv, n_jobs=-1, scoring='roc_auc',verbose=2)#, refit=False)
    grid_search.fit(X, Y)
    print(grid_search.best_estimator_)
    print(grid_search.best_score_)
    print(grid_search.best_params_)
    
    return grid_search.best_params_
    