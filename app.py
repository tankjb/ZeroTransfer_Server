import datetime
import os
import builtins
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)

@app.route('/userList', methods=['GET'])
def userList():
    refresh_list()
    list = []
    for c in Client.query.all():
        list.append(c.ip)
    return {'users': list}

def refresh_list():
    time = datetime.datetime.now()
    for c in Client.query.all():
        if (time - c.time).seconds > 600:
            c.delete()
    db.session.commit()
    return

@app.route('/online', methods=['GET'])
def online():
    ip = request.args.get('ip')
    refresh_list()
    exist = Client.query.filter_by(ip=ip).first()
    if not exist:
        db.session.add(Client(ip, datetime.datetime.now()))
        db.session.commit()
    return {'status': 'ok'}
        

if __name__ == "__main__":
    if not os.path.isfile("./db/db.sqlite"):
            builtins.exec("from model import *")
            builtins.exec("from app import db, app")
            builtins.exec("db.create_all(app=app)")    
    
    app.run(host='0.0.0.0',
            port='8888',
            debug = False,
            use_reloader = True)
