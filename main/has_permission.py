#! /usr/bin/env python
# coding=utf-8
from functools import wraps
import json
from flask import session
from main import db
from main.models import User, Role, Permissions, UserRole, RolePermissions, UserPermissions


# Permission.check(permissions=['dashboard_create, dashboard_edit'])

# 先查用户对应的用户组,再查用户组对应的权限,再查用户对应的权限,并集后, 如果传过来的权限在这个并集里,就执行函数,不然就就报没有权限的信息
class Permission(object):
    @classmethod
    def check(cls, **kwargs):
        def decoratored(func):
            def wrap(*args, **kw):
                models = kwargs.get('models')
                user_id = session['user_id']
                curent_user = db.session.query(User).filter_by(id=user_id).first()
                if not curent_user:
                    return json.dumps(dict(code=403, message='please login in'))
                else:
                    permission_list = []
                    user_permissions = db.session.query(UserPermissions).filter_by(user_id=user_id)
                    for user_permission in user_permissions:
                        permission_list.append(
                            db.session.query(Permissions).filter_by(id=user_permission.permissions_id).first())
                    for model in models:
                        if model not in permission_list:
                            return json.dumps(dict(code=403, message='no permission'))
                        else:
                            return
                return func(*args, **kw)

            return wrap

        return decoratored
