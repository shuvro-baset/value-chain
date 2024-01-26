from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import Product
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def createProduct(request):
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_group = request.POST.get('product_group')
            uom = request.POST.get('uom')

            # ToDo: product_name unique validation check and sending message.
            product = Product.objects.create(
                product_name=product_name,
                product_group=product_group,
                uom=uom
            )
            messages.info(request, 'Product Succesfully Created.....')
            return redirect("valueChainApp:product-list")
    return render(request, 'create_product.html')


def productList(request):
    return render(request, 'product_list.html')