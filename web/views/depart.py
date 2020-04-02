#!/usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service.subject import StarkHandler
from .base import PermissionHandler


class DepartmentHandler(PermissionHandler, StarkHandler):
    list_display = ['title', ]
