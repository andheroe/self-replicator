# Self-Replicator

This application will replicate a specified repository and the files contained within said repository to a user's GitHub account. Once the application is running, the user simply navigates to the specified url and authenticates their GitHub account, after which they will be redirected to their newly created repo.

The live application can be found here: https://self-replicator.herokuapp.com

# Running Locally
(Note) This assumes a user is completely new to Python and Flask

### 1. Installing Python
If your operating system does not provide you with a Python package, you can download an installer from the [Python official website](https://www.python.org/downloads/). Opening a terminal window and typing pthon3 should display the following

```bash
$ python3
Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 03:13:28) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
You can exit the interactive prompt by typing exit() and hitting enter.

### 2. Cloning the self-replicator Repo
You can now clone the application code from GitHub to a local workspace by following the intructions provided [here](https://help.github.com/articles/cloning-a-repository/) and with the repo clone url: https://github.com/alonzo118/self-replicator.git.

### 3. Starting a Virtual Environment
Within the newly cloned repo type the follwing to create a new virtual environment and activate it.
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

### 4. Installing required dependencies
Type the following to install all dependencies from the requirements.txt file.
```bash
$ pip install -r requirements.txt
```

### 5. Register your new OAuth app with GitHub and create .env file
Visit https://github.com/settings/applications/new to register your new OAuth app and obtain the required OAuth credentials. The application authorization callback URL must be set to http://localhost:5000/login/github/authorized. 

Taking the newly created client Id, client secret, and the repo/user you would like to replicate from, create a file called .env in the root directory of self-replicator repo with the following constants.
```python
SECRET_KEY='RANDOM-STRING'
GITHUB_CLIENT_ID='YOUR-NEW-CLIENT-ID'
GITHUB_CLIENT_SECRET='YOUR-NEW-CLIENT-SECRET'
ORIGIN_REPO_NAME='self-replicator' '''replicating the self-replicator repo'''
ORIGIN_REPO_USER='alonzo118'
```
Finally, because this is being run locally, we must set the OAUTHLIB_INSECURE_TRANSPORT variable to disable HTTPS requirements from oauthlib, a key part of the OAuth process. Please keep in mind that this should should only ever be done for local testing purposes and never run in a production envrionment. 
```bash
$ export OAUTHLIB_INSECURE_TRANSPORT=1
```

### 6. Starting the app and logging in with GitHub
Type the following to start the application.
```bash
$ python selfreplicator.py
```
Then navigate to http://localhost:5000/ and authenticate your GitHub account and the required permissions and viola you should be redirected to your newly replicated repo.

# Tech Specs
The purpose of this web application is to allows users to authenticate their GitHub account and then use that authentication to perform actions with their GitHub account and repositories that result in the replication of a specified repo.

The two main components at work here are Flask-Dance and GitPython which are wrapped in a Flask-framework application.

### Flask 
The [flask framework](http://flask.pocoo.org/) allows users to quickly create python-based web applications. 
* This specific application has one main view or route (@app.route("/")) (@app.route("/index")) that a user is initially directed to when heading to the application url. 
* From there we use a Request.session() github object to handle storage of the authentication parameters and persist cookies across all of the HTTP requests we will be making for our user. 

### OAuth with Flask Dance
To perform GitHub OAuth the application is using [Flask-Dance](https://github.com/singingwolfboy/flask-dance-github). This provides a blueprint that implements the views necessary to be a consumer in the OAuth process and simplifies the application from having to manually handle the OAuth process. From the flask-dance docs:

"The blueprint has two views: /github, which is the view that the user visits to begin the OAuth dance, and /github/authorized, which is the view that the user is redirected to at the end of the OAuth dance. 
Because we set the url_prefix to be /login, the end result is that the views are at /login/github and /login/github/authorized. The second view is the “authorized callback URL” that you must tell GitHub about when you create the application."

* The user is sent to GitHub to authenticate their info. 
* Once authenticated, GitHub redirects back to our /authorized url and provides a token that is stored in the `github` object which allows the application to perform the various tasks necessary using the GitHub API and Git.
* The application then makes a Get request for the origin repo information and a Create request to create a new bare repo for the authneticated user.

### Git commands with GitPython
Finally the application uses the [GitPython](https://gitpython.readthedocs.io/en/stable/) library to provide an abstraction of git objects and easy access of respository data and manipulation.

* The origin repo information that was returned from the GitHub API is used to clone said repo into a local scratch repo.
* A remote object representing the newly created destination GitHub repo is created.
* Finally the local cloned origin repo is pushed to the remote destination repo object as a master branch and the local-scratch repo directory is deleted.

The application then navigates a user to their newly replicated repo.

