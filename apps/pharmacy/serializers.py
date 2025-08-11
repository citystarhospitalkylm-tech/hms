from rest_framework import serializers
from .models import Supplier, DrugCategory, Drug, Batch, SaleItem


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class DrugCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugCategory
        fields = '__all__'

class DrugSerializer(serializers.ModelSerializer):
    category = DrugCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DrugCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Drug
        fields = ['id', 'name', 'description', 'unit_price', 'category', 'category_id', 'created_at']

#class StockSerializer(serializers.ModelSerializer):
 #   drug = DrugSerializer(read_only=True)
  #  drug_id = serializers.PrimaryKeyRelatedField(
   #     queryset=Drug.objects.all(), source='drug', write_only=True
    

  #  class Meta:
   #     model = Stock
    #    fields = [
     #       'id', 'drug', 'drug_id', 'batch_no', 'quantity',
      #      'expiry_date', 'supplier', 'received_at'
        

#class PrescriptionItemSerializer(serializers.ModelSerializer):
 #   drug = DrugSerializer(read_only=True)
  #  drug_id = serializers.PrimaryKeyRelatedField(
   #     queryset=Drug.objects.all(), source='drug', write_only=True
    #)

    #lass Meta:
    #    model = PrescriptionItem
     #   fields = ['id', 'drug', 'drug_id', 'dosage', 'quantity']

#class PrescriptionSerializer(serializers.ModelSerializer):
 #   items = PrescriptionItemSerializer(many=True)

  #  class Meta:
   #     model = Prescription
    #    fields = ['id', 'patient', 'prescribed_by', 'created_at', 'notes', 'items']

    #def create(self, validated_data):
     #   items_data = validated_data.pop('items')
      #  prescription = Prescription.objects.create(**validated_data)
       # for item in items_data:
        #    PrescriptionItem.objects.create(prescription=prescription, **item)
        #eturn prescription

#class DispenseSerializer(serializers.ModelSerializer):
 #   prescription_item = PrescriptionItemSerializer(read_only=True)
  #  prescription_item_id = serializers.PrimaryKeyRelatedField(
   #     queryset=PrescriptionItem.objects.filter(dispense=None),
    #    source='prescription_item', write_only=True
    #)

 #   class Meta:
#        model = Dispense
  #      fields = ['id', 'prescription_item', 'prescription_item_id', 'dispensed_by', 'dispensed_at']