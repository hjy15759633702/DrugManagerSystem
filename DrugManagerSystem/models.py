#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 17:53
# @Author  : hjy
# @File    : models.py
# 数据模型

from exts import db

# ID 手机号码 用户名	密码
# 用户信息
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

# 药品ID 药品编号	 药品名称 药品类别Id 药品描述(作用，药效)	单价 是否卖出 进货时间 出售时间
# 药品信息
class Drug(db.Model):
    __tablename__ = 'drug'
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

# 药品类别
class DrugType(db.Model):
    __tablename__ = 'drugType'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    # relationship的作用是将药品和药品类别连接起来
    drugs = db.relationship('Drug', backref='drugType', lazy='dynamic')