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

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 首页
@app.route('/')
def home():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return render_template('home.html')
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
                user = User(telephone = telephone,username = username,password = password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

# 添加药品
@app.route('/addDrug/', methods=['POST', 'GET'])
def addDrug():
    if request.method == 'GET':
        return render_template('addDrug.html')
    else:
        typeId = None
        num = request.form.get('num')
        name = request.form.get('name')
        type = request.form.get('type')
        count = request.form.get('count')
        price = request.form.get('price')
        desc = request.form.get('desc')

        # 查找数据库类别表
        drugType = DrugType.query.filter(DrugType.name == type).first()
        if drugType:
            drug = Drug(num=num,name=name,)
        drug = Drug.query.filter(User.id == user_id).first()

        user = User(telephone=telephone, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        num = db.Column(db.String(50), nullable=False)
        name = db.Column(db.String(50), nullable=False)
        desc = db.Column(db.String(500), nullable=False)
        isSale = db.Column(db.Boolean(), nullable=False, default=False)
        stockDate = db.Column(db.Date(), nullable=True)
        saleDate = db.Column(db.Date(), nullable=True)
        stockPrice = db.Column(db.REAL(), nullable=True)
        salePice = db.Column(db.REAL(), nullable=True)
        # foreignkey药品关联药品类别表id
        drugTypeId = db.Column(db.Integer(), db.ForeignKey('drugType.id'))

        return redirect(url_for('login'))

    return render_template('addDrug.html')

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
