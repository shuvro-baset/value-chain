from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from .models import Product, ProductIssue, RawMaterials, PurchaseOrder, PurchaseRecipt, SalesOrder, DeliveryChallan, StockEntry
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
def createProductIssue(request):
    products = Product.objects.all()
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            description = request.POST.get('description')
            total_qty = request.POST.get('total_qty')
            product_id = request.POST.get('product')  # Assuming 'product' is the product ID

            # Retrieve the Product instance corresponding to the selected product ID
            product = get_object_or_404(Product, pk=product_id)
            print('=============', product)
            # ToDo: product_name unique validation check and sending message.
            product_issue = ProductIssue.objects.create(
                description=description,
                total_qty=total_qty,
                product=product,
                creator=request.user
            )
            messages.info(request, 'Product Issue Succesfully Created.....')
            return redirect("valueChainApp:product-issue-list")
    return render(request, 'create_issue.html', {'products':products})


def productList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
def productIssueList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        productIssue = ProductIssue.objects.all()
    return render(request, 'product_issue_list.html', {'productIssue': productIssue})