from histoviewer import histoviewer
import pandas as pd

cols = str('age,workclass,fnlwgt,education,education-num,'
           'marital-status,occupation,relationship,race,sex,'
           'capital-gain,capital-loss,hours-per-week,'
           'native-country,class')

# load adult income dataset from UCI:
#   https://archive.ics.uci.edu/ml/datasets/Adult
adult = pd.read_csv('sample_data/adult.csv', names=cols.split(','),
                    header=None, index_col=None)

# execute script with:
#   bokeh serve sample_app.py
# then navigate to the URL:
#   http://localhost:5006/sample_app
histoviewer(adult, 'fnlwgt', serve='shell')
