# apps/patients/serializers.py

import datetime
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "mrn",
            "first_name",
            "last_name",
            "full_name",
            "dob",
            "age",
            "gender",
            "blood_group",
            "allergies",
            "phone_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "mrn",
            "full_name",
            "age",
            "created_at",
            "updated_at",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_age(self, obj):
        today = datetime.date.today()
        return (
            today.year
            - obj.dob.year
            - ((today.month, today.day) < (obj.dob.month, obj.dob.day))
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)