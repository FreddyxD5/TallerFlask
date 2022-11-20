from datetime import datetime
from aplicacion import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from models.post import Post
from utils.utils import Permisions
from models.role import Role
import hashlib





class User(UserMixin, db.Model):
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',cascade="all, delete", passive_deletes=True, backref='author', lazy='dynamic',)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default= datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(300))

    def __init__(self, **kwargs):        
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username =="jesusu":
                self.role = Role.query.filter_by(name='Administrador').first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        self.avatar = '{url}/{hash}?={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=200, default = 'default', rating='g')

    def gravatar(self, size=200, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default = default, rating=rating)
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permisions.ADMIN)

    def __repr__(self):
        return f"{self.username}"


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username='Guest'
        
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

    def __repr__(self):
        return 'AnonymousUser'

login_manager.anonymous_user = AnonymousUser