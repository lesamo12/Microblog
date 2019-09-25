from flask import Flask

app = Flask (__name__)
from flask import escape,url_for


@app.route('/')
def index():
    return  'index'

@app.route('/login')
def login():
    return  'login'

@app.route('/user/<username>')
def profile (username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():

    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login',next='/'))
    print(url_for('profile',username='oussama'))