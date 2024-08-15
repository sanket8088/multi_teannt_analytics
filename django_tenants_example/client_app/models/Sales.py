from django.db import models
from django_tenants.models import TenantMixin
from django.utils import timezone

class SalesData(models.Model):
    sale_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sales_data')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='sales_data')
    
    class Meta:
        ordering = ['sale_date']
    
    def __str__(self):
        return f"Sale on {self.sale_date} for {self.amount}"
