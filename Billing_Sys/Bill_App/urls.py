from django.urls import path
from .views import ProductListView, CreatePurchaseView, PastPurchasesView,GetPurchaseItemDetView

urlpatterns = [
    path('get-products-list/', ProductListView.as_view(), name='get-products-list'),
    path('create-purchase/', CreatePurchaseView.as_view(), name='create-purchase'),
    path('purchases/<str:email>/', PastPurchasesView.as_view(), name='past-purchases'),
    path('get-bill-item/', GetPurchaseItemDetView.as_view(), name='get-bill-item'),
]
