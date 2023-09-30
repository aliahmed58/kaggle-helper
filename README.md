# Kaggle Competition - Helper Scripts

Aim of this repository is to make util files for kaggle competitions for Intro to ML course to do the following tasks:

1. Preprocessing data such as imputation, encoding
2. Training ML models on the cleaned data
3. Outputting a csv file for kaggle submissions with descriptions of parameters used
4. Submitting a Google form for the submission details required by the instructor

## Instructions to run

1. (Recommended not necessary) Create a python virtual env using the command ```python -m venv ./venv``` from root directory
2. Install the requiremd modules using ```pip install -r requirements.txt```
3. Model parameters and changes can be found in ```config.py``` file
4. To execute, run: ```python main.py```

The data files ```(train.csv and test.csv)``` should be in a directory named ```data```
The ```output.csv``` file will be saved in the directory ```./output```

Open main.py to make changes on which columns are dropped, the X and Y columns.

## Submission on Kaggle and Google Forms

### Kaggle

To submit on Kaggle, set the following parameters in ```config.py```:
1. ```SUBMIT_TO_KAGGLE_GOOGLE = True```. 
2. ```COMPETITION_NAME = '<competition name here>'```

Submission to kaggle needs the kaggle.json file in ~/.Kaggle or C:\Users\<username_on_pc>\.kaggle. The kaggle.json can be downloaded from https://www.kaggle.com/<username>/account by clicking on Create New Token

### Google Form

Google on automated browser requires captcha to be submitted, so the last submit has to be done manually :(.

Important params to change in ```config.py```:
1. ```email```
2. ```erp```
3. ```kaggle_username```

The parameters used in google form are specified in ```config.py``` with commented instructions on how to set them. For now, the options are case sensitive. (To be automated more later)



