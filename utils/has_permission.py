#! /usr/bin/env python
# coding=utf-8
from functools import wraps
import json

#
# def login_required(func):
#     @wraps(func)
#     def _wrapper(request, *args, **kwargs):
#         if 'user' not in request.session:
#             print 'redicet login html'
#         if request.session:
#             request.user = request.session
#             return func(request, *args, **kwargs)
#         else:
#             print 'redicet login html'
#
#     return _wrapper

#
# def has_permission(permission_list):
#     def has_permission_wrapper(func):
#         @wraps(func)
#         def _wrapper(request, *args, **kwargs):
#             user = request.user
#             permissions = json.loads(user.permission)
#             if permissions.get(permission for permission in permission_list if permission in permissions):
#                 return func(request, *args, **kwargs)
#             else:
#                 refer = ''
#                 has_refer = False
#                 if 'HTTP_REFERER' in request.META:
#                     refer = request.META['HTTP_REFERER']
#                     has_refer = (refer != "")
#                 data = {'refer': refer, 'has_refer': has_refer}
#                 return HttpResponse("403")
#
#         return _wrapper
#
#     return has_permission_wrapper
from flask import session


class Permission(object):

    @classmethod
    def check(cls, **kwargs):
        def decoratored(func):
            def wrap(handler, *args, **kw):
                model, operators = kwargs.get('model'), kwargs.get('operate')
                curent_user = session['name']
                if not curent_user:
                    handler.finish(dict(status_code=403, msg='Please Login!'))
                    return
                else:
                    current_user_role = curent_user.role or {}
                    if model:
                        if not current_user_role.get('permission', {}):
                            handler.finish(dict(status_code=403, msg='No Permission!'))
                            return
                        elif operators:
                            has_permission = False
                            for operator in operators:
                                if current_user_role.get('permission').get(model, {}).get(operator):
                                    has_permission = True
                            if not has_permission:
                                handler.finish(dict(status_code=403, msg='No Permission!'))
                                return
                return func(handler, *args, **kw)
            return wrap
        return decoratored