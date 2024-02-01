from django.urls import path

from .views import *

app_name = 'valueChainApp'
urlpatterns = [
    path("", home, name="index"),
    path("home/", home, name="home"),
    path("create-product/", createProduct, name="create-product"),
    path("product-list/", productList, name="product-list"),
    path("product-issue-list/", productIssueList, name="product-issue-list"),
    path("raw-materials-list/", rawMaterialList, name="raw-materials-list"),
    path("purchase-order-list/", purchaseOrderList, name="purchase-order-list"),
    path("purchase-receipt-list/", purchaseReceiptList, name="purchase-receipt-list"),
    # path("cost-type-list/", costTypeList, name="cost-type-list"),
    path("production-cost-list/", productionCostList, name="production-cost-list"),
    # path("others-cost-list/", othersCostList, name="others-cost-list"),
    path("stock-entry-list/", stockEntryList, name="stock-entry-list"),
    path("sales-order-list/", salesOrderList, name="sales-order-list"),
    path("delivery-challan-list/", deliveryChallanList, name="delivery-challan-list"),
    path("create-product-issue/", createProductIssue, name="create-product-issue"),
    path("create-raw-materials/", createRawMaterial, name="create-raw-issue"),
    path("<int:raw_materials_no>/create-purchase-order/", createPurchaseOrder, name="create-purchase-order"),
    path("<int:purchase_order_no>/create-purchase-receipt/", createPurchaseReceipt, name="create-purchase-receipt"),
    path("create-stock-entry/", createStockEntry, name="create-stock-entry"),

    path("get-raw-material-products/", getRawMaterialProducts, name="get-raw-material-products"),
]
