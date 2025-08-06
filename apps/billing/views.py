import csv
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invoice, InvoiceItem, Payment
from .serializers import InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer
from .permissions import BillingPermission


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset           = Invoice.objects.select_related('patient').all()
    serializer_class   = InvoiceSerializer
    permission_classes = [BillingPermission]


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset           = InvoiceItem.objects.select_related('invoice').all()
    serializer_class   = InvoiceItemSerializer
    permission_classes = [BillingPermission]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset           = Payment.objects.select_related('invoice').all()
    serializer_class   = PaymentSerializer
    permission_classes = [BillingPermission]


class DailyCashReportView(APIView):
    permission_classes = [BillingPermission]

    def get(self, request):
        today = timezone.now().date()
        payments = Payment.objects.filter(paid_at__date=today)
        summary = {
            'total_received': sum(p.amount for p in payments),
            'by_method': {
                method: sum(p.amount for p in payments if p.method == method)
                for method, _ in Payment.Method.choices
            }
        }
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="daily_cash_{today}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Method', 'Amount'])
            for method, _ in Payment.Method.choices:
                writer.writerow([method, summary['by_method'][method]])
            writer.writerow(['TOTAL', summary['total_received']])
            return response
        return Response(summary, status=status.HTTP_200_OK)