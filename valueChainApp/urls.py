from django.urls import path

from . views import *

app_name = 'valueChainApp'
urlpatterns = [
    path("", home, name="index"),
    path("home/", home, name="home"),
]