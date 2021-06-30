import datetime
import os
import builtins
from flask import request
from model import *
from settings import app, db

@app.route('/userList', methods=['GET'])
def userList():
    refresh_list()
    list = []
    for c in Client.query.all():
        list.append(c.id)
        list.append(c.ip)
        
    return {'users': list}

def refresh_list():
    time = datetime.datetime.now()
    for c in Client.query.all():
        if (time - c.time).seconds > 600:
            db.session.delete(c)
    db.session.commit()
    return

@app.route('/online', methods=['GET'])
def online():
    ip = request.args.get('ip')
    id = request.args.get('id')
    exist = Client.query.filter_by(id=id).first()
    if not exist:
        db.session.add(Client(ip, id, datetime.datetime.now()))
        db.session.commit()
    return {'status': 'ok'}
        

if __name__ == "__main__":
    if not os.path.isfile("./db/db.sqlite"):
            builtins.exec("from model import *")
            builtins.exec("from settings import db, app")
            builtins.exec("db.create_all(app=app)")    
    
    app.run(host='0.0.0.0',
            port='8888',
            debug = False,
            use_reloader = True)
