# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template,safe_join, Response, send_file,make_response
from main import db
from models import Offer, History, User, Customers, Country
import json
import os
import datetime, time
import xlrd
import tempfile
from sqlalchemy import desc

offers = Blueprint('offers', __name__)

@offers.route('/api/customer_select', methods=['POST','GET'])
def customerSelect():
    if request.method == "POST":
        data = request.get_json(force=True)
        result = []
        customers = Customers.query.filter(Customers.company_name.ilike('%'+data["name"]+'%')).all()
        for i in customers:
            data = {
                "id": i.id,
                "text": i.company_name
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
        createdTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_time = "2016-12-19 "+data["email_time"]+":00"
        emailTime = float(time.mktime(time.strptime(email_time,'%Y-%m-%d %H:%M:%S')))
        userName = data["user_id"]
        user = User.query.filter_by(name=userName).first()
        userId = int(user.id)

        offer = Offer(userId,int(data["customer_id"]),data["status"],data["contract_type"],data["contract_num"],float(data["contract_scale"]),data["os"],data["package_name"],data["app_name"],data["app_type"].encode('utf-8'),data["preview_link"],data["track_link"],data["material"],data["startTime"],data["endTime"],data["platform"],data["country"],float(data["price"]),float(data["daily_budget"]),data["daily_type"],float(data["total_budget"]),data["total_type"],data["distribution"],data["authorized"],data["named_rule"],data["KPI"].encode('utf-8'),data["settlement"].encode('utf-8'),data["period"].encode('utf-8'),data["remark"].encode('utf-8'),emailTime,data["email_users"],int(data["email_tempalte"]),createdTime,createdTime)
        try:
            db.session.add(offer)
            db.session.commit()
            db.create_all()

            for i in data['country_detail']:
                history = History(offer.id,userId,"default",createdTime,status=data["status"],country=i["country"],country_price=i["price"],price=data["price"],daily_budget=float(data["daily_budget"]),daily_type=data["daily_type"],total_budget=float(data["total_budget"]),total_type=data["total_type"],KPI=data["KPI"],contract_type=data["contract_type"],contract_scale=float(data["contract_scale"]))
                db.session.add(history)
                db.session.commit()
                db.create_all()
            return json.dumps({"code":200, "message":"success"})
        except Exception as e:
            print e
            return json.dumps({"code":500, "message":"fail"})

@offers.route('/api/offer_show',methods=["POST","GET"])
def offerShow():
    offers = Offer.query.all()
    result = []
    for i in offers:
        customerId = i.customer_id
        customer = Customers.query.filter_by(id=customerId).first()
        customerName = customer.company_name   #客户名称
        status = i.status
        contract_type = i.contract_type
        os = i.os
        app_name = i.app_name
        data = {
            "offer_id": i.id,
            "status": status,
            "contract_type": contract_type,
            "os": os,
            "customer_id": customerName,
            "app_name": app_name,
            "startTime": i.startTime,
            "endTime": i.endTime,
            "country": i.country,
            "price": i.price,
            "updateTime": i.updateTime
        }
        result += [data]
    response = {
        "code": 200,
        "result": result,
        "message": "success"
    }
    return json.dumps(response)

@offers.route('/api/offer_detail/<id>', methods=["GET"])
def offerDetail(id):
    offer = Offer.query.filter_by(id=int(id)).first()
    customerId = offer.customer_id
    customer = Customers.query.filter_by(id=customerId).first()
    userId = offer.user_id
    user = User.query.filter_by(id=userId).first()
    contract_type = offer.contract_type
    if contract_type != "cpa":
        contract_scale = 0
    else:
        contract_scale = offer.contract_scale
    result = {
        "customer_id": customer.company_name,
        "status": offer.status,
        "contract_scale": contract_scale,
        "contract_num": offer.contract_num,
        "user_id": user.name,
        "os": offer.os,
        "package_name": offer.package_name,
        "app_name": offer.app_name,
        "app_type": offer.app_type,
        "preview_link": offer.preview_link,
        "track_link": offer.track_link,
        "material": offer.material,
        "startTime": offer.startTime,
        "endTime": offer.endTime,
        "platform": offer.platform,
        "country": offer.country,
        "price": offer.price,
        "daily_budget": offer.daily_budget,
        "daily_type": offer.daily_type,
        "total_budget": offer.total_budget,
        "total_type": offer.total_type,
        "distribution": offer.distribution,
        "authorized": offer.authorized,
        "named_rule": offer.named_rule,
        "KPI": offer.KPI,
        "settlement": offer.settlement,
        "period": offer.period,
        "remark": offer.remark,
        "email_time": offer.email_time,
        "email_users": offer.email_users,
        "email_tempalte": offer.email_tempalte
    }
    historties = History.query.filter(History.offer_id==id,History.country != "").all()
    countries = []
    for i in historties:
        country = i.country
        countries.append(country)
    countries = list(set(countries))
    country_detail = []
    for i in countries:
        historty = History.query.filter(History.offer_id==id, History.country == i).order_by(desc(History.createdTime)).first()
        country = historty.country
        country_price = historty.country_price
        detail = {
            "country": country,
            "price": country_price
        }
        country_detail += [detail]
    result["country_detail"] = country_detail
    response = {
        "code": 200,
        "result": result,
        "message": "success"
    }
    return json.dumps(response)

@offers.route('/api/update_offer', methods=["POST","GET"])
def updateOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        offer = Offer.query.filter_by(id=int(data["offer_id"])).first()
        flag = data["flag"]
        if offer is not None:
            try:
                offer.updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                        history = History(offer.id, offer.user_id, "update", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), country=i["country"], country_price=i["price"],price=float(data["price"]) if data["price"] != "" else 0,status=data["status"], daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,daily_type = data["daily_type"], total_budget=float(data["total_budget"]) if data['total_budget']!="" else 0,total_type=data["total_type"],KPI=data["KPI"],contract_type=data["contract_type"],contract_scale=float(data["contract_scale"]))
                        db.session.add(history)
                        db.session.commit()
                        db.create_all()
                else:
                    history = History(offer.id, offer.user_id, "update", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),price=float(data["price"]) if data["price"] != "" else 0,status=data["status"], daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,daily_type = data["daily_type"], total_budget=float(data["total_budget"]) if data['total_budget']!="" else 0,total_type=data["total_type"],KPI=data["KPI"],contract_type=data["contract_type"],contract_scale=float(data["contract_scale"])if data["contract_scale"] != "" else 0)
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
                    user = User.query.filter(User.id==user_id).first()
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
                    user = User.query.filter(User.id == user_id).first()
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
                    user = User.query.filter(User.id==user_id).first()
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
                    user = User.query.filter(User.id==user_id).first()
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
                    user = User.query.filter(User.id==user_id).first()
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
                    user = User.query.filter(User.id==user_id).first()
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

#导入国家对应的时间
@offers.route("/api/country_time", methods=["POST","GET"])
def importCountry():
    if request.method == "POST":
        # file_url = request.files["file"][0]
        # tempfd, tempname = tempfile.mkstemp('.xls')
        # os.write(tempfd, file_url['body'])
        tempname = "/Users/liyin/Desktop/time.xlsx"
        try:
            data = xlrd.open_workbook(tempname)
        except Exception,e:
            print e
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        colnames = table.row_values(0)
        # print table.row_values(2)[0]
        # print table.row_values(2)[1]
        date = []
        data = []
        for rownum in range(2,nrows):
            for col in range(1,ncols):
                date.append(table.row_values(rownum)[col])
            result = {
                "country": table.row_values(rownum)[0],
                "date": date
            }

        tables = []
        # for rownum in range(1,nrows):
        #     row = table.row_values(rownum)
        #     if row:
        #         app = {}
        #         for i in range(len(colnames)):
        #             app[colnames[i]] = row[i]
        #         tables.append(app)
        #
        # for row in tables:
        #     print row

@offers.route('/static/<path:filename>')
def static_file_for_console(filename):
    filename = safe_join("../static", filename)
    if not os.path.isabs(filename):
        filename = os.path.join(offers.root_path, filename)
    if not os.path.isfile(filename):
        return Response(), 404
    return send_file(filename, conditional=True)

@offers.route('/<path>')
def today(path):
    base_dir = os.path.dirname(__file__)
    resp = make_response(open(os.path.join(base_dir, path)))
    resp.headers["Content-type"]="application/json;charset=UTF-8"
    return resp