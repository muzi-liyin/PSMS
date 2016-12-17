from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy

psms_db = None

def create_app(config_name):
    global psms_db
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    config[config_name].init_app(app)
    databaseurl = 'mysql://%s:%s@%s:%s/%s' % (app.config["MYSQL_USER"],app.config["MYSQL_PASS"],app.config["MYSQL_HOST"],app.config["MYSQL_PORT"],app.config["MYSQL_DB"])
    app.config['SQLALCHEMY_DATABASE_URI'] =databaseurl
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    psms_db = SQLAlchemy(app)
    from users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    return app

def aa():
    print "aaa"