# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os
                 # os is used to get environment variables IP & PORT
from flask import Flask
from flask import request
from flask import render_template
# from flask.helpers import url_for
from flask import redirect, url_for
# from werkzeug.utils import redirect # Flask is the web app that we will customize
from database import db
from models import Note as Note
from models import User as User
from forms import RegisterForm
# from flask import bcrypt
# from flask import Bcrypt
# from flask.ext.bcrypt import Bcrypt
from flask import session
import bcrypt

from forms import LoginForm

app = Flask(__name__)     # create an app

# bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

app.config['SECRET_KEY'] = 'SE3155'

app.debug = True

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# notes = {1: {'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
#              2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
#              3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}
#              }

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
# @app.route('/')
@app.route('/index')
def index():
    # return 'Welcome, Notes App User!'
    # a_user = {'name': 'Miguel', 'email': 'mmorel@uncc.edu'}

    #check if a user is saved in session
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template('index.html')

    #get user from database
    # a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()

    # return render_template('index.html', user = a_user)

@app.route('/notes')
def get_notes():
    # a_user = {'name': 'Mogli', 'email': 'mogli@uncc.edu'}

    #retrieve user from database
    # a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()

    #check if user is saved in session
    if session.get('user'):
        #retrieve notes from database
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes = my_notes, user = session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/notes/<note_id>')
# @app.route('/notes/1')
def get_note(note_id):
    # a_user = {'name': 'Mogli', 'email': 'mogli@uncc.edu'}
    
    #retrieve user from database
    a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()

    #retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id)

    return render_template('note.html', note = my_note, user = a_user)


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    #check if a user is saved in session
    if session.get('user'):
        #check method used for request
        if request.method == 'POST':
            #get title data
            title = request.form['title']
            # get note data
            text = request.form['noteText']
            # create date stamp
            note= db.session.query(Note).filter_by(id=note_id).one()
            #update note data
            note.title = title
            note.text = text

            #update note in database
            db.session.add(note)
            db.session.commit()
            
            return redirect(url_for('get_notes'))

        else:
        # a_user = {'name': 'Mogli', 'email': 'mogli@uncc.edu'}
        #GET request - show new note form to edit note
        #retrieve user from database
            # a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()

        #retrieve note from database
            my_note = db.session.query(Note).filter_by(id=note_id).one()

            return render_template('new.html', note = my_note, user =session['user'])
    else: 
        #user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    #check if a user is saved in session
    if session.get('user'):
        #retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()
        db.session.delete(my_note)
        db.session.commit()
            
        return redirect(url_for('get_notes'))
    else:
        #user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    #create mock user
    # a_user = {'name': 'Mogli', 'email': 'mogli@uncc.edu'}

    #check metthod used for request

    #check if a user used for request
    if session.get('user'):
        #check method used for request
        if request.method == 'POST':
            #get title data
            title = request.form['title']
            # get note data
            text = request.form['noteText']
            # create date stamp
            from datetime import date
            today = date.today()
            # format date mm/dd/yyyy
            today = today.strftime('%m-%d-%Y')
            new_record = Note(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            
            return redirect(url_for('get_notes'))

        else:
            #GET request - show new note form
            #retrieve user from database
            # a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()
            return render_template('new.html', user=session['user'])
    else:
        #user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
