from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Invoice, InvoiceItem, Payment

class InvoiceItemSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('id',)

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    processed_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id','paid_at')

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    payments = PaymentSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    outstanding_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('id','sequence','invoice_number','status','created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice