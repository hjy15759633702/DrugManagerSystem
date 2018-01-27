#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/1/20 11:31
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：测试


from datetime import datetime
import datetime
import time

if __name__ == '__main__':
    print (datetime.datetime.now())
    print (time.time())
    print (time.localtime())
    print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
