# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
from init import database
db=database


class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(255),nullable=False)
    distance =db.Column(db.String(255),nullable=False)
    duration =db.Column(db.String(255),nullable=False)
    averagespeed =db.Column(db.String(255),nullable=False)
    pathline =db.Column(db.Text,nullable=False)
    startpoint =db.Column(db.String(255),nullable=False)
    endpoint =db.Column(db.String(255),nullable=False)
    date=db.Column(db.DateTime,nullable=False)


    def __init__(self,username, distance ,duration, averagespeed, pathline ,startpoint, endpoint, date ):
        self.username=username
        self.distance=distance
        self.duration=duration
        self.averagespeed=averagespeed
        self.pathline=pathline
        self.startpoint=startpoint
        self.endpoint=endpoint
        self.date=date


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    recordNum=db.Column(db.INTEGER,default=0)
    isAdmin=db.Column(db.BOOLEAN,default=False)
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsers(self):
        pass

    # def addUser(self,username,password):
    #     new=User(username,password)
    #     db.session.add(new)
    #     db.session.commit()