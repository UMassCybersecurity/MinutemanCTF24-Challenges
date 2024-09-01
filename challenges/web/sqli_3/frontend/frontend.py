import string
from flask import Flask, request, session, redirect, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import mysql.connector
import random

server = Flask(__name__)
server.secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) # generates random string
conn = None
waf = ['drop', 'delete', 'insert', ';']

limiter = Limiter(
    get_remote_address,
    app=server,
    default_limits=["1 per second"],
    storage_uri="memory://"
)

class DBManager:
    def __init__(self, database='user_db', host="db", user="root"):
        self.connection = mysql.connector.connect(
            user=user, 
            password='c4cc207db461462f8e22aa3ddc744b66',
            host=host, 
            database=database
        )
        self.db_append_table = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) # generates random string
        self.db_append_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) # generates random string
        self.db_append_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) # generates random string
        self.table = f'users_{self.db_append_table}'
        self.username = f'username_{self.db_append_username}'
        self.password = f'password_{self.db_append_password}'
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.table}')
        self.cursor.execute(f'CREATE TABLE {self.table} ({self.username} VARCHAR(255) primary key, {self.password} VARCHAR(255))')
        self.cursor.executemany(f'INSERT INTO {self.table} ({self.username}, {self.password}) VALUES (%s, %s);', [('admin', 'UMASS{OTHERFLAG}'), ('user1', 'password1')])
        self.connection.commit()

    def make_query(self, username, password):
        self.cursor.execute(f"select {self.username} from {self.table} where {self.username}='{username}' and {self.password}='{password}';")
        return [x[0] for x in self.cursor]
    
    def create_user(self, username, password):
        self.cursor.execute(f"insert into {self.table} ({self.username}, {self.password}) values ('{username}', '{password}');")

print("""sample text debug line 
      
      bottom text""")

@server.route('/')
def index():
    if 'sqlmap' in request.user_agent.string:
        return '<h1>no script kiddies here</h1>'
    if session.get('user'):
        if session.get('user') == 'admin':
            return render_template('index.html', message='Hello admin! The flag is in another castle.')
        else:
            return render_template('index.html', message=f"hi {session.get('user')}")
    
    return render_template('index.html', message='please go to login or register')

@server.route('/login')
def login():
    if 'sqlmap' in request.user_agent.string:
        return '<h1>no script kiddies here</h1>'
    # if session.get('user'):
    #     return redirect('/')
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

        if len(rec) == 0:
            return render_template('login.html', message="login incorrect")
        elif rec[0] == 'admin':
            session['user'] = 'admin'
            # for convenience
            return render_template('login.html', message=f'You are now logged in as {'admin'}')
            # return redirect('/')
        else:
            session['user'] = ' '.join(rec)
            # for convenience
            return render_template('login.html', message=f'You are now logged in as {' '.join(rec)}')
            # return redirect('/')
    return render_template('login.html')

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

    return render_template('register.html')

def wait_db():
    try:
        global conn
        if not conn:
            conn = DBManager()
            conn.populate_db()
    except:
        return True
    return False