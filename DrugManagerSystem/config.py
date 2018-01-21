#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 12:55
# @Author  : hjy
# @File    : config.py
# 配置文件

import os
# DEBUG模式
DEBUG = True
SECRET_KEY = os.urandom(24)

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'drugManagerSystem'
USERNAME = 'root'
PASSWORD = 'hjy'
DB_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
SQLALCHEMY_COMMIT_ON_TEARDOWN = True