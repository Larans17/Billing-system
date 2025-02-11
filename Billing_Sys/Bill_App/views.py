from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Product, Purchase, PurchaseItem, Denomination
from .serializers import ProductSerializer, PurchaseSerializer,PurchaseItemSerializer
import json
from .tasks import *
from django.db.models import F

# from Bill_App.tasks import send_email_to_customer

class ProductListView(APIView):
    """
    API to get the list of products.
    """
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreatePurchaseView(APIView):
    """
    API to create a new purchase with proper stock validation.
    """
    def post(self, request):
            try:
                with transaction.atomic():
                    customer_email = request.data.get('customer_email')
                    items = request.data.get('items', [])
                    denominations = request.data.get('denominations', [])
                    paid_amount = float(request.data.get('paid_amount', 0))
                    total_amount = float(request.data.get('total_amount', 0))
                    taxable_amount = float(request.data.get('taxable_amount', 0))
                    tax_amount = float(request.data.get('tax_amount', 0))

                    if not customer_email:
                        raise ValidationError("Customer email is required.")

                    if not items:
                        raise ValidationError("No items selected.")

                    purchase = Purchase.objects.create(customer_email=customer_email,total_amount=total_amount,
                    balance_amount=(paid_amount-total_amount),paid_amount=paid_amount,taxable_amount=taxable_amount,tax_amount=tax_amount)
                    items = json.loads(items)
                    total_cost = 0
                    for item in items:
                        product = get_object_or_404(Product, product_id=item['product_id'])
                        quantity = int(item['quantity'])
                        tax_amt = int(item['tax_amt'])
                        taxable_amt = int(item['taxable_amt'])

                        if product.available_stocks < quantity:
                            raise ValidationError(f'Insufficient stock for {product.name}')

                        product.available_stocks -= quantity
                        product.save()

                        PurchaseItem.objects.create(purchase=purchase, product=product, quantity=quantity,tax_amount=tax_amt
                                                    ,unit_price=taxable_amt,total_amount=(taxable_amt+tax_amt))
                    
                    
                    denominations = json.loads(denominations)
                    for denom_dict in denominations: 
                        for value, count in denom_dict.items():
                            value = int(value)
                            count = int(count)

                            # Check if the denomination already exists
                            denomination_obj, created = Denomination.objects.get_or_create(value=value, defaults={"count": count})

                            if not created:
                                denomination_obj.count = F("count") + count
                                denomination_obj.save()


                        balance = total_amount - paid_amount
                        
                    kwargs = {
                        'to_email': customer_email,
                        'total_amount': total_amount,
                        'paid_amount': paid_amount,
                        }
                    subject = "Invoice Amount"
                    content = f"""
                               <p>Thank you for your purchase.</p>
                               <p><strong>Total: </strong> ₹{total_cost}</p>
                               <p><strong>Balance: </strong> ₹{balance}</p>
                               """
                    # send_email_to_customer.delay(customer_email,subject,content)
                    EmailThread(**kwargs).start()
                    return Response({'total_cost': total_cost, 'balance': balance}, status=status.HTTP_201_CREATED)
            except ValidationError as ve:
                return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PastPurchasesView(APIView):
    """
    API to fetch past purchases of a customer.
    """
    def get(self, request, email):
        try:
            if email !="None":
                purchases = Purchase.objects.filter(customer_email=email)
            else:
                purchases = Purchase.objects.all()
            serializer = PurchaseSerializer(purchases, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetPurchaseItemDetView(APIView):
    """
    API to fetch  purchases item .
    """
    def get(self, request):
        try:
            pur_id = request.query_params.get('id')
            purchases = PurchaseItem.objects.select_related('product').filter(purchase=pur_id)
            serializer = PurchaseItemSerializer(purchases, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
