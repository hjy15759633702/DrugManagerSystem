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
            # 获取数据列表
            drugTypes = DrugType.query.all()
            # 获取所有药品 前面一百条数据
            drugs = Drug.query.limit(100).offset(1)
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
