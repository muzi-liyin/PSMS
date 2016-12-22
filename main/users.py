# -*- coding: utf-8 -*-
import base64

from flask import Flask, Blueprint, request, session, url_for, redirect, render_template
import json

from main import db
from main.models import User
from has_permission import Permission

users = Blueprint('users', __name__)


@Permission.check(model='users', operate=['query'])
@users.route('/register', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        print request.data
        data = request.get_json(force=True)
        session["name"] = data["name"]
        user = User(data["name"], data["email"], base64.encodestring(data["passwd"]), data["phone"])
        db.session.add(user)
        db.session.commit()
        db.create_all()
        return json.dumps({"code": "200", "message": session["name"]})
    elif request.method == "GET":
        if 'name' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@users.route('/login', methods=['POST', 'GET'])
def login_in():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = db.session.query(User).filter_by(name=data["name"]).first()
        if data["passwd"] == base64.decodestring(user.passwd):
            session["name"] = data["name"]
            return session["name"]
        else:
            return 'passwd or username error'


@users.route('/login', methods=['POST', 'GET'])
def login_out():
    del session['name']
    return redirect(url_for('index'))


    # @users.route('/select', methods=['POST', 'GET'])
    # def select():
    #     if request.method == "POST":
    #         data = request.get_json(force=True)
    #         name = data["name"]
    #         user = db.session.query(Users).filter_by(name=name).first()
    #         return user.name
