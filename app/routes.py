import shutil
import git
from flask import render_template, redirect, url_for, json
from app import app
from werkzeug.contrib.fixers import ProxyFix
from flask_dance.contrib.github import make_github_blueprint, github
from git import Repo
from config import tmp


app.wsgi_app = ProxyFix(app.wsgi_app)

blueprint = make_github_blueprint(
    app.config['GITHUB_CLIENT_ID'],
    app.config['GITHUB_CLIENT_SECRET'],
    scope=['public_repo']
)

app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
@app.route("/index")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))

    origin_repo = github.get('/repos/' + app.config['ORIGIN_REPO_USER'] + '/' +
        app.config['ORIGIN_REPO_NAME'])
    if not origin_repo.ok:
        return ('Repo <b>{repo}</b> for user <b>@{login}</b> not found on GitHub. '
        'Please restart application with a valid user/repo combination'
        ' to replicate.'.format(repo=app.config['ORIGIN_REPO_NAME'],
            login=app.config['ORIGIN_REPO_USER']))

    origin_repo_name = origin_repo.json()['name']
    user_login = github.get('/user').json()['login']

    new_repo_name = origin_repo_name
    duplicate_incrementor = 1
    while github.get("/repos/" + user_login + '/' + new_repo_name).ok:
        new_repo_name = origin_repo_name + str(duplicate_incrementor)
        duplicate_incrementor += 1

    payload = {'name': new_repo_name, 'description': origin_repo.json()['description']}
    response = github.post("/user/repos", json.dumps(payload))

    repo = Repo.clone_from(origin_repo.json()['clone_url'], tmp + '/' + new_repo_name)
    remote = repo.create_remote('target', response.json()['clone_url'][:8] +
        github.token['access_token'] + ':' + 'x-oauth-basic@' +
        response.json()['clone_url'][8:])
    remote.push(refspec='{}:{}'.format('master','master'))
    shutil.rmtree(tmp + '/' + new_repo_name)

    return redirect(response.json()['svn_url'])
