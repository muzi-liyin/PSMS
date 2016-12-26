# -*- coding: utf-8 -*-
import base64
from datetime import datetime

from flask import Flask, Blueprint, request, session, g
import json

from main import db
from main.models import User, Role, Permissions, UserRole, RolePermissions, UserPermissions

users = Blueprint('users', __name__)


@users.route('/api/user/create', methods=['POST', 'GET'])
def create_user():
    role_ids = [4]
    permission_ids = [9, 10]
    if request.method == "POST":
        data = request.get_json(force=True)
        if db.session.query(User).filter_by(name=data["name"]).first():
            return json.dumps({"code": "500", "message": "user name has exist"})
        user = User(data["name"], data["email"], base64.encodestring(data["passwd"]), data["phone"])
        db.session.add(user)
        db.session.commit()
        userid = db.session.query(User).filter_by(name=data["name"]).first().id
        session["user_id"] = userid

        # 查出用户组对应的权限
        role_permission_list = []
        for roleid in role_ids:
            permissions = db.session.query(RolePermissions).filter_by(role_id=roleid)
            for permission in permissions:
                role_permission_list.append(permission.permissions_id)
        # 取出用户组对应的权限,和用户的权限做并集
        last_peremissions = list(set(role_permission_list + permission_ids))

        # 存有户权限表
        for permission in last_peremissions:
            user_permission = UserPermissions(userid, permission)
            db.session.add(user_permission)
        db.session.commit()

        # 存用户角色表
        for role in role_ids:
            user_role = UserRole(userid, role)
            db.session.add(user_role)
        db.session.commit()
        return json.dumps({"code": "200", "message": "success", "results": session["user_id"]})
    return json.dumps({"code": "500", "message": "request method error"})


@users.route('/api/user/do_edit/<id>', methods=['POST', 'GET'])
def do_edit_user(id):
    if request.method == "GET":
        # 查出用户所有角色
        local_dict = {}
        user = db.session.query(User).filter_by(id=id).first()
        userid = user.id
        roles = db.session.query(UserRole).filter_by(user_id=userid)
        role_list = []
        role_dict = {}
        for role in roles:
            role_dict[role.role_id] = db.session.query(Role).filter_by(id=role.role_id).first().name
            role_list.append(role_dict)
        local_dict['role_selected'] = role_list
        role_alls = Role.query.all()
        role_alls_dicts = {}
        for role_all in role_alls:
            role_alls_dicts[role_all.id] = role_all.name
        local_dict['role_all'] = role_alls_dicts
        # 查出用户所有的权限
        permission_list = []
        permission_dict = {}
        permissions = db.session.query(UserPermissions).filter_by(user_id=userid)
        for permission in permissions:
            permission_dict[permission.permissions_id] = db.session.query(Permissions).filter_by(
                id=permission.permissions_id).first().name
        permission_list.append(permission_dict)
        local_dict['permission_selected'] = permission_list
        permission_alls = Permissions.query.all()
        permission_alls_dicts = {}
        for permission_all in permission_alls:
            permission_alls_dicts[permission_all.id] = permission_all.name
        local_dict['permission_all'] = permission_alls_dicts

        # 查出用户的所有信息
        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'passwd': base64.decodestring(user.passwd),
            'phone': user.phone,
            'last_datetime': user.last_datetime
        }
        local_dict['user_msg'] = data
        return json.dumps({"code": "200", "message": "success", "results": local_dict})
    return json.dumps({"code": "500", "message": "request method error"})


@users.route('/api/user/edit/<id>', methods=['POST', 'GET'])
def edit_user(id):
    role_ids = []
    permission_ids = [12]
    if request.method == "POST":
        data = request.get_json(force=True)
        if not db.session.query(User).filter_by(id=id).first():
            return json.dumps({"code": "500", "message": "user name is not exist"})
        user = db.session.query(User).filter_by(id=id).first()
        userid = user.id
        user_permission_agos = db.session.query(UserPermissions).filter_by(user_id=userid)
        user_role_agos = db.session.query(UserRole).filter_by(user_id=userid)

        for user_permission_ago in user_permission_agos:
            # print user_permission_ago.permissions_id
            db.session.delete(user_permission_ago)
        for user_role_ago in user_role_agos:
            # print user_role_ago.role_id
            db.session.delete(user_role_ago)
        db.session.commit()


        # if db.session.query(User).filter_by(name=data["name"]).first():
        #     return json.dumps({"code": "500", "message": "user name has exist"})
        user.name = data["name"]
        user.email = data["email"]
        user.passwd = base64.encodestring(data["passwd"])
        user.phone = data["phone"]
        db.session.add(user)
        db.session.commit()
        userid = db.session.query(User).filter_by(name=data["name"]).first().id
        # session["user_id"] = userid

        # 查出用户组对应的权限
        role_permission_list = []
        for roleid in role_ids:
            permissions = db.session.query(RolePermissions).filter_by(role_id=roleid)
            for permission in permissions:
                role_permission_list.append(permission.permissions_id)
        # 取出用户组对应的权限,和用户的权限做并集
        last_peremissions = list(set(role_permission_list + permission_ids))

        # 存有户权限表
        for permission in last_peremissions:
            user_permission = UserPermissions(userid, permission)
            db.session.add(user_permission)
        db.session.commit()

        # 存用户角色表
        for role in role_ids:
            user_role = UserRole(userid, role)
            db.session.add(user_role)
        db.session.commit()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})

@users.route('/api/user/login', methods=['POST', 'GET'])
def login_in():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = db.session.query(User).filter_by(name=data["name"]).first()
        if user:
            user_id = db.session.query(User).filter_by(name=data["name"]).first().id
            user.last_datetime = str(datetime.now())
            if data["passwd"] == base64.decodestring(user.passwd):
                session["user_id"] = user_id
                return json.dumps({"code": "200", "message": "success", "results": session["user_id"]})
            else:
                return json.dumps({"code": "500", "message": "password error!"})
        else:
            return json.dumps({"code": "500", "message": "user has not register"})


@users.route('/api/user/logout', methods=['POST', 'GET'])
def login_out():
    if request.method == "POST":
        session.pop('user_id', None)
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})


@users.route('/api/role/create', methods=['POST', 'GET'])
def create_role():
    permission_list = [11, 14, 15]
    if request.method == "POST":
        data = request.get_json(force=True)
        role = Role(data["name"])
        if db.session.query(Role).filter_by(name=data["name"]).first():
            return json.dumps({"code": "500", "message": "role had exits"})
        db.session.add(role)
        db.session.commit()
        role_id = role.id
        for i in permission_list:
            role_permissions = RolePermissions(role_id, i)
            db.session.add(role_permissions)
        db.session.commit()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})
