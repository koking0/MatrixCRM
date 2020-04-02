#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib


def getMd5(origin):
    md5 = hashlib.md5()
    md5.update(origin.encode('utf-8'))
    return md5.hexdigest()
