# Talkatiel_API
API for Talkatiel Project


## Steps to Setup
First be sure to have python and pip installed

If you don't have virtual envirnment installed either, run:
```
$ pip install --user pipenv
```

Then setup a virtual environment for the project and activate it.

```
$ virtualenv env
$ source activate
```
To exit the virtual environment when we are done we type:

```$ deactivate ```

Your terminal should now look like:

```(env) $ # command go here```

Next we want to install all the dependencies.  We do this by using pip

```(env)$ pip install -r requirements.txt```

This will install the python libraries in the virtual environment.  This means that anytime you install python packages, they will be installed in the virtual environment instead of your system.  This will stop packages from conflicting with each other and stop the packages that you already have installed from updating or changing.

To run the REST API, just run Reciever.py.  It will connect to the database defined and serve requests on the port defined.  The script will look for a sqlite database titled chinook.db, and will serve requests on port 5002.   