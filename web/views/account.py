#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from web import models
from web.utils.md5 import getMd5
from rbac.service.initPermission import initPermission


def login(request):
    """
    用户登录
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == "POST":
        # 1.获取前端发送的用户名和密码
        username = request.POST.get('username')
        password = getMd5(request.POST.get('password', ''))
        # 2.根据用户名和密码去用户表中获取用户对象
        user = models.UserInfo.objects.filter(name=username, password=password).first()
        # 3.如果用户不存在，返回错误信息
        if not user:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        # 4.如果用户存在，初始化该用户的权限信息到 session 中
        request.session['user_info'] = {'id': user.id, 'nickname': user.nickname}
        initPermission(user, request)
        # 5.重定向到 index 页面
        return redirect('/index/')


def logout(request):
    """
    用户注销
    """
    request.session.delete()
    return redirect('/login/')


def index(request):
    if request.session["user_info"]:
        return render(request, 'index.html')
    else:
        return redirect('/login/')
