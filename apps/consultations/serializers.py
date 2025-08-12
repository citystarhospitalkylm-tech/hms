from rest_framework import serializers
from .models import Consultation, Prescription, PrescriptionItem, Referral

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = "__all__"
        read_only_fields = ("id",)

class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = (
            "id",
            "consultation",
            "patient",
            "prescribed_by",
            "created_at",
            "items",
        )
        read_only_fields = ("id", "created_at", "prescribed_by")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        validated_data["prescribed_by"] = self.context["request"].user
        prescription = Prescription.objects.create(**validated_data)
        for item_data in items_data:
            PrescriptionItem.objects.create(
                prescription=prescription,
                **item_data
            )
        return prescription

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = "__all__"
        read_only_fields = ("id", "created_at", "referred_by")

    def create(self, validated_data):
        validated_data["referred_by"] = self.context["request"].user
        return super().create(validated_data)

class ConsultationSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    referrals = ReferralSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "doctor",
        )

    def create(self, validated_data):
        validated_data["doctor"] = self.context["request"].user
        return super().create(validated_data)