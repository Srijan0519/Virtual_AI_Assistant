from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from app.models import User, Chat

@app.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('chat'))
  return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('chat'))

  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Implement logic to validate user input and create a new User object
    new_user = User(username=username, email=email, hashed_password= "Abcd_2$")
    # Hashed password logic omitted for brevity

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash('Signup successful! Please login.', 'success')
    return redirect(url_for('login'))

  return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('chat'))

  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):  # Check hashed password
      login_user(user)
      flash('Logged in successfully!', 'success')
      return redirect(url_for('chat'))
    else:
      flash('Invalid email/password combination.', 'danger')

  return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logged out successfully!', 'success')
  return redirect(url_for('index'))

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
  if request.method == 'POST':
    message = request.form['message']

    # Create a new Chat object with the message
    new_chat = Chat(session_id='<session_id>', message=message)  # Replace with actual session ID

    # Add the chat message to the database
    db.session.add(new_chat)
    db.session.commit()

  # Retrieve chat history based on session ID
  chat_history = Chat.query.filter_by(session_id='<session_id>').all()  # Replace with actual session ID

  return render_template('chat.html', chat_history=chat_history)
