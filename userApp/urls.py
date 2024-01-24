from django.urls import path
from . views import *

app_name = 'userApp'

urlpatterns = [
    path("", test, name="test"),
    path('login', loginUser, name='login'),
    path('logout', logoutUser, name='logout'),
    path('signup', signup, name='signup'),
    path('change-password', changePass, name='change_pass'),
]