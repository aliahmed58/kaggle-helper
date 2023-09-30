from sklearn.tree import ExtraTreeClassifier, DecisionTreeClassifier, ExtraTreeRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


NUMERICAL_IMPUTATION = 'mean' # knn or mean
CATEGORICAL_IMPUTAITON = 'mode' #
ENCODING = 'one_hot' 
SCALING = 'minmax' # standard or minmax
FORWARD_FEATURING = True 
BEST_FEATURES = 15 # if forward_featuring = true

# MODEL = KNeighborsClassifier(n_neighbors=91)
MODEL = DecisionTreeClassifier(max_depth=7, min_samples_split=10)
# MODEL = GaussianNB()
MODEL_NAME = 'Decision Tree Classifier'

TREE_PARAMS_GRID_SEARCH = {
    'max_depth': [3, 4, 5, 6, 7, 8, 9],
    'min_samples_split': [1, 2, 3, 5, 7, 8, 9, 11]
}

# TREE_PARAMS_GRID_SEARCH = {
#     'n_neighbors': [11, 21, 45, 61, 91],
# }

OUTPUT_FILE_NAME = './out/output.csv'
SUBMIT_TO_KAGGLE = False

def get_configs(params) -> str:
    config_str = f'Model used: {MODEL_NAME} {params} \nNumerical Imputation using {NUMERICAL_IMPUTATION}\nCategorical Imputation using {CATEGORICAL_IMPUTAITON} \nCategorical encoding using {ENCODING}\nScaling method: {SCALING}\n'
        
    if FORWARD_FEATURING:
        config_str = config_str + f'Forward Featuring used to select best {BEST_FEATURES} features'
        
    return config_str