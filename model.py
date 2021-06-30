from settings import db

class Client(db.Model):

    ip = db.Column(db.String(100), primary_key=True, unique=True)
    time = db.Column(db.DateTime)
    
    def __init__(self, ip, time):
        self.ip = ip
        self.time = time