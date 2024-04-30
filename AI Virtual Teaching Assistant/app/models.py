from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from app import db,app

from datetime import datetime

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    #datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Chat(id={self.id}, user_message='{self.user_message}', bot_response='{self.bot_response}', session_id='{self.session_id}', timestamp='{self.timestamp}')"

with app.app_context():
    db.create_all()
