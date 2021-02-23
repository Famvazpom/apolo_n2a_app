# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('',views.resultsView.as_view(),name='results'),
    path('export/<int:etype>',views.export.as_view(),name='export')
]
