#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 17:53
# @Author  : hjy
# @File    : models.py
# 数据模型

from exts import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)