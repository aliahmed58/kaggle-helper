""" 
Util file to auto submit output files to kaggle and Google forms provided
"""

import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
import time
import config


FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSduSrNxsx5C1qat-t71uTXHyR8vjLoGPhNHEMvkEVHj92s6IA/viewform'

# Do not change
form_input_dict = {
    'email': [config.email, '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input'],
    
    'erp': [config.erp, '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'],
    
    'kaggle_username': [config.kaggle_username, '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'],
    
    'param_specs': [config.parameter_specification, '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input'],
    
    'date': ['Will be auto selected', '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input'],
    
    'time': {
        'hour': '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/input',
        'min': '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[3]/div/div[1]/div/div[1]/input',
        'am_pm_button': '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[4]/div[1]/div[2]',
        'AM': '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[4]/div[2]/div[1]/span',
        'PM': '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[4]/div[2]/div[2]/span'
    },
    
    'model_name': {
        'name_button': '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div[1]/div[1]',
        'Random Forest': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[3]',
        'Gradient Boosting': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[4]',
        'Adaptive Boosting': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[5]',
        'Light GBM': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[6]',
        'XGBoost': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[7]',
        'CatBoost': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[8]',
        'BaggingClassifier': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[9]',
        'other': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[10]'
    },
    'additional_notes': [config.additional_notes, '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div[1]/div[2]/textarea']
}


def make_submission(challenge_name: str, filepath: str, description: str) -> None:
    submit_to_kaggle(challenge_name, filepath, description)
    fill_google_form()

def _get_timestamp() -> list:
    """
    Get the time stamp in the format required in Google Forms: HOUR : MINUTES : AM / PM
    Returns:
        list: a list with the timestamp strings in the respective order ['hr', 'min', 'am/pm']
    """
    now = datetime.now()
    am_pm = now.strftime('%p')
    hour = now.strftime('%H')
    minutes = now.strftime('%M')
    
    return [hour, minutes, am_pm]

def _get_date() -> str:
    """
    Get today's date in the format mm/dd/yyy
    Returns:
        str: the string value of date in the given format
    """
    now = datetime.now()
    return now.strftime('%m/%d/%Y')
    

def submit_to_kaggle(challenge_name: str, filepath: str, description: str) -> bool:
    """
    Method to submit the output file in to kaggle competition
    Args:
        challenge_name (str): the name of challenge on kaggle
        filepath (str): the file path of the file to be submitted
        description (str): the description that will be posted along with the submission

    Returns:
        bool: True if successfully submitted, else False
    """
    exit_code = os.system(f'kaggle competitions submit -c {challenge_name} -f {filepath} -m "{description}"')

    return exit_code == 0


def fill_google_form():
    browser = webdriver.Chrome()
    
    browser.get(FORM_LINK)
    
    for key, value in form_input_dict.items():
       
        if key == 'time':
            time_dict = form_input_dict[key]
            timestamp = _get_timestamp()
            hour_element = browser.find_element(By.XPATH, time_dict['hour'])
            min_element = browser.find_element(By.XPATH, time_dict['min'])
            
            hour_element.send_keys(timestamp[0])
            min_element.send_keys(timestamp[1])
                
            continue
            
        if key == 'model_name':
            model_dict = form_input_dict[key]
            name_button = browser.find_element(By.XPATH, model_dict['name_button'])
            
            name_button.send_keys(Keys.ENTER)
            
            time.sleep(1)
            
            model_name = browser.find_element(By.XPATH, model_dict[config.MODEL_NAME])
            model_name.click()
            
            continue
        
        element = browser.find_element(By.XPATH, value[1])
        
        if key in ['email', 'erp', 'kaggle_username', 'param_specs', 'additional_notes']:
            element.send_keys(value[0])
            continue
        if key == 'date':
            date_str = _get_date()
            element.send_keys(date_str)
            continue
    
    # multiple choice options select for data cleaning techniques
    for option in config.data_cleaning_techniques:
        x_path = f"//span[text()='{option}']"
        choice = browser.find_element(By.XPATH, x_path)
        choice.click()
    
    for option in config.missing_values_handled:
        x_path = f"//span[text()='{option}']"
        choice = browser.find_element(By.XPATH, x_path)
        choice.click()
        
    send_a_copy = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[2]/div/div[3]/div[1]/label/div/div[1]')
    send_a_copy.click()
    
    if config.AUTO_SUBMIT_GOOGLE:
        send_btn = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[2]/div/div[3]/div[3]/div[1]/div/span')
        send_btn.click()
    
    while (True):
        pass
            
