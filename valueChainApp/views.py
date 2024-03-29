from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate

from .models import Product, ProductIssue, RawMaterials, PurchaseOrder, PurchaseReceipt, SalesOrder, DeliveryChallan, \
    StockEntry, ProductionCost, RawMaterialsProduct, PurchaseOrderProduct, PurchaseReceiptProduct, \
    SalesOrderProduct, DeliveryChallanProduct
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.db import models, transaction


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
            current_market_rate = request.POST.get('current_market_rate')
            is_finished_good = request.POST.get('is_finished_good') == 'on'
            if is_finished_good is None:
                is_finished_good = False

            existing_product = Product.objects.filter(product_name=product_name).first()
            if existing_product:
                messages.error(request, f'A product with the name "{product_name}" already exists.')
                return render(request, 'create_product.html')

            product = Product.objects.create(
                product_name=product_name,
                product_group=product_group,
                uom=uom,
                current_market_rate=current_market_rate,
                is_finished_good=is_finished_good
            )
            messages.info(request, 'Product Succesfully Created.....')
            return redirect("valueChainApp:product-list")
    return render(request, 'create_product.html')


def createProductIssue(request):
    products = Product.objects.filter(is_finished_good=True)
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
                creator=request.user,
                status='OPEN'
            )
            messages.info(request, 'Product Issue Succesfully Created.....')
            return redirect("valueChainApp:product-issue-list")
    return render(request, 'create_product_issue.html', {'products': products})


@transaction.atomic()
def createRawMaterial(request):
    products = Product.objects.filter(is_finished_good=False)
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
                product_issue=product_issue_ins,
                status='OPEN'
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


@transaction.atomic()
def createPurchaseOrder(request, raw_materials_no):
    raw_materials_ins = get_object_or_404(RawMaterials, id=raw_materials_no)
    if raw_materials_ins:
        raw_material_products = RawMaterialsProduct.objects.filter(raw_materials_id=raw_materials_ins.id)

    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            raw_materials = raw_materials_ins.id
            purchase_order_no = request.POST.get('purchase_order_no')
            if PurchaseOrder.objects.filter(purchase_order_no=purchase_order_no).exists():
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
                purchase_order_no=purchase_order_no,
                description=request.POST.get('description'),
                raw_materials=raw_materials_ins,
                product_issue=product_issue_ins,
                total_qty=total_qty,
                total=total,
                status='OPEN'
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


@transaction.atomic()
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


@transaction.atomic()
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
            remaining_qty = float(product_issue.total_qty) - float(
                product_issue.stockentry_set.aggregate(total_qty=models.Sum('qty'))['total_qty'] or 0)
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


@transaction.atomic()
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


@transaction.atomic()
def createSalesOrder(request):
    # products = Product.objects.all()
    products = Product.objects.filter(is_finished_good=True)

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
            insufficient_stock_products = []

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                product = Product.objects.get(pk=product)
                total_qty = total_qty + float(qty)
                total = total + (float(rate) * float(qty))

                if product.stock_qty < float(qty):
                    insufficient_stock_products.append(product.product_name)

            if insufficient_stock_products:
                messages.error(request,
                               f'Insufficient stock for products: {", ".join(insufficient_stock_products)}')
                return redirect('valueChainApp:create-sales-order')

            sales_order = SalesOrder.objects.create(
                creator=request.user,
                sales_order_no=sales_order_no,
                description=request.POST.get('description'),
                total_qty=total_qty,
                total=total,
                status='OPEN'
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


@transaction.atomic()
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
            insufficient_stock_products = []

            products = request.POST.getlist('product[]')
            uoms = request.POST.getlist('uom[]')
            qtys = request.POST.getlist('qty[]')
            rates = request.POST.getlist('rate[]')

            for product, rate, qty in zip(products, rates, qtys):
                product = Product.objects.get(pk=product)
                total_qty = total_qty + float(qty)
                total = total + (float(rate) * float(qty))

                if product.stock_qty < float(qty):
                    insufficient_stock_products.append(product.product_name)

            if insufficient_stock_products:
                messages.error(request,
                               f'Insufficient stock for products: {", ".join(insufficient_stock_products)}')
                return render(request, 'create_delivery_challan.html',
                              {'sales_order_products': sales_order_products})

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


def productionCostList(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        productionCostList = ProductionCost.objects.all()
    return render(request, 'production_cost_list.html', {'productionCostList': productionCostList})


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


def singleProduct(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        if product:
            product_issue_count = ProductIssue.objects.filter(product=product).count()
            raw_mat_count = RawMaterialsProduct.objects.filter(product=product).count()
            purchase_orders_count = PurchaseOrderProduct.objects.filter(product=product).count()
            purchase_receipt_count = PurchaseReceiptProduct.objects.filter(product=product).count()
            stock_entry_count = StockEntry.objects.filter(product=product).count()
            sales_order_count = SalesOrderProduct.objects.filter(product=product).count()
            delivery_challan_count = DeliveryChallanProduct.objects.filter(product=product).count()

    except Http404:
        return redirect('valueChainApp:product-list')

    context = {
        'product': product,
        'product_issue_count': product_issue_count,
        'raw_mat_count': raw_mat_count,
        'purchase_orders_count': purchase_orders_count,
        'purchase_receipt_count': purchase_receipt_count,
        'stock_entry_count': stock_entry_count,
        'sales_order_count': sales_order_count,
        'delivery_challan_count': delivery_challan_count,

    }

    return render(request, 'product_details.html', context)


def singleProductIssue(request, product_issue_id):
    product_issue = get_object_or_404(ProductIssue, pk=product_issue_id)
    data = {
        'raw_materials': 0
    }
    column_name = []
    column_value = []
    raw_materials_value = \
        PurchaseReceipt.objects.filter(product_issue_id=product_issue_id).aggregate(total_sum=Sum('total'))[
            'total_sum'] or 0
    data['raw_materials'] = float(raw_materials_value)
    production_costs = ProductionCost.objects.filter(product_issue_id=product_issue_id)
    for cost in production_costs:
        data[cost.cost_type] = float(cost.total)

    for cost_type, total in data.items():
        column_name.append(cost_type)
        column_value.append(total)

    context = {'product_issue': product_issue, 'data': data, 'column_name': column_name, 'column_value': column_value}
    return render(request, 'product_issue_details.html', context)


def singleRawMaterial(request, raw_materials_id):
    try:
        raw_materials = get_object_or_404(RawMaterials, pk=raw_materials_id)
        if raw_materials:
            raw_materials_products = RawMaterialsProduct.objects.filter(raw_materials=raw_materials)
    except Http404:
        return redirect('valueChainApp:raw-materials-list')

    return render(request, 'raw_materials_details.html',
                  {'raw_materials': raw_materials, 'raw_materials_products': raw_materials_products})


def singlePurchaseOrder(request, purchase_order_id):
    try:
        purchase_order = get_object_or_404(PurchaseOrder, pk=purchase_order_id)
        if purchase_order:
            purchase_order_products = PurchaseOrderProduct.objects.filter(purchase_order=purchase_order)
    except Http404:
        return redirect('valueChainApp:purchase-order-list')

    return render(request, 'purchase_order_details.html',
                  {'purchase_order': purchase_order, 'purchase_order_products': purchase_order_products})


def singlePurchaseReceipt(request, purchase_receipt_id):
    try:
        purchase_receipt = get_object_or_404(PurchaseReceipt, pk=purchase_receipt_id)
        if purchase_receipt:
            purchase_receipt_products = PurchaseReceiptProduct.objects.filter(purchase_receipt=purchase_receipt)
    except Http404:
        return redirect('valueChainApp:purchase-receipt-list')

    return render(request, 'purchase_receipt_details.html',
                  {'purchase_receipt': purchase_receipt, 'purchase_receipt_products': purchase_receipt_products})


def singleSalesOrder(request, sales_order_id):
    try:
        sales_order = get_object_or_404(SalesOrder, pk=sales_order_id)
        if sales_order:
            sales_order_products = SalesOrderProduct.objects.filter(sales_order=sales_order)
    except Http404:
        return redirect('valueChainApp:sales-order-list')

    return render(request, 'sales_order_details.html',
                  {'sales_order': sales_order, 'sales_order_products': sales_order_products})


def singleDeliveryChallan(request, delivery_challan_id):
    try:
        delivery_challan = get_object_or_404(DeliveryChallan, pk=delivery_challan_id)
        if delivery_challan:
            delivery_challan_products = DeliveryChallanProduct.objects.filter(delivery_challan=delivery_challan)
    except Http404:
        return redirect('valueChainApp:delivery-challan-list')

    return render(request, 'delivery_challan_details.html',
                  {'delivery_challan': delivery_challan, 'delivery_challan_products': delivery_challan_products})


def product_wise_report(request):
    finished_products = Product.objects.filter(is_finished_good=True)
    product_reports = []

    for product in finished_products:
        cogs = ProductIssue.objects.filter(product=product).aggregate(
            total_production_cost=Sum('production_cost')
        )['total_production_cost'] or 0.0

        # Calculate Revenue for the product
        revenue = DeliveryChallan.objects.filter(
            sales_order__status='COMPLETE', deliverychallanproduct__product=product
        ).aggregate(total_sales=Sum(F('deliverychallanproduct__qty') * F('deliverychallanproduct__rate')))[
                      'total_sales'] or 0.0

        gross_profit = float(revenue) - float(cogs)

        product_report = {
            'product': product,
            'cogs': cogs,
            'revenue': revenue,
            'gross_profit': gross_profit
        }
        product_reports.append(product_report)

    context = {
        'product_reports': product_reports
    }

    return render(request, 'gain_and_loss_report.html', context)
