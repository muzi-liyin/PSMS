# -*- coding: utf-8 -*-

from flask import Blueprint, request
from main import db
from models import Offer, History, Users, Customers, Country
import json
import datetime, time
import xlrd

offers = Blueprint('offers', __name__)

@offers.route('/api/customer_select', methods=['POST','GET'])
def customerSelect():
    if request.method == "POST":
        data = request.get_json(force=True)
        result = []
        customers = Customers.query.filter(Customers.company_name.ilike('%'+data["name"]+'%')).all()
        for i in customers:
            data = {
                "customer_id": i.id,
                "company_name": i.company_name
            }
            result += [data]
        response = {
            "code": 200,
            "result": result
        }
        return json.dumps(response)

@offers.route('/api/country_select', methods=["POST","GET"])
def countrySelect():
    if request.method == "POST":
        data = request.get_json(force=True)
        result = []
        if u'\u4e00' <= data["name"] <= u'\u9fff':
            countries = Country.query.filter(Country.chinese.ilike('%'+data["name"]+'%')).all()
        else:
            countries = Country.query.filter(Country.british.ilike('%'+data["name"]+'%')).all()
        for i in countries:
            data = {
                "id": i.shorthand,
                "text": i.chinese
            }
            result += [data]
        response = {
            "code": 200,
            "result": result,
            "message": "success"
        }
        return json.dumps(response)
    else:
        return json.dumps({"code": 500, "message":"The request type wrong!"})

@offers.route('/api/create_offer', methods=['POST','GET'])
def createOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        data["createdTime"] = datetime.datetime.now().strftime("%Y-%m-%d")
        email_time = "2016-12-19 "+data["email_time"]+":00"
        data["email_time"] = time.mktime(time.strptime(email_time,'%Y-%m-%d %H:%M:%S'))

        offer = Offer(int(data["user_id"]),int(data["customer_id"]),data["status"],data["contract_type"],data["contract_num"],float(data["contract_scale"]),data["os"],data["package_name"],data["app_name"],data["app_type"].encode('utf-8'),data["preview_link"],data["track_link"],data["material"],data["startTime"],data["endTime"],data["platform"],data["country"],float(data["price"]),float(data["daily_budget"]),data["daily_type"],float(data["total_budget"]),data["total_type"],data["distribution"],data["authorized"],data["named_rule"],data["KPI"].encode('utf-8'),data["settlement"].encode('utf-8'),data["period"].encode('utf-8'),data["remark"].encode('utf-8'),data["email_time"],data["email_users"],data["email_tempalte"],data["createdTime"],data["createdTime"])

        try:
            db.session.add(offer)
            db.session.commit()
            db.create_all()

            for i in data['country_detail']:
                history = History(offer.id,int(data["user_id"]),"default",data["createdTime"],status=data["status"],country=i["country"],country_price=i["price"],price=data["price"],daily_budget=float(data["daily_budget"]),daily_type=data["daily_type"],total_budget=float(data["total_budget"]),total_type=data["total_type"],KPI=data["KPI"],contract_type=data["contract_type"],contract_scale=float(data["contract_scale"]))
                db.session.add(history)
                db.session.commit()
                db.create_all()
            return json.dumps({"code":200, "message":"success"})
        except Exception as e:
            print e
            return json.dumps({"code":500, "message":"fail"})

@offers.route('/api/update_offer', methods=["POST","GET"])
def updateOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        offer = Offer.query.filter_by(id=int(data["offer_id"])).first()
        flag = data["flag"]
        if offer is not None:
            try:
                offer.updateTime = datetime.datetime.now().strftime("%Y-%m-%d")
                offer.status = data["status"] if data["status"] != "" else offer.status
                offer.contract_type = data["contract_type"] if data["contract_type"] != "" else offer.contract_type
                offer.contract_scale = float(data["contract_scale"]) if data["contract_scale"] != "" else offer.contract_scale
                offer.country = data["country"] if data["country"] != "" else offer.country
                offer.price = float(data["price"]) if data["price"] != "" else offer.price
                offer.daily_budget = float(data["daily_budget"]) if data["daily_budget"] != "" else offer.daily_budget
                offer.daily_type = data["daily_type"] if data["daily_type"] != "" else offer.daily_type
                offer.total_budget = float(data["total_budget"]) if data["total_budget"] != "" else offer.total_budget
                offer.total_type = data["total_type"] if data["total_type"] != "" else offer.total_type
                offer.KPI = data["KPI"].encode('utf-8') if data["KPI"] != "" else offer.KPI
                db.session.add(offer)
                db.session.commit()
                if "country_detail" in flag:
                    for i in data['country_detail']:
                        history = History(offer.id, offer.user_id, "update", datetime.datetime.now().strftime("%Y-%m-%d"), country=i["country"], country_price=i["price"],price=float(data["price"]) if data["price"] != "" else 0,status=data["status"], daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,daily_type = data["daily_type"], total_budget=float(data["total_budget"]) if data['total_budget']!="" else 0,total_type=data["total_type"],KPI=data["KPI"],contract_type=data["contract_type"],contract_scale=float(data["contract_scale"]))
                        db.session.add(history)
                        db.session.commit()
                        db.create_all()
                else:
                    history = History(offer.id, offer.user_id, "update", datetime.datetime.now().strftime("%Y-%m-%d"),price=float(data["price"]) if data["price"] != "" else 0,status=data["status"], daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,daily_type = data["daily_type"], total_budget=float(data["total_budget"]) if data['total_budget']!="" else 0,total_type=data["total_type"],KPI=data["KPI"],contract_type=data["contract_type"],contract_scale=float(data["contract_scale"])if data["contract_scale"] != "" else 0)
                    db.session.add(history)
                    db.session.commit()
                    db.create_all()

                return json.dumps({"code": 200, "message":"success"})
            except Exception as e:
                print e
                return json.dumps({"code": 500, "message": "fail"})
        else:
            return json.dumps({"code":400, "message": "offer is None"})

@offers.route("/api/history", methods=["POST","GET"])
def historty():
    if request.method == "POST":
        data = request.get_json(force=True)
        offer_id = int(data["offer_id"])
        flag = data["flag"]
        if flag == "country_detail":
            country = []
            result = []
            history = History.query.filter(History.offer_id==offer_id,History.country!="")
            for i in history:
                country.append(i.country)
            country = list(set(country))
            print country
            for i in country:
                detail = []
                history_country = History.query.filter(History.offer_id==offer_id,History.country==i)
                for j in history_country:
                    createdTime = j.createdTime
                    country_price = j.country_price
                    country_data = {
                        "country_price": country_price,
                        "createdTime": createdTime
                    }
                    detail += [country_data]
                result += [{"country":i,"detail":detail}]
            response = {
                "code": 200,
                "result": result
            }
            return json.dumps(response)
        else:
            result = []
            if flag == "status":
                history = History.query.filter(History.offer_id==offer_id,History.status!="")
                for i in history:
                    status = i.status
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = Users.query.filter(Users.id==user_id).first()
                    detail = {
                        "username": user.name,
                        "status": status,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "contract_type":
                history = History.query.filter(History.offer_id==offer_id,History.contract_type!="")
                for i in history:
                    contract_type = i.contract_type
                    contract_scale = i.contract_scale
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = Users.query.filter(Users.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "contract_type": contract_type,
                        "contract_scale": contract_scale,
                        "createdTime": createdTime
                    }
                    result += [detail]

            elif flag == "price":
                history = History.query.filter(History.offer_id==offer_id,History.price!="")
                for i in history:
                    price = i.price
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = Users.query.filter(Users.id==user_id).first()
                    detail = {
                        "username": user.name,
                        "price": price,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "daily_budget":
                history = History.query.filter(History.offer_id==offer_id,History.daily_budget!="")
                for i in history:
                    daily_budget = i.daily_budget
                    daily_type = i.daily_type
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = Users.query.filter(Users.id==user_id).first()
                    detail = {
                        "username": user.name,
                        "daily_budget": daily_budget,
                        "daily_type": daily_type,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "total_budget":
                history = History.query.filter(History.offer_id==offer_id,History.total_budget!="")
                for i in history:
                    total_budget = i.total_budget
                    total_type = i.total_type
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = Users.query.filter(Users.id==user_id).first()
                    detail = {
                        "username": user.name,
                        "total_budget": total_budget,
                        "total_type": total_type,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "KPI":
                history = History.query.filter(History.offer_id == offer_id, History.total_budget != "")
                for i in history:
                    KPI = i.KPI
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = Users.query.filter(Users.id==user_id).first()
                    detail = {
                        "username": user.name,
                        "KPI": KPI,
                        "createdTime": createdTime
                    }
                    result += [detail]
                    print
            f = lambda x, y: x if y in x else x + [y]
            response = {
                "code": 200,
                "result": reduce(f, [[], ] + result)
            }
            return json.dumps(response)

#导入国家表
@offers.route("/api/country")
def country():
    wb = xlrd.open_workbook("/Users/liyin/Downloads/1.xlsx")

    wb.sheet_names()
    sh = wb.sheet_by_name(u'Sheet1')
    count = 0
    for rownum in range(sh.nrows):
        country = Country(sh.row_values(rownum)[0], sh.row_values(rownum)[1], sh.row_values(rownum)[2])
        db.session.add(country)
        db.session.commit()
        db.create_all()
        count += 1

    print count