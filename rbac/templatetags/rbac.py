#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.http import QueryDict
from django.urls import reverse

from rbac.service import urls

register = Library()


@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    创建一级菜单
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


@register.inclusion_tag('rbac/multiMenu.html')
def multiMenu(request):
    """
    创建二级菜单
    """
    # 1.获取 session 中的菜单字典
    menuDict = request.session[settings.MENU_SESSION_KEY]
    # 2.对菜单字典的key进行排序
    keyList = sorted(menuDict)
    # 3.将菜单字典整理到有序字典中
    orderedDict = OrderedDict()
    for firstMenuKey in keyList:
        firstMenu = menuDict[firstMenuKey]
        firstMenu['class'] = 'nav-parent'
        for secondMenu in firstMenu['children']:
            if secondMenu['id'] == request.current_selected_permission:
                secondMenu['class'] = 'nav-active'
                firstMenu['class'] = 'nav-parent nav-expanded nav-active'
        orderedDict[firstMenuKey] = firstMenu
    return {'menuDict': orderedDict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    创建路径导航
    """
    if len(request.breadcrumb) > 1:
        request.breadcrumb[-1]["class"] = "active"
    return {'recordList': request.breadcrumb}


@register.filter
def has_permission(request, name):
    """
    判断是否有权限
    :param request:
    :param name:
    :return:
    """
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    return urls.memory_url(request, name, *args, **kwargs)
