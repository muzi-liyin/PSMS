# -*- coding: utf-8 -*-

from flask import Flask
from main import psms_db

class Users(psms_db.Model):
    id = psms_db.Column(psms_db.Integer, primary_key=True, nullable=False)
    name = psms_db.Column(psms_db.String(20), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __repr__(self):
        return ''%(self.id, self.name)
    psms_db.create_all()