# apps/labs/serializers.py

from rest_framework import serializers
from .models import LabTest, LabOrder


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = [
            "id",
            "code",
            "name",
            "description",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)


class LabOrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.full_name", read_only=True
    )
    test_name = serializers.CharField(
        source="test.name", read_only=True
    )

    class Meta:
        model = LabOrder
        fields = [
            "id",
            "patient",
            "patient_name",
            "doctor",
            "test",
            "test_name",
            "ordered_at",
            "status",
            "result",
            "result_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "ordered_at",
            "patient_name",
            "test_name",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)