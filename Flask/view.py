'''
一个简单的基于python-Flask的网页POST和GET的demo
后端以MYSQL作为数据库 ORM使用sqlalchemy作为中间件来处理前端对于后端数据库的CURD操作
by hucaigang
'''

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,Column

app = Flask(__name__)
app.config.from_object('config')#详见config.py 设置数据库
db = SQLAlchemy(app) #创建数据库对象
db.init_app(app) #启动数据库对象

#数据库处理
class Stu(db.Model):#表
    __table_name__ = 'stu' #表名
    name =  Column(String(10),primary_key=True)
    num = Column(Integer)
    score = Column(Integer)

def db_inquery(name):
    user = Stu.query.filter(Stu.name == name).first() #filter提供查询语句 first返回第一个查到的对象 name就是属性
    return "his name is %s,his score is %s and his id is %s"%(user.name,user.score,user.num)

#@app.route('/add')#增
def db_add(name,num,score):
    new_stu = Stu()#具象化
    new_stu.name = name
    new_stu.num = num
    new_stu.score = score
    db.session.add(new_stu)
    db.session.commit()
    return 'OK'

#@app.route('/update/<name>')#改
def db_update(name,num,new_score):
    new_stu = Stu.query.filter(Stu.name == name).all()
    for stu in new_stu:
        stu.score = new_score
    db.session.commit()
    return 'OK'

#app包装完毕 

#开始定义路由(url)
@app.route("/")
def hello():
    return render_template("hello.html") #访问主页

#增删改查执行部分
@app.route("/inquery",methods=['GET','POST']) #两种访问方式皆可
def inquery():
    if(request.method=='GET'):#直接访问
        return "对不起，请返回主页"
    else:
        a = request.form.get('username')
        #解析成功
        return db_inquery(a)
@app.route("/add",methods=['GET','POST']) #两种访问方式皆可
def add():
    if(request.method=='GET'):#直接访问
        return "对不起，请返回主页"
    else:
        a = request.form.get('username',type=str)
        b = request.form.get('usernum',type=int)
        c = request.form.get('userscore',type=int)
        #解析成功
        return db_add(a,b,c)
@app.route("/update",methods=['GET','POST'])
def update():
    if(request.method=='GET'):#直接访问
        return "对不起，请返回主页"
    else:
        a = request.form.get('username',type=str)
        b = request.form.get('usernum',type=int)
        c = request.form.get('new_userscore',type=int)
        #解析成功
        return db_update(a,b,c)

#form访问CURD页面
@app.route("/add_",methods=['GET','POST'])
def browse_add():
    if(request.method=='GET'):#直接访问
        return "对不起，请返回主页"
    else:
        return render_template('add.html')

@app.route("/inquery_",methods=['GET','POST'])
def browse_inquery():
    if(request.method=='GET'):#直接访问
        return "对不起，请返回主页"
    else:
        return render_template('inquery.html')

@app.route("/update_",methods=['GET','POST'])
def browse_update():
    if(request.method=='GET'):#直接访问
        return "对不起，请返回主页"
    else:
        return render_template('update.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) #本机访问