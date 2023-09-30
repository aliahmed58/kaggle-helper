""" 
Util file to auto submit output files to kaggle and Google forms provided

1.  Submission to kaggle needs the kaggle.json file in ~/.Kaggle or C:\Users\<username_on_pc>\.kaggle
    The kaggle.json can be downloaded from https://www.kaggle.com/<username>/account by clicking on Create New Token
"""

import os

def submit_to_kaggle(description: str, filename: str) -> None:    
    os.system(f'kaggle competitions submit -c iml-fall-2023-first-challenge -f {filename} -m "Message"') 