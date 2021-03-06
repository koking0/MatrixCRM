#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from collections import OrderedDict
from django.conf import settings
from django.urls.resolvers import RoutePattern
from django.utils.module_loading import import_string
from django.urls import URLResolver, URLPattern


def check_url_exclude(url):
    """
    排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(patterns, pre_fix, url_ordered_dict, pre_namespace):
    """
    递归的去获取URL
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in patterns:
        if isinstance(item, URLResolver):  # URL解析对象
            if item.app_name == None:  # 如果item.app_name等于None则不递归,提高效率，注意此处必须在url配置namespace
                continue
            pre_namespace = item.namespace  # 获取命名空间名
        part = item.pattern.regex.pattern.strip("^$")  # 获取当前的URL
        if isinstance(item, URLPattern):  # URL匹配对象
            if check_url_exclude((pre_fix + part).replace('\\', '')):  # 过滤自定义的url信息
                continue
            if isinstance(item.pattern, RoutePattern):  # 过滤Django本身的路由信息
                continue
            itemName = item.name
            if not itemName:
                itemName = '%s:%s' % (pre_namespace, pre_fix + part)
            url_ordered_dict[itemName] = {'name': itemName, 'url': pre_fix + part,
                                          'namespace': pre_namespace}  # 存入排序字典
        else:
            recursion_urls(item.url_patterns, pre_fix + part, url_ordered_dict, pre_namespace)
    return url_ordered_dict


def get_all_url_dict():
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """
    url_ordered_dict = OrderedDict()

    md = import_string(settings.ROOT_URLCONF)  # from luff.. import urls
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由

    return url_ordered_dict
