from django.db import models
from django.db.models import F, Avg

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        if self.status == 'completed':
            self.update_vendor_on_time_delivery_rate()
            if self.quality_rating is not None:
                self.update_vendor_quality_rating_avg()

        if self.acknowledgment_date is not None:
            self.update_vendor_average_response_time()
        
        self.update_vendor_fulfillment_rate()

    def update_vendor_on_time_delivery_rate(self):
        vendor = self.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=F('issue_date')).count()
        vendor.on_time_delivery_rate = on_time_orders / completed_orders.count() * 100
        vendor.save()

    def update_vendor_quality_rating_avg(self):
        vendor = self.vendor
        completed_orders_with_quality_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating__isnull=True)
        quality_rating_sum = completed_orders_with_quality_rating.aggregate(models.Sum('quality_rating'))['quality_rating__sum']
        vendor.quality_rating_avg = quality_rating_sum / completed_orders_with_quality_rating.count()
        vendor.save()

    def update_vendor_average_response_time(self):
        vendor = self.vendor
        acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor).exclude(acknowledgment_date__isnull=True)
        response_times = acknowledged_orders.annotate(response_time=F('acknowledgment_date') - F('issue_date'))
        average_response_time = response_times.aggregate(Avg('response_time'))['response_time__avg']
        vendor.average_response_time = average_response_time.total_seconds() / 3600  # convert to hours
        vendor.save()
    
    def update_vendor_fulfillment_rate(self):
        vendor = self.vendor
        total_orders = PurchaseOrder.objects.filter(vendor=vendor)
        fulfilled_orders = total_orders.filter(status='completed', quality_rating__gte=0)
        vendor.fulfillment_rate = (fulfilled_orders.count() / total_orders.count()) * 100
        vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"