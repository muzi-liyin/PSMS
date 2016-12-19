# -*- coding: utf-8 -*-
from main import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Model Users `{}`>'%(self.name)