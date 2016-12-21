# -*- coding: utf-8 -*-
import uuid

from flask import Flask, Blueprint, request
from werkzeug.wrappers import Response

from main import db
from main.models import Customers
import json

customers = Blueprint('customers', __name__)


def add_origin(data):
    resp = Response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@customers.route('/customers/create', methods=['POST', 'GET'])
def create_customer():
    if request.method == "POST":
        data = request.get_json(force=True)
        code = uuid.uuid1()
        customer_code = str(code).upper()[:8]

        if db.session.query(Customers).filter_by(company_address=data["company_name"]):
            resp = add_origin(json.dumps({"code": "500", "message": "failed"}))
            return resp
            # return json.dumps({"code": "500", "message": "failed"})
        customer = Customers(customer_code, data["company_name"], data['company_address'], data['comment'])
        db.session.add(customer)
        db.session.commit()
        db.create_all()
        resp = add_origin(json.dumps({"code": "200", "message": "success"}))
        return resp
    resp = add_origin(json.dumps({"code": "500", "message": "failed"}))
    return resp


@customers.route('/customers', methods=['POST', 'GET'])
def customer():
    if request.method == "GET":
        customers = db.session.query(Customers).filter().all()
        msg_list = []
        msg = {}
        for customer in customers:
            msg['customers_id'] = customer.id
            msg['customer_code'] = customer.customer_code
            msg['company_name'] = customer.company_name
            msg['company_address'] = customer.company_address
            msg['comment'] = customer.comment
            msg_list.append(msg)
        resp = add_origin(json.dumps(msg_list))
        return resp
    resp = add_origin(json.dumps({"code": "500", "message": "failed"}))
    return resp


@customers.route('/customers/query/<id>', methods=['POST', 'GET'])
def query_customer(id):
    if request.method == "GET":
        customer = db.session.query(Customers).filter_by(id=id).first()
        resp = add_origin(json.dumps({'customer_code': customer.customer_code, 'company_name': customer.company_name,
                           'company_address': customer.company_address, 'comment': customer.comment}))
        return resp
    resp = add_origin(json.dumps({"code": "500", "message": "failed"}))
    return resp


@customers.route('/customers/edit/<id>', methods=['POST', 'GET'])
def edit_customer(id):
    if request.method == "POST":
        data = request.get_json(force=True)
        customer = db.session.query(Customers).filter_by(id=id).first()
        customer.company_name = data['company_name']
        customer.company_address = data['company_address']
        customer.comment = data['comment']
        db.session.commit()
        resp = add_origin(json.dumps({"code": "200", "message": "success"}))
        return resp
    resp = add_origin(json.dumps({"code": "500", "message": "failed"}))
    return resp


@customers.route('/customers/delete/<id>', methods=['POST', 'GET'])
def delete_customer(id):
    if request.method == "POST":
        customer = db.session.query(Customers).filter_by(id=id).first()
        db.session.delete(customer)
        db.session.commit()
        resp = add_origin({"code": "200", "message": "success"}))
        return resp
    resp = add_origin(json.dumps({"code": "500", "message": "failed"}))
    return resp
