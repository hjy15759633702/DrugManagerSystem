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
    __tablename__ = 'User'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

# 药品ID 药品编号	 药品名称 药品类别Id 药品描述(作用，药效)	单价 是否卖出 进货时间 出售时间
# 药品信息
class Drug(db.Model):
    __tablename__ = 'Drug'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    num = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    isSale = db.Column(db.Boolean(), nullable=False, default=False)
    stockDate = db.Column(db.Date(), nullable=True)
    saleDate = db.Column(db.Date(), nullable=True)
    stockPrice = db.Column(db.REAL(), nullable=True)
    salePice = db.Column(db.REAL(), nullable=True)
    drugTypeId = db.Column(db.Integer(), db.ForeignKey("DrugType.id"))  # 药品关联药品类别表id
    drugType = db.relationship("DrugType", backref=db.backref("Drug", order_by=id))

# 药品类别
class DrugType(db.Model):
    __tablename__ = 'DrugType'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    drugList = db.relationship("Drug", backref=db.backref("DrugType", order_by=id))

# class Host(Base):
#     __tablename__ = 'host1'
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     hostname = Column(String(64),unique=True,nullable=False)
#     ip_addr = Column(String(128),unique=True,nullable=False)
#     port = Column(Integer,default=22)
#     group_id = Column(Integer, ForeignKey("group1.id"))  #主机关联组id
#     #表示在group表中可以通过host_list查看host表内容，在host表中可以通过group查看group表内容
#     group = relationship("Group", backref="host")
#     #group_list = relationship("Group",back_populates="host_list") #使用populates两边名称要一致
#
# class Group(Base):
#     __tablename__ = "group1"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64),unique=True, nullable=False)
#     #host_id = Column(Integer, ForeignKey("hosts.id")) #创建一个组就要指定一个主机id变成一对一的关系
#     #host_list = relationship("Host",back_populates="group_list") #使用populates两边名称要一致,两个表对应设置名称group_list和host_list