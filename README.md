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

## How to make requests

### Posts
#### Get Feed
There are 3 different types of sorting one user: Hot, Top, and New.  When making a get request to each of these, you can append a number to the url to get from that post num onward.  This will return 50 posts.
##### URLS
* /Posts/Hot/\<optional:startingIdx> GET Hot
* /Posts/Top/\<optional:startingIdx> GET Top
* /Posts/New/\<optional:startingIdx> GET New

#### Getting Comments
To get comments, you'll make a get request using the parent post's ID.
##### URL
* /Posts/\<int:postID> GET

#### Voting
To upvote or downvote a post, you will make a get request at a url made up of the post id and the type of vote.  The vote type is 0 for downvote and any positive number for upvote.
##### URL
* /Posts/\<int:postID>/\<int:voteType> GET

#### Reporting Comments/Posts
Use a POST method to send the report data.  The userID will be the ID of the reporting user.  The reason will be the text of the reason for the report, limit 1000 characters.
Use the json format:
* data:
  * userID
  * reason
##### URL
* /Posts/Report/\<int:postID> POST

#### Deleting a Post
Send a GET request to the URL to remove the post with that postID.
##### URL
* /Posts/Delete/\<int:postID> GET


### Users
#### Add a User
To add a user, make a post request.  UserID is self explanatory.  The phone is the phone number of the user.  The deviceID is a unique device identifier. Admin is a boolean, true if they are an admin.
user the json format:
* data:
	* userID
	* phone
	* deviceID
	* admin
##### URL
* /Users/ POST
#### Getting data about user
Make a get request to the url with the userID
##### URL
* /Users/\<int:userID> GET