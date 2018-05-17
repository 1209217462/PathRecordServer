from flask import Blueprint,render_template, request,jsonify

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


def makeRes(code,msg,count,data):
    return {'code':code,'msg':msg,'count':count,'data':data}


@view.route('/webapi/users', methods=['GET'])
def returnUsers():
    if  request.method=='GET':
        page=request.args.get('page')
        pageSize=request.args.get('limit')

        # users=User.query.filter_by(isAdmin=False).order_by(User.id).paginate(10,int(pageSize),False)
        users=User.query.filter_by(isAdmin=False).paginate(int(page),int(pageSize))

        userList=users.items

        print(len(userList))


        data=[]
        for user in userList:
            print('{:<2} {} {}'.format(user.id,user.username,user.isAdmin))
            new={'id':user.id,'username':user.username,'recordNum':user.recordNum}
            data.append(new)
        print({'data':data,'msg':'用户列表'})

        code='0'
        count=db.session.query(User.id).filter(User.isAdmin==False).count()
        msg='用户列表'

        res=makeRes(code,msg,count,data)

        return jsonify(res);

@view.route('/webapi/recordByUser', methods=['GET'])
def returnRecord():
    pass
