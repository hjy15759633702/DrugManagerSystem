#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 12:55
# @Author  : hjy
# @File    : config.py
# 入口函数

from flask import Flask, render_template, request, url_for, redirect, session
import config
from models import User,Drug,DrugType
from exts import db
from sqlalchemy import func
import time

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 首页
@app.route('/')
def home():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            drugs = []
            # 获取数据列表
            drugTypes = DrugType.query.all()

            # 获取所有药品 前面一百条数据
            drugsfromDb = db.session.query(Drug.num, Drug.name, func.count('*').label('count'))\
                .group_by(Drug.num).order_by(Drug.id).limit(100).offset(0)

            # 从数据库查到列表
            for drug in drugsfromDb:
                drugs.append(drug)

            return render_template('home.html', drugTypes=drugTypes, drugs=drugs)
    return redirect(url_for('login'))

# 登录
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        checkbox = request.form.get('checkbox')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 选中以后31天内不需要登录  cookie保存
            if checkbox is not None and checkbox == 'remembered':
                session.permanent = True
            return redirect(url_for('home'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'
# 注册
@app.route('/regist/', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html', phoneTips='0', passwordTips='0')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password_again = request.form.get('password_again')

        user = User.query.filter(User.telephone == telephone).first()

        if user:
            return render_template('regist.html', phoneTips='1', passwordTips='0')
        else:
            if password != password_again:
                return render_template('regist.html', phoneTips='0', passwordTips='1')
            else:
                user = User(telephone=telephone, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

# 添加药品
@app.route('/addDrug/', methods=['POST', 'GET'])
def addDrug():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            if request.method == 'GET':
                return render_template('addDrug.html')
            else:
                # 当前时间
                # nowDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                num = request.form.get('num')
                name = request.form.get('name')
                type = request.form.get('type')
                count = request.form.get('count')
                price = request.form.get('price')
                desc = request.form.get('desc')

                try:
                    count = int(count)
                except Exception:
                    raise ValueError('count value is error!')

                # 查找数据库类别表
                drugType = DrugType.query.filter(DrugType.name == type).first()
                if drugType:
                    drugTypeId = drugType.id
                    for index in range(0,count):
                        drug = Drug(num=num, name=name, desc=desc, stockPrice=price, drugTypeId=drugTypeId)
                        drug.drugType = drugType
                        db.session.add(drug)
                        db.session.flush()  # 主要是这里，写入数据库，但是不提交
                else:
                    drugType = DrugType(name=type)
                    db.session.add(drugType)
                    db.session.commit()
                    drugTypeId = drugType.id
                    for index in range(0, count):
                        drug = Drug(num=num, name=name, desc=desc, stockPrice=price, drugTypeId=drugTypeId)
                        drug.drugType = drugType
                        db.session.add(drug)
                        db.session.flush()  # 主要是这里，写入数据库，但是不提交

                db.session.commit()
                return redirect(url_for('home'))
    return redirect(url_for('login'))

# 药品详情
@app.route('/drugDetail/<drugNum>/', methods=['GET'])
def drugDetail(drugNum):
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # 查找药品数据库
            drug = Drug.query.filter(Drug.num == drugNum).first()
            # 出售
            saleCount = Drug.query.filter(Drug.isSale == True, Drug.num == drugNum).count()
            # 库存
            stockCount = Drug.query.filter(Drug.isSale == False, Drug.num == drugNum).count()

            return render_template('drugDetail.html', drug=drug, saleCount=saleCount, stockCount=stockCount)

    return redirect(url_for('login'))

# 查找药品
@app.route('/searchDrug/', methods=['POST'])
def searchDrug():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # 判断是否是POST
            if request.method == 'POST':
                drugs = []
                keywords = request.form.get('keywords')

                drugsfromDb = Drug.query.filter(db.or_(Drug.num.like("%"+keywords+"%"),
                                                     Drug.name.like("%"+keywords+"%"),
                                                     Drug.desc.like("%" + keywords + "%")))\
                    .group_by(Drug.num).order_by(Drug.id).limit(100).offset(0)

                # 从数据库查到列表
                for drug in drugsfromDb:
                    drugs.append(drug)
                    print (drug.drugType.name)

                return render_template('searchDrug.html', drugs=drugs)

    return redirect(url_for('login'))

# 注销
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    session.clear()
    return redirect(url_for('login'))

# 获取上下文
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.debug = True
    app.run()
