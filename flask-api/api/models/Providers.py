from .. import db
from time import time

class Provider(db.Model):
    """Model class for provider. (Organization)"""
    
    __tablename__ = 'Provider'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    offices = db.relationship('Office', backref='provider', lazy = True)