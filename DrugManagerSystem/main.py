#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 12:55
# @Author  : hjy
# @File    : config.py
# 入口函数

from flask import Flask, render_template, request
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pass

@app.route('/regist/', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        pass


if __name__ == '__main__':
    app.run()
