import string
from flask import Flask, request, session, redirect, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import mysql.connector
import random
import os

server = Flask(__name__)
server.secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)) # generates random string
conn = None
waf = ['drop', 'delete', 'insert', ';']
FLAG = os.environ['FLAG']

limiter = Limiter(
    get_remote_address,
    app=server,
    default_limits=["100 per second"],
    storage_uri="memory://"
)

class DBManager:
    def __init__(self):
        self.admin_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)) # generates random string

    def init_db(self, database='user_db', host="db", user="root"):
        self.connection = mysql.connector.connect(
            user=user, 
            password='c4cc207db461462f8e22aa3ddc744b66',
            host=host, 
            database=database
        )
        self.cursor = self.connection.cursor()

    def close_db(self):
        self.cursor.close()
        self.connection.close()

    def populate_db(self):
        self.init_db()
        self.cursor.execute(f'DROP TABLE IF EXISTS users')
        self.cursor.execute(f'CREATE TABLE users (username VARCHAR(255) primary key, password VARCHAR(255))')
        self.cursor.executemany(f'INSERT INTO users (username, password) VALUES (%s, %s);', [('admin', self.admin_password), ('user1', 'password1')])
        self.connection.commit()
        self.close_db()

    def make_query(self, username, password):
        self.init_db()
        self.cursor.execute(f"select username from users where username='{username}' and password='{password}';") # todo add stack trace in output
        res = [x[0] for x in self.cursor]
        self.close_db()
        return res

    def create_user(self, username, password):
        self.init_db()
        self.cursor.execute(f"insert into users (username, password) values ('{username}', '{password}');")
        self.close_db()

print("""sample text debug line 
      
      bottom text""")

@server.route('/')
def index():
    if 'sqlmap' in request.user_agent.string:
        return '<h1>no script kiddies here</h1>'
    if session.get('user'):
        if session.get('user') == 'admin':
            return render_template('index.html', message=f'Hello admin!\n{FLAG}')# UMASS{FLAG_CONTENTS}
        else:
            return render_template('index.html', message=f"hi {session.get('user')}")
    
    return render_template('index.html', message='please go to login or register')

@server.route('/login')
def login():
    if 'sqlmap' in request.user_agent.string:
        return '<h1>no script kiddies here</h1>'
    if session.get('user'):
        return redirect('/')
    username, password = request.args.get('username'), request.args.get('password')
    if username and password:
        if wait_db():
            return render_template('login.html', message='database still loading, please wait')
        if any([x in username.lower() or x in password.lower() for x in waf]):
            return render_template('login.html', message='please dont break this')

        try:
            rec = conn.make_query(username, password)
        except Exception as e:
            return render_template('login.html', message=f"something went wrong ({e})")

        if len(rec) != 1:
            return render_template('login.html', message="login incorrect")
        elif rec[0] == 'admin':
            session['user'] = 'admin'
            return redirect('/')
        else:
            session['user'] = rec[0]
            return redirect('/')
    if not username and not password:
        return render_template('login.html')
    return render_template('login.html', message="Please enter both username and password")

@server.route('/logout')
def logout():
    if 'sqlmap' in request.user_agent.string:
        return '<h1>no script kiddies here</h1>'
    if session.get('user'):
        session.pop('user')
    return redirect('/')

@server.route('/register')
def register():
    if 'sqlmap' in request.user_agent.string:
        return '<h1>no script kiddies here</h1>'
    if session.get('user'):
        return redirect('/')
    username, password = request.args.get('username'), request.args.get('password')
    if username and password:
        if wait_db():
            return render_template('register.html', message='database still loading, please wait')
        if any([x in username.lower() or x in password.lower() for x in waf]):
            return render_template('register.html', message='please dont break this')

        try:
            conn.create_user(username, password)
            session['user'] = username
            return redirect('/')
        except Exception as e:
            return render_template('register.html', message=f"something went wrong ({e})")

    if not username and not password:
        return render_template('register.html')
    return render_template('register.html', message="please enter both username and password")

def wait_db():
    try:
        global conn
        if not conn:
            conn = DBManager()
            conn.populate_db()
    except:
        return True
    return False
