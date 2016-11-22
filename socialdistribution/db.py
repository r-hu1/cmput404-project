from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

# from yourapplication.database import db_session

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' # In memory DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB/tables.db' # relative path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite' # In memory DB

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/yournewdb"
heroku = Heroku(app)
db = SQLAlchemy(app)
# db.create_all()

# For more information on DB URI: http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html


'''
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
'''
