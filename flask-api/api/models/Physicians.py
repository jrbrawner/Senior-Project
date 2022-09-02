from .. import db
import json
from time import time

class Physician(db.Model):
    """Model for physicians."""

    __tablename__ = 'Physician' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    office_id = db.Column(db.Integer, db.ForeignKey('Office.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('Provider.id'), nullable=False)
    patients = db.Relationship('Patient.id', backref='patients', lazy=True)
    