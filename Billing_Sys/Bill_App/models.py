from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.name} ({self.product_id})"
    
class Purchase(models.Model):
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase by {self.customer_email} on {self.created_at}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items_pur")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return (self.product.price * self.quantity) * (1 + self.product.tax_percentage / 100)

class Denomination(models.Model):
    value = models.IntegerField(unique=True)
    count = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"₹{self.value} ({self.count})"
