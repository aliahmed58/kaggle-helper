import utils
import pandas as pd
from sklearn.tree import ExtraTreeClassifier, DecisionTreeClassifier, ExtraTreeRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, RepeatedKFold, GridSearchCV, cross_val_score
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.feature_selection import SequentialFeatureSelector, SelectKBest, f_classif
from sklearn.preprocessing import MinMaxScaler
import config
import submitter
import os

# loading datasets
train_df = pd.read_csv('data/train.csv')
test_df = pd.read_csv('data/test.csv')

# record ids from test data set
record_ids = test_df['RecordID']

# Y value hopsital deatb
Y = train_df['hospital_death']

# drop unneccesary columns
utils.drop_columns(train_df, 'RecordID', 'hospital_id', 'hospital_death', 'icu_id','ethnicity','gender','icu_admit_source',
                   'icu_stay_type','icu_type', 'hospital_death')
utils.drop_columns(test_df, 'RecordID', 'hospital_id', 'icu_id','ethnicity','gender','icu_admit_source','icu_stay_type','icu_type',
                   )

# imputing numericals
utils.impute_numericals(train_df, config.NUMERICAL_IMPUTATION)
utils.impute_numericals(test_df, config.NUMERICAL_IMPUTATION)

# imputing categoricals
utils.impute_categoricals(train_df)
utils.impute_categoricals(test_df)

utils.scale_numericals(train_df, config.SCALING)
utils.scale_numericals(test_df, config.SCALING)

train_df = utils.encode_dataset(train_df, config.ENCODING)
test_df = utils.encode_dataset(test_df, config.ENCODING)

# X data frame
X = train_df

if config.FORWARD_FEATURING:
    best_features = list(utils.select_features(X, Y, config.BEST_FEATURES, model=config.MODEL))
    print(best_features)
    X = train_df[best_features]
    test_df = test_df[best_features]
    
best_params = ''
if config.GRID_SEARCH: 
    best_params = utils.grid_search(config.GRID_SEARCH_PARAMS, config.MODEL, X, Y)

    config.MODEL = config.MODEL.set_params(**best_params)

print(config.MODEL.get_params())

config.MODEL = utils.fit_model(X, Y, config.MODEL, 'Model Ran: ')

probs = utils.predict(test_df, config.MODEL)

output = pd.DataFrame()

output['RecordID'] = record_ids
output['hospital_death'] = probs

# create output folder if does not exist
if not os.path.exists('./out'):
    os.mkdir('./out')

output.to_csv(config.OUTPUT_FILE_NAME, index=False)

# get configs
config_str = config.get_configs(best_params)

print(config_str)

if config.SUBMIT_TO_KAGGLE_GOOGLE:
    submitter.make_submission(config.COMPETITION_NAME, './out/output.csv', config_str)