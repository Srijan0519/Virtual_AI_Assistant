from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2
import datetime

def get_database_connection():
  """Connects to the PostgreSQL database and returns a connection object."""

  try:
    # Replace these placeholders with your actual database credentials
    connection = psycopg2.connect(user="postgres",
                                  password="your_password",
                                  host="localhost",
                                  port="5432",
                                  database="your_database_name")
    return connection

  except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL database", error)
    return None

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:your_password@localhost:5432/your_database_name'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.Text, nullable=False)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))