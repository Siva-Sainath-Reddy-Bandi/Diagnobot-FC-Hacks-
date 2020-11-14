from flask import Flask
# flask_sqlalchemy has some additional features that makes it easier to work with flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt     # Hashes passwords to ensure that even if database is hacked, it cannot be found
from flask_login import LoginManager

# __name__ is so that flask knows where to look for templates and static files
app = Flask(__name__)
# protects against modifying cookies, cross site requests, forgery attacks, etc.
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'     # /// are a relative path from the current file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # what the user is redirected to if they try accessing account before logging in
login_manager.login_message_category = 'info'

from flaskblog import routes