from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate

from .models import Product, ProductIssue, RawMaterials, PurchaseOrder, PurchaseReceipt, SalesOrder, DeliveryChallan, \
    StockEntry, ProductionCost, RawMaterialsProduct, PurchaseOrderProduct, PurchaseReceiptProduct, \
    SalesOrderProduct, DeliveryChallanProduct
from django.contrib import messages
from django.db.models import Q
from django.db import models


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

            existing_product = Product.objects.filter(product_name=product_name).first()
            if existing_product:
                messages.error(request, f'A product with the name "{product_name}" already exists.')
                return render(request, 'create_product.html')

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

            product = get_object_or_404(Product, pk=product_id)

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
    products = Product.objects.exclude(product_group__icontains='Finished Goods')
    product_issues = ProductIssue.objects.exclude(status='COMPLETE')

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            raw_materials_no = request.POST.get('raw_materials_no')
            if RawMaterials.objects.filter(raw_materials_no=raw_materials_no).exists():
                messages.error(request, 'Raw materials number already exists. Please provide a unique number.')
                return render(request, 'create_raw_materials.html',
                              {'products': products, 'product_issues': product_issues})

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
    raw_materials_ins = get_object_or_404(RawMaterials, id=raw_materials_no)
    if raw_materials_ins:
        raw_material_products = RawMaterialsProduct.objects.filter(raw_materials_id=raw_materials_ins.id)

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            raw_materials = raw_materials_ins.id
            purchas_order_no = request.POST.get('purchase_order_no')
            if PurchaseOrder.objects.filter(purchas_order_no=purchas_order_no).exists():
                messages.error(request, 'Purchase Order number already exists. Please provide a unique number.')
                return render(request, 'create_purchase_order.html',
                              {'raw_material_products': raw_material_products})

            product_issue = raw_materials_ins.product_issue.id
            total_qty = 0
            total = 0

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                total_qty = total_qty + float(qty)
                total = total + (float(rate) * float(qty))

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
    return render(request, 'create_purchase_order.html', {'raw_material_products': raw_material_products})


def createPurchaseReceipt(request, purchase_order_no):
    purchase_order_ins = get_object_or_404(PurchaseOrder, id=purchase_order_no)
    if purchase_order_ins:
        purchase_order_products = PurchaseOrderProduct.objects.filter(purchase_order=purchase_order_ins.id)

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            purchase_order = purchase_order_ins.id
            purchase_receipt_no = request.POST.get('purchase_receipt_no')
            if PurchaseReceipt.objects.filter(purchase_receipt_no=purchase_receipt_no).exists():
                messages.error(request, 'Purchase Receipt number already exists. Please provide a unique number.')
                return render(request, 'create_purchase_receipt.html',
                              {'purchase_order_products': purchase_order_products})

            product_issue = purchase_order_ins.product_issue.id
            total_qty = 0
            total = 0

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                total_qty = total_qty + float(qty)
                total = total + (float(rate) * float(qty))

            product_issue_ins = get_object_or_404(ProductIssue, pk=product_issue)

            # Create RawMaterials instance
            purchase_receipt = PurchaseReceipt.objects.create(
                creator=request.user,
                purchase_receipt_no=purchase_receipt_no,
                description=request.POST.get('description'),
                purchase_order=purchase_order_ins,
                product_issue=product_issue_ins,
                total_qty=total_qty,
                total=total
            )

            # Create RawMaterialsProduct instances for each row
            for product, uom, qty, rate in zip(products, uoms, qtys, rates):
                PurchaseReceiptProduct.objects.create(
                    product=Product.objects.get(pk=product),
                    uom=uom,
                    qty=qty,
                    rate=rate,
                    raw_materials=purchase_order_ins.raw_materials,
                    product_issue=product_issue_ins.issue_no,
                    purchase_order=purchase_order_ins,
                    purchase_receipt=purchase_receipt
                )


            return redirect('valueChainApp:purchase-receipt-list')
    return render(request, 'create_purchase_receipt.html', {'purchase_order_products': purchase_order_products})


def createStockEntry(request, product_issue_no):
    product_issue_ins = get_object_or_404(ProductIssue, id=product_issue_no)
    if product_issue_ins:
        product_issue = ProductIssue.objects.get(id=product_issue_ins.id)
        if product_issue.status != 'COMPLETE':
            return redirect('valueChainApp:stock-entry-list')

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            stock_entry_no = request.POST.get('stock_entry_no')
            if StockEntry.objects.filter(stock_entry_no=stock_entry_no).exists():
                messages.error(request, 'Stock Entry number already exists. Please provide a unique number.')
                return render(request, 'create_stock_entry.html',
                              {'product_issue': product_issue})

            product_issue = product_issue_ins
            product = product_issue_ins.product
            uom = product_issue_ins.product.uom
            qty = request.POST.get('qty')
            rate = request.POST.get('rate')
            total = float(qty) * float(rate)

            # Validate if stock entry exceeds product issue quantity
            remaining_qty = product_issue.total_qty - \
                            product_issue.stockentry_set.aggregate(total_qty=models.Sum('qty'))['total_qty'] or 0
            if float(qty) > remaining_qty:
                messages.error(request, 'Stock Entry quantity cannot exceed remaining quantity of Product Issue')
                return render(request, 'create_stock_entry.html', {'product_issue': product_issue})

            stock_entry = StockEntry.objects.create(
                creator=request.user,
                stock_entry_no=stock_entry_no,
                product_issue=product_issue,
                product=product,
                uom=uom,
                qty=qty,
                rate=rate,
                total=total
            )

            return redirect('valueChainApp:stock-entry-list')

    return render(request, 'create_stock_entry.html', {'product_issue': product_issue})


def createProductionCost(request):
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        product_issues = ProductIssue.objects.all()
        if request.method == 'POST':
            product_issue = request.POST.get('product_issue')
            cost_type = request.POST.getlist('cost_type[]')
            total = request.POST.getlist('total[]')

            product_issue_ins = get_object_or_404(ProductIssue, pk=product_issue)

            for cost_type, total in zip(cost_type, total):
                ProductionCost.objects.create(
                    creator=request.user,
                    cost_type=cost_type,
                    product_issue=product_issue_ins,
                    total=total
                )
            return redirect('valueChainApp:production-cost-list')
    return render(request, 'create_production_cost.html', {'product_issues': product_issues})


def createSalesOrder(request):
    # products = Product.objects.all()
    products = Product.objects.filter(
        Q(product_group__iexact='Finished Goods') |  # Case-insensitive match
        Q(product_group__icontains='finished goods')  # Case-insensitive partial match
    )

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            sales_order_no = request.POST.get('sales_order_no')
            if SalesOrder.objects.filter(sales_order_no=sales_order_no).exists():
                messages.error(request, 'Sales Order number already exists. Please provide a unique number.')
                return render(request, 'create_sales_order.html',
                              {'products': products})
            total_qty = 0
            total = 0

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                total_qty = total_qty + float(qty)
                total = total + (float(rate) * float(qty))

            sales_order = SalesOrder.objects.create(
                creator=request.user,
                sales_order_no=sales_order_no,
                description=request.POST.get('description'),
                total_qty=total_qty,
                total=total
            )

            for product, uom, qty, rate in zip(products, uoms, qtys, rates):
                SalesOrderProduct.objects.create(
                    sales_order=sales_order,
                    product=Product.objects.get(pk=product),
                    uom=uom,
                    qty=qty,
                    rate=rate,
                )

            # ToDo: udpate status

            return redirect('valueChainApp:sales-order-list')
    return render(request, 'create_sales_order.html', {'products': products})


def createDeliveryChallan(request, sales_order_no):
    sales_order_ins = get_object_or_404(SalesOrder, id=sales_order_no)
    if sales_order_ins:
        sales_order_products = SalesOrderProduct.objects.filter(sales_order=sales_order_ins.id)

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')

    else:
        if request.method == 'POST':
            sales_order = sales_order_ins.id
            delivery_challan_no = request.POST.get('delivery_challan_no')
            if DeliveryChallan.objects.filter(delivery_challan_no=delivery_challan_no).exists():
                messages.error(request, 'Delivery Challan number already exists. Please provide a unique number.')
                return render(request, 'create_sales_order.html',
                              {'products': products})

            total_qty = 0
            total = 0

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                total_qty = total_qty + float(qty)
                total = total + (float(rate) * float(qty))

            delivery_challan = DeliveryChallan.objects.create(
                delivery_challan_no=delivery_challan_no,
                creator=request.user,
                sales_order=sales_order_ins,
                description=request.POST.get('description'),
                total_qty=total_qty,
                total=total
            )

            for product, uom, qty, rate in zip(products, uoms, qtys, rates):
                DeliveryChallanProduct.objects.create(
                    delivery_challan=delivery_challan,
                    sales_order=sales_order,
                    product=Product.objects.get(pk=product),
                    uom=uom,
                    qty=qty,
                    rate=rate,
                )

            # ToDo: udpate status update stock..........

            return redirect('valueChainApp:delivery-challan-list')
    return render(request, 'create_delivery_challan.html', {'sales_order_products': sales_order_products})


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
        purchaseReceiptList = PurchaseReceipt.objects.all()
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
