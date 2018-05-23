from flask import Blueprint, render_template, request, jsonify

from model import User,Record,db
from config import session


api=Blueprint('api',__name__)


# @api.before_request
# def  before_req():
#     url=request.url
#     words=url.split('/')
#     word=words[len(words)-1]
#     if word=='login':
#         print('收到登录请求 ')
#     elif  word=='addUser':
#         print('收到注册请求')
#     else:
#         username=request.form.get('username')
#         if session.exists(username):
#             print('session包含用户 {}'.format(username))
#         else:
#             print('未登录')
#             return jsonify({'message': u'需要登录后访问 或 无此页面'})
#


# 登录验证
@api.route('/login',methods=['POST'])
def login():
    # username=request.json.get
    print(request.method)
    if  request.method=='POST':

        req_username=request.form.get('username')
        req_password=request.form.get('password')
        # 查询数据库获取用户
        user = User.query.filter_by(username = req_username,
                                    password = req_password).first()
        # 有该用户
        if user:
            # session.get('user')
            # session['username'] = req_username
            session.set(req_username,'1')
            session.expire(req_username,60*60) #设置一小时过期
            print('用户 {} 验证通过'.format(req_username))
            print('当前session : {}'.format(session.keys()))
            return jsonify({'msg':'用户 {} 验证通过'.format(req_username),'state':'success'})
        else:
            print('没有用户 {}'.format(req_username))
            return jsonify({'msg':'用户名或密码错误！','state':'fail'})


# 用户注册
@api.route('/addUser',methods=['POST'])
def addUser():
    req_username = request.form.get('username')
    req_password = request.form.get('password')

    user = User.query.filter_by(username=req_username).first()

    if  user:
        return jsonify({'msg':'用户名已经被注册！','state':'fail'})


    newUser=User(req_username,req_password)
    db.session.add(newUser)
    db.session.commit()
    db.session.close()

    print('添加用户{}'.format(req_username))
    # 直接登录
    session.set(req_username, '1')
    session.expire(req_username, 60 * 60)  # 设置一小时过期
    return jsonify({'msg':'用户注册成功！','state':'success'})


# 上传数据
@api.route('/postData',methods=['POST'])
def postData():
    if request.method == 'POST':
        username =request.form.get('username')
        distance=request.form.get('distance')
        duration=request.form.get('duration')
        averagespeed=request.form.get('averagespeed')
        pathline=request.form.get('pathline')
        startpoint=request.form.get('startpoint')
        endpoint=request.form.get('endpoint')
        date=request.form.get('date')

        if session.get(username):
            newRecord=Record(username,distance,duration,averagespeed,pathline,startpoint,endpoint,date)
            try:
                db.session.add(newRecord)
                db.session.commit()
                db.session.close()
                print('用户 {} 添加一条记录'.format(username))
                return jsonify({'msg': '同步记录成功！', 'state': 'success'})
            except :
                db.session.rollback()
                return jsonify({'msg': 'sql 执行错误！', 'state': 'fail'})
        else:
            return jsonify({'msg': '用户未登录！', 'state': 'fail'})

# 返回轨迹的详细信息,用于安卓端回放轨迹
@api.route('/getPathlineByID/<int:id>',methods=['GET'])
def getPathLineByID(id):
    if request.method=='GET':

        record = Record.query.filter_by(id=id).first()

        id=record.id
        lines=record.pathline
        start=record.startpoint
        end=record.endpoint

        recordData={'id':id,'lines':lines,'start':start,'end':end}
        return jsonify({'msg':'','record':recordData,'state':'success'})
