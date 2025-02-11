from rest_framework import serializers
from .models import Product, Purchase, PurchaseItem, Denomination

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    tax = serializers.StringRelatedField(source="product.tax_percentage")
    name = serializers.StringRelatedField(source="product.name")
    product_id = serializers.StringRelatedField(source="product.product_id")
    price = serializers.StringRelatedField(source="product.price")
    denominations = serializers.SerializerMethodField()
    taxable_amount = serializers.StringRelatedField(source="purchase.taxable_amount")
    pur_tax_amount = serializers.StringRelatedField(source="purchase.tax_amount")
    balance_amount = serializers.StringRelatedField(source="purchase.balance_amount")
    total_amount = serializers.StringRelatedField(source="purchase.total_amount")
    class Meta:
        model = PurchaseItem
        fields = ['id','purchase','product','product_id','name', 'price','quantity', 'unit_price','tax',
                  'tax_amount','total_amount','taxable_amount','pur_tax_amount','balance_amount','total_amount','denominations']

    def get_denominations(self, obj):
        balance_amt = obj.purchase.balance_amount
        denomi_queryset = Denomination.objects.filter(count__gt=0).order_by('-value')
        
        denomi = list(denomi_queryset.values('id', 'value', 'count'))
        
        selected_denominations = []
        
        for denom in denomi:
            if balance_amt <= 0:
                break  # Stop if the amount is fully matched

            max_possible = min(balance_amt // denom['value'], denom['count'])  # Take the possible count
            if max_possible > 0:
                selected_denominations.append({'id': denom['id'], 'value': denom['value'], 'count': max_possible})
                balance_amt -= max_possible * denom['value']  # Reduce balance
        
        return selected_denominations

class PurchaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y at %I:%M %p")

    class Meta:
        model = Purchase
        fields = ['id','customer_email', 'created_at', 'total_amount','paid_amount','tax_amount']

    
