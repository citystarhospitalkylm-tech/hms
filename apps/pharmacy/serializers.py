from rest_framework import serializers
from .models import (
    Supplier,
    DrugCategory,
    Drug,
    Batch,
    SaleItem,
)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

class DrugCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugCategory
        fields = "__all__"

class DrugSerializer(serializers.ModelSerializer):
    category = DrugCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DrugCategory.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Drug
        fields = [
            "id", "name", "description",
            "unit_price", "category", "category_id", "created_at"
        ]

class SaleItemSerializer(serializers.ModelSerializer):
    batch_no = serializers.CharField(source="batch.batch_no", read_only=True)
    drug_name = serializers.CharField(source="batch.drug.name", read_only=True)

    class Meta:
        model = SaleItem
        fields = [
            "id", "batch", "batch_no", "drug_name",
            "quantity_sold", "unit_price", "sold_at"
        ]

class StockSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source="drug.name", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    total_sold = serializers.IntegerField(read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="drug.unit_price", read_only=True
    )

    class Meta:
        model = Batch
        fields = [
            "id", "batch_no", "drug", "drug_name",
            "supplier", "supplier_name", "quantity",
            "total_sold", "available_quantity",
            "unit_price", "expiry_date", "created_at"
        ]