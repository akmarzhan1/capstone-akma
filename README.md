# Welcome to the Content Suggestion tool

Welcome to my Capstone! You have two options to access this project: through Heroku and by manually downloading and running locally. 

## Heroku Deployment

The link to the Heroku website: https://capstone-akma.herokuapp.com/about 

Note that the user information collected before February 27th is not maintained, so you would have to create a new account. Sorry for the inconvenience. You can also use the pre-made user information or create your own account if you want to test the register page:

```{python}
email: test@user.com
password: test1234
```
## Documentation and Helpful Links

Watch these videos to familiarize yourself with the app and its features.

#### Prototype 2
[![Video tutorial](https://user-images.githubusercontent.com/47840436/155910621-8e570c0b-5cb3-461f-aaa4-c3945b030668.png)](https://drive.google.com/file/d/1xpgPpe7_YenO-bV89TyrH1irMNF0Gu06/view?usp=sharing "[v0.2] Video tutorial")

#### Prototype 3

[![Video tutorial](https://user-images.githubusercontent.com/47840436/155910386-d385508b-1007-4421-9950-7ba1a4f613aa.png)](https://drive.google.com/file/d/1MEsSbRu7UOULC_42P9sk8FxwKQ7AL1yY/view?usp=sharing "[v0.3] Video tutorial")

You can also check out the other helpful links in my Notion [here](https://akmarzhan.notion.site/Capstone-5d82dfda87854d789d97c13e08cb5f9e). It has all the documentation and so on. This is the final paper that explains my project. You can find it [here](https://drive.google.com/file/d/1zruBliinuT4rVAPfmo9ndoSyDf-stb1B/view?usp=sharing).

## IMPORTANT NOTICE

Some things that are not yet included due to the time limit, but which I am planning to include:

- [x] larger game selection 
- [x] Github/Google login

## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

##### Usage
Creation of virtualenv:

    $ virtualenv -p python3 venv

If the above code does not work, you could also do

    $ python3 -m venv venv

To activate the virtualenv:

    $ source venv/bin/activate

Or, if you are **using Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

To deactivate the virtualenv (after you finished working):

    $ deactivate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

## Environment Variables

All environment variables are stored within the `.env` file and loaded with dotenv package.

**Never** commit your local settings to the Github repository!

## Run Application

Start the server by running:

    $ export FLASK_ENV=dev
    $ export FLASK_APP=web
    $ export DATABASE_URL='sqlite:///web.db'
    $ export SECRET_KEY='testing_key'
    $ python3 -m flask run
    
If **using Windows**, use 'set' instead of 'export'

## Flask-Migrate

Flask-Migrations is an extensions that manages DB migrations, common commands:

flask db migrate (create migration)
flask db upgrade (implement migration in the DB)


