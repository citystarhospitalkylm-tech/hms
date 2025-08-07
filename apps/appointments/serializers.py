# apps/appointments/serializers.py

from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.full_name", read_only=True
    )
    doctor_name = serializers.CharField(
        source="doctor.get_full_name", read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "appointment_time",
            "token_number",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "token_number",
            "patient_name",
            "doctor_name",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)