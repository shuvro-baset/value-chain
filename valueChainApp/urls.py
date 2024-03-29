from django.urls import path

from .views import *

app_name = 'valueChainApp'
urlpatterns = [
    path("", home, name="index"),
    path("home/", home, name="home"),
    path("create-product/", createProduct, name="create-product"),
    path("create-product-issue/", createProductIssue, name="create-product-issue"),
    path("create-raw-materials/", createRawMaterial, name="create-raw-materials"),
    path("<int:raw_materials_no>/create-purchase-order/", createPurchaseOrder, name="create-purchase-order"),
    path("<int:purchase_order_no>/create-purchase-receipt/", createPurchaseReceipt, name="create-purchase-receipt"),
    path("<int:product_issue_no>/create-stock-entry/", createStockEntry, name="create-stock-entry"),
    path("add-production-cost/", createProductionCost, name="add-production-cost"),
    path("create-sales-order/", createSalesOrder, name="create-sales-order"),
    path("<int:sales_order_no>/create-delivery-challan/", createDeliveryChallan, name="create-delivery-challan"),
    path("product-list/", productList, name="product-list"),
    path("product-issue-list/", productIssueList, name="product-issue-list"),
    path("raw-materials-list/", rawMaterialList, name="raw-materials-list"),
    path("purchase-order-list/", purchaseOrderList, name="purchase-order-list"),
    path("purchase-receipt-list/", purchaseReceiptList, name="purchase-receipt-list"),
    path("production-cost-list/", productionCostList, name="production-cost-list"),
    path("stock-entry-list/", stockEntryList, name="stock-entry-list"),
    path("sales-order-list/", salesOrderList, name="sales-order-list"),
    path("delivery-challan-list/", deliveryChallanList, name="delivery-challan-list"),
    path("product-details/<int:product_id>", singleProduct, name="product-details"),
    path("product-issue-details/<int:product_issue_id>", singleProductIssue, name="product-issue-details"),
    path("raw-materials/<int:raw_materials_id>", singleRawMaterial, name="raw-materials-details"),
    path("purchase-order/<int:purchase_order_id>", singlePurchaseOrder, name="purchase-order-details"),
    path("purchase-receipt/<int:purchase_receipt_id>", singlePurchaseReceipt, name="purchase-receipt-details"),
    path("sales-order/<int:sales_order_id>", singleSalesOrder, name="sales-order-details"),
    path("delivery-challan/<int:delivery_challan_id>", singleDeliveryChallan, name="delivery-challan-details"),
    path("gain-and-loss-report", product_wise_report, name="gain-and-loss-report"),

]
