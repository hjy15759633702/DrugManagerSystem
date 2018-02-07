#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 17:53
# @Author  : hjy
# @File    : models.py
# 数据模型

from exts import db
from datetime import datetime
# ID 手机号码 用户名	密码
# 用户信息
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# 药品ID 药品编号	 药品名称 药品类别Id 药品描述(作用，药效)	单价 是否卖出 进货时间 出售时间
# 药品信息
class Drug(db.Model):
    __tablename__ = 'drug'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    num = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    isSale = db.Column(db.Boolean(), nullable=False, default=False)
    # isChoose = db.Column(db.Boolean(), nullable=False, default=False)
    stockDate = db.Column(db.DateTime(), default=datetime.now)
    stockPrice = db.Column(db.REAL(), nullable=True, default=0)
    saleDate = db.Column(db.DateTime(), nullable=True)
    salePice = db.Column(db.REAL(), nullable=True, default=0)
    # foreignkey药品关联药品类别表id
    drugTypeId = db.Column(db.Integer(), db.ForeignKey('drugType.id'))
    drugType = db.relationship('DrugType', backref='drug')

# 药品类别
class DrugType(db.Model):
    __tablename__ = 'drugType'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    # relationship的作用是将药品和药品类别连接起来
    # drugs = db.relationship('Drug', backref='drugType', lazy='dynamic')

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

# 选购表
class Sale(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # 选购时间
    time = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    # 用户外键
    userId = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', backref='sale')
    # 药品外键
    # drugId = db.Column(db.Integer(), db.ForeignKey('drug.id'))
    # 药品编号
    drugNum = db.Column(db.String(50), nullable=False)

    # drug = db.relationship('Drug', backref='sale')
    # 购买数量
    # saleCount = db.Column(db.Integer(), nullable=False)

# 账户表
class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # 结账流水号 后期银行对接  可以用上 先架构着  默认是8个0
    accountNo = db.Column(db.String(50), nullable=False, default='00000000')
    # 结账时间
    time = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    # 用户外键
    userId = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', backref='account')
    # 药品外键
    drugId = db.Column(db.Integer(), db.ForeignKey('drug.id'))
    drugNum = db.Column(db.String(50), nullable=False)
    # 药品编号
    drug = db.relationship('Drug', backref='account')
