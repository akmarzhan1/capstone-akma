# Welcome to the Content Suggestion tool

Welcome to my Capstone! You have two options to access this project: through Heroku and by manually downloading and running locally.

## Heroku Deployment

The link to the Heroku website: https://capstone-akma.herokuapp.com/about 


## IMPORTANT NOTICE

Some things that are not yet included due to the time limit, but which I am planning to include:

- [x] responsive images and timer (it only works for a zoomed out screen for now)
- [x] to-do tasks integration with flask 
- [x] addition of timer feature inside todo tasks 
- [x] larger game selection 
- [x] settings page integration 

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


