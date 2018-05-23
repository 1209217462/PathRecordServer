from flask import Blueprint,render_template, request,jsonify
from  datetime import datetime

from model import User,Record,db
from config import session

view=Blueprint('view',__name__)

@view.route('/',methods=['GET'])
def index():
    return render_template('login.html')


@view.route('/web/login',methods=['POST'])
def webLogin():
    if  request.method=='POST':
        req_username=request.form.get('username')
        req_password=request.form.get('password')
        admin = User.query.filter_by(username  = req_username,
                                    password = req_password).first()
        if  admin is not None and admin.isAdmin==True:
            session.set('admin', req_username)
            session.expire('admin', 60 * 60)  # 设置一小时过期
            print('web 登录成功')
            return render_template('main.html',admin=req_username)
        else:
            print('web 登录失败')
            return render_template('login.html',msg='用户名或密码错误')


@view.route('/web/showMain',methods=['GET'])
def showMain():
    admin=session.get('admin')
    return render_template('main.html',admin=admin)

@view.route('/web/showRecordList/<string:username>',methods=['GET'])
def showRecordList(username):
    if request.method=='GET':
        admin = session.get('admin')
        return render_template('recordList.html',admin=admin,username=username)


#返回显示轨迹的页面
@view.route('/web/showRecordDetail/<int:id>',methods=['GET'])
def showRecordDetail(id):
    if request.method=='GET':

        admin = session.get('admin')
        username=request.args.get('username')

        record = Record.query.filter_by(id=id).first()

        id=record.id
        lines=record.pathline
        start=record.startpoint
        end=record.endpoint

        Longitudes = []
        Latitudes = []

        pointsStr = lines.split(';')
        result = ''

        for pointStr in pointsStr:
            point = pointStr.split(',')
            result=result+'['+point[1]+','+point[0]+'],'

        result=result[:-1] #去掉最后一个 逗号

        return render_template('recordDetail.html',admin=admin,username=username,points=result)





@view.route('/webapi/users', methods=['GET'])
def returnUsers():
    if  request.method=='GET':
        page=request.args.get('page')
        pageSize=request.args.get('limit')

        # users=User.query.filter_by(isAdmin=False).order_by(User.id).paginate(10,int(pageSize),False)
        users=User.query.filter_by(isAdmin=False).paginate(int(page),int(pageSize))
        userList=users.items
        # print(len(userList))

        data=[]
        for user in userList:
            # print('{:<2} {} {}'.format(user.id,user.username,user.isAdmin))
            new={'id':user.id,'username':user.username,'recordNum':user.recordNum}
            data.append(new)
        # print({'data':data,'msg':'用户列表'})

        code='0'
        count=db.session.query(User.id).filter(User.isAdmin==False).count()
        msg='用户列表'

        res=makeRes(code,msg,count,data)
        return jsonify(res);


# 根据用户名获取轨迹列表
@view.route('/webapi/recordByUser/<string:username>', methods=['GET'])
def returnRecord(username):
    if request.method=='GET':
        page=request.args.get('page')
        pageSize=request.args.get('limit')

        records=Record.query.filter_by(username=username).paginate(int(page),int(pageSize))
        recordList=records.items

        data=[]
        for record in recordList:
            date= datetime.strptime(record.date,'%a, %d %b %Y %H:%M:%S GMT')
            new={'id':record.id,'date':date,'start':record.startpoint,'end':record.endpoint,'distance':record.distance,'duration':record.duration,'averageSpeed':record.averagespeed}
            data.append(new)


        code='0'
        count=db.session.query(Record.id).filter(Record.username==username).count()
        msg=username+' 的轨迹记录'

        res=makeRes(code,msg,count,data)
        return jsonify(res)

@view.route('/webapi/deleteRecord/<int:id>',methods=['GET'])
def deleteRecordByID(id):
    if request.method=='GET':
        record=Record.query.filter_by(id=id).first()
        db.session.delete(record)
        db.session.commit()
        db.session.close()
        return jsonify({'msg':'删除记录成功,id: '+str(id),'state':'success'})


@view.route('/webapi/deleteUser/<int:id>',methods=['GET'])
def deleteUserByID(id):
    if request.method=='GET':
        user=User.query.filter_by(id=id).first()
        username=user.username
        records=Record.query.filter_by(username=username).all()

        db.session.delete(user)
        for record in records:
            db.session.delete(record)
        db.session.commit()
        db.session.close()
        return jsonify({'msg':'删除用户成功\nid: '+str(id)+'\nusername: '+username,'state':'success'})



def makeRes(code,msg,count,data):
    return {'code':code,'msg':msg,'count':count,'data':data}

