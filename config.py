from sklearn.tree import ExtraTreeClassifier, DecisionTreeClassifier, ExtraTreeRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from catboost import CatBoostClassifier


NUMERICAL_IMPUTATION = 'mean' # knn or mean
CATEGORICAL_IMPUTAITON = 'mode' #
ENCODING = 'one_hot' 
SCALING = 'standard' # standard or minmax
FORWARD_FEATURING = False 
BEST_FEATURES = 15 # if forward_featuring = true

MODEL = CatBoostClassifier()

TREE_PARAMS_GRID_SEARCH = {
    'max_depth': [3, 4, 5, 6, 7, 8, 9],
    'min_samples_split': [1, 2, 3, 5, 7, 8, 9, 11]
}

# TREE_PARAMS_GRID_SEARCH = {
#     'n_neighbors': [11, 21, 45, 61, 91],
# }

OUTPUT_FILE_NAME = './out/output.csv'

SUBMIT_TO_KAGGLE_GOOGLE = True
COMPETITION_NAME = 'iml-fall-2023-first-challenge'

"""
********* Options below are for google form submission *********
"""

"""
Options 'Random Forest', 'Gradient Boosting', 'Adaptive Boosting', 'Light GBM', 'XGBoost', 'CatBoost'
'BaggingClassifier', 'other' (CASE SENSITIVE)
"""
MODEL_NAME = 'CatBoost' 

email = ''
erp = ''
kaggle_username = ''
parameter_specification = 'default'

"""
Additional notes (leave blank if nothing)
"""
additional_notes = ''

"""
Data cleaning techniques
Comment out the ones not needed
"""
data_cleaning_techniques = [
    'One-hot encoding', 
    'Scaling/Normalisation', 
    # 'Feature Importance',
    # 'Forward/Backward Selection',
    # 'Label Encoding'
    ]

"""
How missing values were handled
Comment out the values not needed
"""
missing_values_handled = [
    # 'Removed',
    'Simple Imputation',
    # 'KNN Imputation',
    # 'None'
]


def get_configs(params) -> str:
    config_str = f'Model used: {MODEL_NAME} {params} || Numerical Imputation using {NUMERICAL_IMPUTATION} || Categorical Imputation using {CATEGORICAL_IMPUTAITON} || Categorical encoding using {ENCODING} || Scaling method: {SCALING} ||'
        
    if FORWARD_FEATURING:
        config_str = config_str + f'Forward Featuring used to select best {BEST_FEATURES} features'
        
    return config_str