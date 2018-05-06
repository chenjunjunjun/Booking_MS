#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 17-12-7 下午4:48
# @Author  : 无敌小龙虾
# @File    : urls.py.py
# @Software: PyCharm


from django.conf.urls import url
from . import views

app_name = 'booking'

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),
    url(r'^register/$', views.Register, name='register'),
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^detail/$', views.DetailView, name='detail'),
    url(r'^book/$', views.Booking, name='book'),
    url(r'^result/$', views.resultView, name='result'),
    # url(r'^count/$', views.statisticView, name='statistic'),
    url(r'^count/department/$',views.DstatisView, name='dstatis'),
    url(r'^count/magazine/$', views.MstatisView, name='mstatis'),
    url(r'^count/person/$', views.PstatisView, name='pstatis')
]
