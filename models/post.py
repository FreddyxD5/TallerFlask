from datetime import datetime
from aplicacion import db

class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_active=db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, body, timestamp, user_id):
        self.body = body
        self.timestamp = timestamp
        self.user_id = user_id

    def __repr__(self):
        return f'{ self.id } - {self.author }'