from rest_framework import serializers
from .models import Medicine, Batch, PharmacySale, SaleItem
from apps.consultations.serializers import PrescriptionSerializer

class MedicineSerializer(serializers.ModelSerializer):
    total_stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = Medicine
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ('id','medicine','batch','quantity','unit_price','total_price')


class PharmacySaleSerializer(serializers.ModelSerializer):
    items         = SaleItemSerializer(many=True)
    total_amount  = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    sold_by       = serializers.HiddenField(default=serializers.CurrentUserDefault())
    prescription  = serializers.PrimaryKeyRelatedField(
        queryset=PrescriptionSerializer.Meta.model.objects.all(),
        required=False, allow_null=True
    )

    class Meta:
        model = PharmacySale
        fields = '__all__'
        read_only_fields = ('id','sale_date','total_amount')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = PharmacySale.objects.create(**validated_data)
        for item in items_data:
            SaleItem.objects.create(sale=sale, **item)
        return sale