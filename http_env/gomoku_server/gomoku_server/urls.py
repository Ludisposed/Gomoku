"""gomoku_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from game.views import (Login, Regist, Logout, OnLine, Invite, Beinvited, 
                       StartGame, CurrentGame, Move)

urlpatterns = [
    path('user/login', Login),
    path('user/regist', Regist),
    path('user/logout', Logout),
    path('user/online', OnLine),
    path('user/invite', Invite),
    path('user/invited', Beinvited),
    path('user/startgame', StartGame),
    path('user/currentgame', CurrentGame),
    path('user/move', Move),
]
