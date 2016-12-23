# -*- coding: utf-8 -*-
import base64

from flask import Flask, Blueprint, request, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
import json

from main import db
from main.models import User, Group

users = Blueprint('users', __name__)


@users.route('/api/user/create', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = User(data["name"], data["email"], base64.encodestring(data["passwd"]), data["phone"])
        db.session.add(user)
        db.session.commit()
        db.create_all()
        session["user_id"] = db.session.query(User).filter_by(name=data["name"]).first().id
        return json.dumps({"code": "200", "message": "success", "results": session["user_id"]})
    return json.dumps({"code": "500", "message": "request method error"})


@users.route('/api/user/login', methods=['POST', 'GET'])
def login_in():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = db.session.query(User).filter_by(name=data["name"]).first()
        user_id = db.session.query(User).filter_by(name=data["name"]).first().id
        if data["passwd"] == base64.decodestring(user.passwd):
            session["user_id"] = user_id
            return json.dumps({"code": "200", "message": "success", "results": session["name"]})
        else:
            return json.dumps({"code": "500", "message": "password error!"})


@users.route('/api/user/logout', methods=['POST', 'GET'])
def login_out():
    if request.method == "POST":
        session.pop('user_id', None)
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})


@users.route('/api/group/create', methods=['POST', 'GET'])
def create_group():
    if request.method == "POST":
        data = request.get_json(force=True)
        group = Group(data["name"])
        db.session.add(group)
        db.session.commit()
        db.create_all()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})
