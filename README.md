## Introduction
Histoviewer is an interactive bokeh application for dynamically viewing histograms and bar charts for a pandas DataFrame input.

Try out the application here (it may take up to a minute to start the heroku app):  
https://histoviewer.herokuapp.com/sample_app

Play around with the sliders, text inputs, dropdowns, and button widgets to update the data dynamically!

## Features
Histoviewer uses bokeh widgets to interact with the displayed plots. The column selection dropdown changes the data source to **df[column]**.

- Continuous variables
  - dynamically rebin histogram from 10-100 bins
  - dynamically rescale minimum/maximum bounds of histogram
- Categorical variables
  - resort by y-axis (descending) or x-axis (alphabetical)
  - reindex x-axis to filter categories

## Getting Started
To use Histoviewer, simply install the required dependencies:  
```
pip install -r requirements.txt
```

Then run the following code (in Jupyter notebook) to interact with a pandas DataFrame:
```
from histoviewer import histoviewer
histoviewer(df)
```

For an example of how to run histoviewer from a python 2.7 script, see [sample_app.py](https://github.com/alvinthai/histoviewer/blob/master/sample_app.py).
