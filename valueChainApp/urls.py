from django.urls import path

from . views import *

app_name = 'valueChainApp'
urlpatterns = [
    path("", home, name="index"),
    path("home/", home, name="home"),
    path("create-product/", createProduct, name="create-product"),
    path("product-list/", productList, name="product-list"),
    path("product-issue-list/", productIssueList, name="product-issue-list"),
    path("create-issue/", createProductIssue, name="create-issue"),
]