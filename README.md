These instructions were adopted from [Zach Duey](https://zduey.github.io/snippets/app-deployment-with-heroku/).

#### Deploy Instructions

1. Clone/init git and cd into folder
2. Setup heroku
    - Install [heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
    - Execute ```heroku login``` and login with heroku account credentials
3. Execute ```heroku create```
4. Create virtual environment by executing following commands:
    - ```conda create -n histoviewer python=2.7```
    - ```source activate histoviewer```
    - ```pip install -r requirements.txt```
5. Create **runtime.txt** file with the following text:
    - python-2.7.14
6. Create **Procfile** file with the following text:
    - web: bokeh serve --port=$PORT --host=**{appname}**.herokuapp.com --address=0.0.0.0 --use-xheaders sample_app.py
7. Commit to heroku git by executing below commands:
    - ```git add .```
    - ```git commit -m 'some message'```
    - if committing from master branch: ```git push heroku master```
    - if committing from non-master branch: ```git push heroku non-master:master```
