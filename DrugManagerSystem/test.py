#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/1/20 11:31
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：测试

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
import config
from models import User

app = Flask(__name__)
app.config.from_object(config)

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User)

# manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()