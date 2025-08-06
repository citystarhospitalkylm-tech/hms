from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = (
            'id', 'patient_id', 'qr_code', 'created_at', 'updated_at'
        )