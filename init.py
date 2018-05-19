from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from config  import *

app = Flask(__name__)
app.secret_key="qwer"


# 数据库 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+dbUsername+':'+dbPassword+'@'+dbHost+'/'+dbName+'?charset=utf8'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Falsed
app.config['SQLALCHEMY_ECHO']=True  #log显示sql语句
app.config['JSON_AS_ASCII'] = False #支持中文
app.config['SQLALCHEMY_POOL_RECYCLE']= 60*60 # 设置自动回收连接的时间为一小时
database=SQLAlchemy(app)# db对象是 SQLAlchemy 类的实例