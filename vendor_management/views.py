from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.utils import timezone

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, url_path='performance')
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_metrics)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.none()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor', None)
        if vendor_id is not None:
            queryset = queryset.filter(vendor__id=vendor_id)
        return queryset

    @action(detail=True, methods=['post'], url_path='acknowledge')
    def acknowledge(self, request, pk=None):
        po = self.get_object()
        po.acknowledgment_date = timezone.now()
        po.save()
        return Response({'status': 'Purchase order acknowledged'})