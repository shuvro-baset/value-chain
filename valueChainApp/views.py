from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate

from .models import Product, ProductIssue, RawMaterials, PurchaseOrder, PurchaseRecipt, SalesOrder, DeliveryChallan, \
    StockEntry, ProductionCost, RawMaterialsProduct, PurchaseOrderProduct, PurchaseReceiptProduct, \
    SalesOrderProduct, DeliveryChallanProduct
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
            product_id = request.POST.get('product')
            issue_no = request.POST.get('issue_no')

            # Retrieve the Product instance corresponding to the selected product ID
            product = get_object_or_404(Product, pk=product_id)

            # ToDo: product_name unique validation check and sending message.
            product_issue = ProductIssue.objects.create(
                description=description,
                total_qty=total_qty,
                product=product,
                issue_no=issue_no,
                creator=request.user
            )
            messages.info(request, 'Product Issue Succesfully Created.....')
            return redirect("valueChainApp:product-issue-list")
    return render(request, 'create_product_issue.html', {'products': products})


def createRawMaterial(request):
    products = Product.objects.all()
    product_issues = ProductIssue.objects.all()

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            raw_materials_no = request.POST.get('raw_materials_no')
            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            product_issue = request.POST.get('product_issue')

            product_issue_ins = get_object_or_404(ProductIssue, pk=product_issue)

            # Create RawMaterials instance
            raw_materials = RawMaterials.objects.create(
                creator=request.user,
                description=request.POST.get('description'),
                raw_materials_no=raw_materials_no,
                product_issue=product_issue_ins
            )

            # Create RawMaterialsProduct instances for each row
            for product, uom, qty in zip(products, uoms, qtys):
                RawMaterialsProduct.objects.create(
                    product=Product.objects.get(pk=product),
                    uom=uom,
                    qty=qty,
                    raw_materials=raw_materials,
                    product_issue=product_issue_ins.issue_no
                )

            return redirect('valueChainApp:raw-materials-list')
    return render(request, 'create_raw_materials.html', {'products': products, 'product_issues': product_issues})


def createPurchaseOrder(request, raw_materials_no):
    products = Product.objects.all()
    raw_materials_ins = get_object_or_404(RawMaterials, id=raw_materials_no)
    if raw_materials_ins:
        raw_material_products = RawMaterialsProduct.objects.filter(raw_materials_id=raw_materials_ins.id)


    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            raw_materials = raw_materials_ins.id
            purchas_order_no = request.POST.get('purchase_order_no')
            product_issue = raw_materials_ins.product_issue.id
            total_qty = 0
            total = 0

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                total_qty = total_qty + float(qty)
                total = total + float(rate)


            product_issue_ins = get_object_or_404(ProductIssue, pk=product_issue)

            # Create RawMaterials instance
            purchase_order = PurchaseOrder.objects.create(
                creator=request.user,
                purchas_order_no=purchas_order_no,
                description=request.POST.get('description'),
                raw_materials=raw_materials_ins,
                product_issue=product_issue_ins,
                total_qty=total_qty,
                total=total
            )

            # Create RawMaterialsProduct instances for each row
            for product, uom, qty, rate in zip(products, uoms, qtys, rates):
                PurchaseOrderProduct.objects.create(
                    product=Product.objects.get(pk=product),
                    uom=uom,
                    qty=qty,
                    rate=rate,
                    raw_materials=raw_materials_ins.raw_materials_no,
                    product_issue=product_issue_ins.issue_no,
                    purchase_order=purchase_order
                )

            return redirect('valueChainApp:purchase-order-list')
    return render(request, 'create_purchase_order.html', {'products': products, 'raw_material_products': raw_material_products})


def createPurchaseReceipt(request):
    products = Product.objects.all()
    product_issues = ProductIssue.objects.all()

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            pass
            return redirect('valueChainApp:purchase-receipt-list')
    return render(request, 'create_purchase_receipt.html', {'products': products, 'product_issues': product_issues})


def createStockEntry(request):
    products = Product.objects.all()
    product_issues = ProductIssue.objects.all()

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            pass
            return redirect('valueChainApp:stock-entry-list')
    return render(request, 'create_stock_entry.html', {'products': products, 'product_issues': product_issues})


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


def rawMaterialList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        rawMaterialList = RawMaterials.objects.all()
    return render(request, 'raw_material_list.html', {'rawMaterialList': rawMaterialList})


def purchaseOrderList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        purchaseOrderList = PurchaseOrder.objects.all()
    return render(request, 'purchase_order_list.html', {'purchaseOrderList': purchaseOrderList})


def purchaseReceiptList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        purchaseReceiptList = PurchaseRecipt.objects.all()
    return render(request, 'purchase_receipt_list.html', {'purchaseReceiptList': purchaseReceiptList})


# def costTypeList(request):
#     context = {}
#     if not request.user.is_authenticated:
#         return redirect('valueChainApp:home')
#     else:
#         costTypeList = CostType.objects.all()
#     return render(request, 'cost_type_list.html', {'costTypeList': costTypeList})


def productionCostList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        productionCostList = ProductionCost.objects.all()
    return render(request, 'production_cost_list.html', {'productionCostList': productionCostList})


# def othersCostList(request):
#     context = {}
#     if not request.user.is_authenticated:
#         return redirect('valueChainApp:home')
#     else:
#         othersCostList = OthersCost.objects.all()
#     return render(request, 'others_cost_list.html', {'othersCostList': othersCostList})


def stockEntryList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        stockEntryList = StockEntry.objects.all()
    return render(request, 'stock_entry_list.html', {'stockEntryList': stockEntryList})


def salesOrderList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        salesOrderList = SalesOrder.objects.all()
    return render(request, 'sales_order_list.html', {'salesOrderList': salesOrderList})


def deliveryChallanList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        deliveryChallanList = DeliveryChallan.objects.all()
    return render(request, 'delivery_challan_list.html', {'deliveryChallanList': deliveryChallanList})


def getRawMaterialProducts(request):
    print("view function...........")
    raw_materials_id = request.GET.get('raw_materials_id')
    data = list(
        RawMaterialsProduct.objects.filter(raw_materials_id=raw_materials_id).values('product', 'uom', 'qty'))
    return JsonResponse(data, safe=False)
