#! /usr/bin/env python
# coding=utf-8
from functools import wraps
import json
from flask import session
from main import db
from main.models import User


class Permission(object):
    @classmethod
    def check(cls, **kwargs):
        def decoratored(func):
            def wrap(handler, *args, **kw):
                model, operators = kwargs.get('model'), kwargs.get('operate')
                curent_user = session['name']
                if not curent_user:
                    return json.dumps(dict(code=403, message='Please Login!'))
                else:
                    curent_user_role = db.session.query(User).filter_by(name=curent_user).first().group() or {}
                    if model:
                        if not curent_user_role.get('permission', {}):
                            return json.dumps(dict(code=403, message='No Permission!'))
                        elif operators:
                            has_permission = False
                            for operator in operators:
                                if curent_user_role.get('permission').get(model, {}).get(operator):
                                    has_permission = True
                            if not has_permission:
                                return json.dumps(dict(status_code=403, msg='No Permission!'))
                return func(handler, *args, **kw)

            return wrap

        return decoratored
