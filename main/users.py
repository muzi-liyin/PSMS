# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request
from main import psms_db
from main.models import Users

users = Blueprint('users', __name__)
@users.route('/', methods=['POST','GET'])
def create_user():
    if request.method == "POST":
        data = request.get_json(force=True)

        user = Users(data["name"])
        psms_db.session.add(user)
        psms_db.session.commit()
        return "hello"