from sklearn.tree import ExtraTreeClassifier, DecisionTreeClassifier, ExtraTreeRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


NUMERICAL_IMPUTATION = 'mean' # knn or mean
CATEGORICAL_IMPUTAITON = 'mode' #
ENCODING = 'one_hot' 
SCALING = 'minmax' # standard or minmax
FORWARD_FEATURING = False     
BEST_FEATURES = 15 # if forward_featuring = true
GRID_SEARCH = False
"""
The GRID_SEARCH_PARAMS should be a dictionary with list of parmas specific to the model
GRID_SEARCH_PARAMS = {
    'parameter_name': [... possible values of the parameter],
    'antoher_param_name': [... another possible values :D]
    'iterations': [100, 200, 300...]
}
When GRID_SEARCH = True, leave constructor params of MODEL empty
"""
GRID_SEARCH_PARAMS = {
    'iterations': [1700, 2500, 7000, 12000],
    'max_depth': [5, 7, 9],
    'learning_rate': [0.004, 0.0005]
}


MODEL = GaussianNB()


OUTPUT_FILE_NAME = './out/output.csv'

SUBMIT_TO_KAGGLE_GOOGLE = False
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
    'Feature Importance',
    # 'Forward/Backward Selection',
    # 'Label Encoding',
    'Principal Component Analysis'
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