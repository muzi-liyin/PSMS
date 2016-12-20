# -*- coding: utf-8 -*-

from flask import Blueprint, request
from main import db
from models import Offer, History
import json
import datetime, time

offers = Blueprint('offers', __name__)

@offers.route('/create_offer', methods=['POST','GET'])
def createOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        data["createdTime"] = datetime.datetime.now().strftime("%Y-%m-%d")
        email_time = "2016-12-19 "+data["email_time"]+":00"
        data["email_time"] = time.mktime(time.strptime(email_time,'%Y-%m-%d %H:%M:%S'))

        offer = Offer(data["user_id"],data["status"],data["contract_type"],data["contract_num"],data["contract_scale"],data["os"],data["package_name"],data["app_name"],data["app_type"].encode('utf-8'),data["preview_link"],data["track_link"],data["material"],data["startTime"],data["endTime"],data["platform"],data["country"],data["price"],data["daily_budget"],data["daily_type"],data["total_budget"],data["total_type"],data["distribution"],data["authorized"],data["named_rule"],data["KPI"].encode('utf-8'),data["settlement"].encode('utf-8'),data["period"].encode('utf-8'),data["remark"].encode('utf-8'),data["email_time"],data["email_users"],data["email_tempalte"],data["createdTime"])
        try:
            db.session.add(offer)
            db.session.commit()
            db.create_all()
            for i in data['country_detail']:
                history = History(offer.id,data["user_id"],"default",data["createdTime"],i["country"],i["price"],data["price"],data["daily_budget"],data["total_type"],data["total_budget"],data["KPI"])
                db.session.add(history)
                db.session.commit()
                db.create_all()
            return json.dumps({"code":200, "message":"success"})
        except Exception as e:
            print e
            return json.dumps({"code":500, "message":"fail"})