# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, session, url_for, redirect, render_template
from main import db
from main.models import Users

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        print request.data
        data = request.get_json(force=True)
        session["name"] = data["name"]
        user = Users(data["name"], data["email"], data["passwd"], data["phone"])
        db.session.add(user)
        db.session.commit()
        db.create_all()
        return session['name']
    elif request.method == "GET":
        if 'name' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@users.route('/login', methods=['POST', 'GET'])
def login_in():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = db.session.query(Users).filter_by(name=data["name"]).first()
        if data["passwd"] == user.passwd:
            session["name"] = data["name"]
            return session["name"]
        else:
            return 'passwd or username error'


@users.route('/login', methods=['POST', 'GET'])
def login_out():
    del session['name']
    return redirect(url_for('index'))


@users.route('/select', methods=['POST', 'GET'])
def select():
    if request.method == "POST":
        data = request.get_json(force=True)
        name = data["name"]
        user = db.session.query(Users).filter_by(name=name).first()
        return user.name