# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request
from main import db
from main.models import Users
import json

users = Blueprint('users', __name__)
@users.route('/', methods=['POST','GET'])
def create_user():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = Users(data["name"])
        db.session.add(user)
        db.session.commit()
        db.create_all()
        return "hello"
@users.route('/select', methods=['POST','GET'])
def select():
    if request.method == "POST":
        data = request.get_json(force=True)
        name = data["name"]
        user = db.session.query(Users).filter_by(name=name).first()
        return user.name

@users.route('/offer', methods=['POST','GET'])
def create_offer():
    if request.method == "POST":
        data = request.get_json(force=True)