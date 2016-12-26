#! /usr/bin/env python
# coding=utf-8
from functools import wraps
import json
from flask import session, render_template, make_response
from main import db
from main.models import User, Role, Permissions, UserPermissions


# 先查用户对应的用户组,再查用户组对应的权限,再查用户对应的权限,并集后, 如果传过来的权限在这个并集里,就执行函数,不然就就报没有权限的信息
class Permission(object):
    @classmethod
    def check(cls, *args, **kwargs):
        def decoratored(func):
            def wrap(*args, **kw):
                models = kwargs.get('models')
                if 'user_id' in session:
                    user_id = session['user_id']
                    curent_user = db.session.query(User).filter_by(id=user_id).first()
                else:
                    return json.dumps(dict(code=403, message='user not login'))
                if not curent_user:
                    return json.dumps(dict(code=403, message='not have this user'))
                else:
                    permission_list = []
                    user_permissions = db.session.query(UserPermissions).filter_by(user_id=user_id)
                    for user_permission in eval(user_permissions.permissions_id):
                        permission_list.append(
                            db.session.query(Permissions).filter_by(id=user_permission).first().name)
                    for model in models:
                        if model not in permission_list:
                            return json.dumps(dict(code=403, message='no permission'))
                return func(*args, **kw)

            return wrap

        return decoratored
