from rest_framework import serializers
from .models import (
    Ward, Room, Bed, Admission, VitalSign,
    NursingNote, Round, ServiceUsage, DischargeSummary
)


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'
        read_only_fields = ('is_available',)


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = '__all__'
        read_only_fields = ('id','admitted_by','admitted_at','status','discharged_at')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['admitted_by'] = user
        return super().create(validated_data)


class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = '__all__'
        read_only_fields = ('id','recorded_at','recorded_by')

    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)


class NursingNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NursingNote
        fields = '__all__'
        read_only_fields = ('id','created_at','created_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'
        read_only_fields = ('id','at_time')

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user
        return super().create(validated_data)


class ServiceUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUsage
        fields = '__all__'
        read_only_fields = ('id','created_at')

    def create(self, validated_data):
        return super().create(validated_data)


class DischargeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DischargeSummary
        fields = '__all__'
        read_only_fields = ('id','created_at','created_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)