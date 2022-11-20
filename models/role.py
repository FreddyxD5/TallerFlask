from aplicacion import db
from utils.utils import Permisions


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    default= db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
        
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0
    
    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return self.name
    
    def insert_roles():
        roles = {
            'User':[Permisions.FOLLOW, Permisions.COMMENT, Permisions.WRITE],
            'Moderator':[Permisions.FOLLOW, Permisions.COMMENT, Permisions.WRITE, Permisions.MODERATE],
            'Administrador':[Permisions.FOLLOW, Permisions.COMMENT,
            Permisions.WRITE, Permisions.MODERATE, Permisions.ADMIN
            ]
        }

        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
