#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 12:55
# @Author  : hjy
# @File    : config.py
# 入口函数

from flask import Flask, render_template, request, url_for, redirect, session
import config
from models import User,Drug,DrugType,Sale,Account
from exts import db
from sqlalchemy import func
from sqlalchemy import extract
import time
import datetime

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

# 添加药品类别
@app.route('/addDrugType/', methods=['POST', 'GET'])
def addDrugType():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            if request.method == 'GET':
                drugTypeTips = None
                drugTypes = []
                # 获取数据列表
                drugTypesfromDb = DrugType.query.all()
                # 从数据库查到列表
                for drugType in drugTypesfromDb:
                    count = Drug.query.filter(Drug.drugTypeId == drugType.id).count()
                    drugType.set_count(count)
                    drugTypes.append(drugType)
                return render_template('addDrugType.html', drugTypes=drugTypes, drugTypeTips=drugTypeTips)
            else:
                drugTypeName = request.form.get('drugTypeName')
                drugType = DrugType.query.filter(DrugType.name == drugTypeName).first()
                if drugType:
                    drugTypeTips = u'该药品类别已经存在，更改其他类别名称吧!'
                else:
                    drugTypeTips = u'该药品类别已经添加成功!'
                    drugType = DrugType(name=drugTypeName)
                    db.session.add(drugType)
                    db.session.commit()

                drugTypes = []
                # 获取数据列表
                drugTypesfromDb = DrugType.query.all()
                # 从数据库查到列表
                for drugType in drugTypesfromDb:
                    count = Drug.query.filter(Drug.drugTypeId == drugType.id).count()
                    drugType.set_count(count)
                    drugTypes.append(drugType)

                return render_template('addDrugType.html', drugTypes=drugTypes, drugTypeTips=drugTypeTips)

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

# 删除药品类别
@app.route('/deleteDrugType/<drugTypeId>/', methods=['GET','POST'])
def deleteDrugType(drugTypeId):
    print ('drugTypeId:'+drugTypeId)
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # 查找药品数据库
            drugType = DrugType.query.filter(DrugType.id == drugTypeId).first()
            if drugType:
                # 删除药品
                drugs = Drug.query.filter(Drug.drugTypeId == drugType.id).all()
                for drug in drugs:
                    db.session.delete(drug)
                    db.session.flush()
                db.session.delete(drugType)
                db.session.flush()
                db.session.commit()
            return redirect(url_for('addDrugType'))

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

                return render_template('searchDrug.html', drugs=drugs)

    return redirect(url_for('login'))

# 进货页面
@app.route('/addStock/<drugNum>/', methods=['GET','POST'])
def addStock(drugNum):
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # 判断是否是POST
            if request.method == 'GET':
                drug = Drug.query.filter(Drug.num == drugNum).first()
                return render_template('addStock.html', drug=drug)
            else:
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
                    for index in range(0, count):
                        drug = Drug(num=num, name=name, desc=desc, stockPrice=price, drugTypeId=drugTypeId)
                        drug.drugType = drugType
                        db.session.add(drug)
                        db.session.flush()  # 主要是这里，写入数据库，但是不提交
                db.session.commit()

                return redirect(url_for('addStockHome'))
    return redirect(url_for('login'))

# 进货首页
@app.route('/addStockHome/', methods=['GET'])
def addStockHome():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            drugs = []
            # 获取所有药品 前面一百条数据
            drugsfromDb = db.session.query(Drug.num, Drug.name, func.count('*').label('count')) \
                .group_by(Drug.num).order_by(Drug.id).all()

            # 从数据库查到列表
            for drug in drugsfromDb:
                drugs.append(drug)

            return render_template('addStockHome.html', drugs=drugs)
    return redirect(url_for('login'))


# 进货历史
@app.route('/addStocHistory/', methods=['GET'])
def addStocHistory():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            drugs = []
            drugsfromDb = db.session.query(Drug.num, Drug.name, Drug.stockDate,
                                           func.count('*').label('count')).group_by(Drug.stockDate).order_by(db.desc(Drug.stockDate))
            # 从数据库查到列表
            for drug in drugsfromDb:
                drugs.append(drug)
            return render_template('addStockHis.html', drugs=drugs)

    return redirect(url_for('login'))

# 退货操作
@app.route('/backStock/<drugNum>/<stockDate>', methods=['GET'])
def backStock(drugNum, stockDate):
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            drugsfromDb = Drug.query.filter(db.and_(Drug.num == drugNum, Drug.stockDate == stockDate)).all()
            # 从数据库查到列表
            for drug in drugsfromDb:
                db.session.delete(drug)
                db.session.commit()

            return redirect(url_for('addStocHistory'))

    return redirect(url_for('login'))

# 购买首页
@app.route('/saleDrugHome/', methods=['GET'])
def saleDrugHome():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            drugs = []
            # 获取所有药品 药品编号进行分组查询  查找每种药品库存多少
            drugsfromDb = db.session.query(Drug.num, Drug.name, func.count('*').label('count')).group_by(Drug.num).all()
            # 对购买表 药品编号进行分组查询  查找每种药品选购多少
            salesfromDb = db.session.query(Sale.drugNum, func.count('*').label('count'))\
                .filter(Sale.userId == user_id).group_by(Sale.drugNum).all()

            for d in drugsfromDb:
                drug = {}
                count = d.count
                drug['num'] = d.num
                drug['name'] = d.name
                for s in salesfromDb:
                    if d.num == s.drugNum:
                        if d.count - s.count >= 0:
                            count = d.count - s.count
                drug['count'] = count
                drugs.append(drug)
            return render_template('saleDrugHome.html', drugs=drugs)
    return redirect(url_for('login'))

# 购买
@app.route('/saleDrug/<drugNum>/', methods=['GET','POST'])
def saleDrug(drugNum):
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # 判断是否是POST
            if request.method == 'GET':
                count = 0
                drug = {}
                # 查找药品编号  卖出价格 数量
                drugsfromDb = db.session.query(Drug.num, Drug.name, Drug.stockPrice, func.count('*').label('count')).filter(Drug.num == drugNum).first()
                salesfromDb = db.session.query(func.count('*').label('count')).filter(db.and_(Sale.drugNum == drugNum, Sale.userId == user_id)).first()

                drug['name'] = drugsfromDb.name
                drug['num'] = drugsfromDb.num
                drug['stockPrice'] = drugsfromDb.stockPrice

                if drugsfromDb.count - salesfromDb.count >= 0:
                    count = drugsfromDb.count - salesfromDb.count

                drug['count'] = count

                return render_template('saleDrug.html', drug=drug)
            else:
                num = request.form.get('num')
                saleCount = request.form.get('saleCount')

                for index in range(int(saleCount)):
                    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    sale = Sale(time=nowTime, userId=user.id, drugNum=num)
                    sale.user = user
                    db.session.add(sale)
                    db.session.commit()

                return redirect(url_for('showSaleDrug'))

    return redirect(url_for('login'))

# 查看选购
@app.route('/showSaleDrug/', methods=['GET'])
def showSaleDrug():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            showSales = []
            allCount = 0
            sales = db.session.query(Sale.id, Sale.drugNum, Sale.time, Sale.userId, func.count('*').label('count')).filter(Sale.userId == user_id).group_by(Sale.drugNum).all()
            for sale in sales:
                showSale = {}
                drug = Drug.query.filter(Drug.num == sale.drugNum).first()
                user = User.query.filter(User.id == sale.userId).first()
                showSale['id'] = sale.id
                showSale['num'] = sale.drugNum
                showSale['name'] = drug.name
                showSale['stockPrice'] = drug.stockPrice
                showSale['saleCount'] = sale.count
                showSale['money'] = sale.count * drug.stockPrice
                allCount = allCount + sale.count * drug.stockPrice
                #showSale['time'] = sale.time
                showSale['username'] = user.username
                showSales.append(showSale)
            return render_template('showSaleDrug.html', showSales=showSales, allCount=allCount)

    return redirect(url_for('login'))

# 删除选购
@app.route('/deleteSale/<num>', methods=['GET'])
def deleteSale(num):
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            sales = Sale.query.filter(db.and_(Sale.drugNum == num, Sale.userId == user_id)).all()
            for sale in sales:
                db.session.delete(sale)
            db.session.commit()
            return redirect(url_for('showSaleDrug'))

    return redirect(url_for('login'))

# 清除选购
@app.route('/clearSale/', methods=['GET'])
def clearSale():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            sales = Sale.query.filter(Sale.userId == user_id).all()
            for sale in sales:
                db.session.delete(sale)
                db.session.flush()
            db.session.commit()

            return redirect(url_for('saleDrugHome'))

    return redirect(url_for('login'))

# 结账英语
@app.route('/account/', methods=['GET'])
def account():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            nowDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 查出当前管理员所有的选购药品进行结账
            sales = db.session.query(Sale.drugNum, Sale.userId, func.count('*').label('count')).filter(Sale.userId == user_id).group_by(Sale.drugNum).all()
            for sale in sales:
                # 结账之前，查询一下库存量是否充足(之间选购已经判断过了)
                drugs = Drug.query.filter(db.and_(Drug.num == sale.drugNum, Drug.isSale == False)).all()
                for i in range(len(drugs)):
                    if i > sale.count-1:
                        break
                    drug = drugs[i]
                    Drug.query.filter(Drug.id == drug.id).update({Drug.isSale: True, Drug.saleDate: nowDate})
                    account = Account(drugId=drug.id, userId=user_id, drugNum=drug.num, time=nowDate)
                    db.session.add(account)
                    db.session.commit()

                # 删除选购表数据
                salesFromDb = Sale.query.filter(db.and_(Sale.drugNum == sale.drugNum, Sale.userId == user_id)).all()
                for i in range(len(salesFromDb)):
                    db.session.delete(salesFromDb[i])
                    db.session.flush()

                db.session.commit()

            return redirect(url_for('saleManageHome'))

    return redirect(url_for('login'))

# 销售管理首页
@app.route('/saleManageHome/', methods=['GET'])
def saleManageHome():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            acs = db.session.query(Account.drugId, Account.userId, Account.time, func.count('*').label('count')).group_by(Account.time, Account.drugNum).all()
            accounts = []
            for a in acs:
                account = {}
                drug = Drug.query.filter(Drug.id == a.drugId).first()
                user = User.query.filter(User.id == a.userId).first()
                account['name'] = drug.name
                account['stockPrice'] = drug.stockPrice
                account['count'] = a.count
                account['time'] = a.time
                account['money'] = a.count * drug.stockPrice
                account['username'] = user.username
                accounts.append(account)

            return render_template('saleManageHome.html', accounts=accounts)
    return redirect(url_for('login'))

# 今日明细
@app.route('/saleOnToday/', methods=['GET'])
def saleOnToday():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            cur = datetime.datetime.now()
            acs = db.session.query(Account.drugId, Account.userId, Account.time, func.count('*').label('count'))\
                .filter(db.and_(extract('year', Account.time) == cur.year, extract('month', Account.time) == cur.month, extract('day', Account.time) == cur.day))\
                .group_by(Account.time, Account.drugNum).all()
            accounts = []
            for a in acs:
                account = {}
                drug = Drug.query.filter(Drug.id == a.drugId).first()
                user = User.query.filter(User.id == a.userId).first()
                account['name'] = drug.name
                account['stockPrice'] = drug.stockPrice
                account['count'] = a.count
                account['time'] = a.time
                account['money'] = a.count * drug.stockPrice
                account['username'] = user.username
                accounts.append(account)
            return render_template('saleOnToday.html', accounts=accounts)
    return redirect(url_for('login'))

# 日期查询
@app.route('/saleSearchByDay/', methods=['GET','POST'])
def saleSearchByDay():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            if request.method == 'GET':
                # 查询今日的明细
                cur = datetime.datetime.now()
                acs = db.session.query(Account.drugId, Account.userId, Account.time, func.count('*').label('count')) \
                    .filter(
                    db.and_(extract('year', Account.time) == cur.year, extract('month', Account.time) == cur.month,
                            extract('day', Account.time) == cur.day)) \
                    .group_by(Account.time, Account.drugNum).all()
                accounts = []
                for a in acs:
                    account = {}
                    drug = Drug.query.filter(Drug.id == a.drugId).first()
                    user = User.query.filter(User.id == a.userId).first()
                    account['name'] = drug.name
                    account['stockPrice'] = drug.stockPrice
                    account['count'] = a.count
                    account['time'] = a.time
                    account['money'] = a.count * drug.stockPrice
                    account['username'] = user.username
                    accounts.append(account)
                return render_template('saleSearchByDay.html', accounts=accounts, startTime=cur.strftime("%Y-%m-%d"), endTime=cur.strftime("%Y-%m-%d"))
            else:
                startTime = request.form.get('startTime')
                endTime = request.form.get('endTime')
                # 时间转换
                st = time.strptime(startTime, "%Y-%m-%d")
                et = time.strptime(endTime, "%Y-%m-%d")
                sy, sm, sd = st[0:3]
                ey, em, ed = et[0:3]
                # 查询今日的明细
                cur = datetime.datetime.now()
                acs = db.session.query(Account.drugId, Account.userId, Account.time, func.count('*').label('count')) \
                    .filter(Account.time.between(startTime,endTime))\
                    .group_by(Account.time, Account.drugNum).all()
                accounts = []
                for a in acs:
                    account = {}
                    drug = Drug.query.filter(Drug.id == a.drugId).first()
                    user = User.query.filter(User.id == a.userId).first()
                    account['name'] = drug.name
                    account['stockPrice'] = drug.stockPrice
                    account['count'] = a.count
                    account['time'] = a.time
                    account['money'] = a.count * drug.stockPrice
                    account['username'] = user.username
                    accounts.append(account)
                return render_template('saleSearchByDay.html', accounts=accounts)
    return redirect(url_for('login'))

# 销售排行
@app.route('/saleOrder/', methods=['GET'])
def saleOrder():
    # 判断用户是否登录
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return render_template('saleOrder.html')

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
