import redis

# app.run()
# host='localhost'
host='0.0.0.0'
prot='5001'

# 数据库
dbName='pathrecord'
dbHost='localhost'
dbUsername='root'
dbPassword='root'

# 用户登录状态
session = redis.Redis(host='localhost',port=6379,db=0)
