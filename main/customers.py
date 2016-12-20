# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request
from main import db
from main.models import Customers
import json

customers = Blueprint('customers', __name__)


@customers.route('/customers/query/<id>', methods=['POST', 'GET'])
def query_customer(id):
    if request.method == "GET":
        customer = db.session.query(Customers).filter_by(id=id).first()
        return json.dumps({'customer_code': customer.customer_code, 'company_name': customer.company_name,
                           'company_address': customer.company_address, 'comment': customer.comment})


@customers.route('/customers/create', methods=['POST', 'GET'])
def create_customer():
    if request.method == "POST":
        data = request.get_json(force=True)
        customer = Customers(data["customer_code"], data["company_name"], data['company_address'], data['comment'])
        db.session.add(customer)
        db.session.commit()
        db.create_all()
        return "hello"


@customers.route('/customers/edit', methods=['POST', 'GET'])
def edit_customer():
    if request.method == "POST":
        data = request.get_json(force=True)
        customer = db.session.query(Customers).filter_by(id=data['id']).first()
        customer.company_name = data['company_name']
        customer.company_address = data['company_address']
        customer.comment = data['comment']
        db.session.commit()
        return "hello"


@customers.route('/customers/delete', methods=['POST', 'GET'])
def delete_customer():
    if request.method == "POST":
        data = request.get_json(force=True)
        customer = db.session.query(Customers).filter_by(id=data['id']).first()
        db.session.delete(customer)
        db.session.commit()
        return "hello"
