from rest_framework import serializers
from .models import Ward, Bed, Admission, Discharge, VitalSign

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'

class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'

class VitalSignSerializer(serializers.ModelSerializer):
    recorded_by = serializers.ReadOnlyField(source='recorded_by.username')
    class Meta:
        model = VitalSign
        fields = '__all__'
        read_only_fields = ('recorded_by','recorded_at')

class AdmissionSerializer(serializers.ModelSerializer):
    admitted_by = serializers.ReadOnlyField(source='admitted_by.username')
    class Meta:
        model = Admission
        fields = '__all__'
        read_only_fields = ('admitted_by','admitted_at','status')

    def create(self, validated_data):
        bed = validated_data['bed']
        if bed.is_occupied:
            raise serializers.ValidationError("Bed is already occupied.")
        bed.is_occupied = True
        bed.save()
        admission = Admission.objects.create(**validated_data)
        return admission

class DischargeSerializer(serializers.ModelSerializer):
    discharged_by = serializers.ReadOnlyField(source='discharged_by.username')
    class Meta:
        model = Discharge
        fields = '__all__'
        read_only_fields = ('discharged_by','discharged_at')

    def create(self, validated_data):
        admission = validated_data['admission']
        if admission.status == 'discharged':
            raise serializers.ValidationError("Already discharged.")
        admission.status = 'discharged'
        admission.save()
        bed = admission.bed
        bed.is_occupied = False
        bed.save()
        discharge = Discharge.objects.create(**validated_data)
        return discharge