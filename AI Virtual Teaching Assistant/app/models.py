from datetime import datetime
from app import app, db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Chat(id={self.id}, message='{self.message[:50]}...', session_id='{self.session_id}', timestamp='{self.timestamp}')"

    def to_dict(self):
        data = {
            'id': self.id,
            'message': self.message,
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat()
        }
        return data

with app.app_context():
    db.create_all()