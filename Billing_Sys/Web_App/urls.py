from django.urls import path
from Web_App.views import (billing,bill_details,get_products)

urlpatterns = [
    path('billing/',billing,name='billing'),
    path('bill-details/',bill_details,name='bill-details'),
    path('get-products/',get_products,name='get-products'),
]
