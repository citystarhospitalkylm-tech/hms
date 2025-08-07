# apps/doctors/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class DoctorSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.filter(role__name="Doctor")
    )

    class Meta:
        model = Doctor
        fields = [
            "id",
            "user",
            "user_id",
            "specialty",
            "qualifications",
            "phone",
            "department",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        validated_data["created_by"] = request_user
        # Pop user_id into user
        validated_data["user"] = validated_data.pop("user_id")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        # Disallow changing the linked user
        validated_data.pop("user_id", None)
        return super().update(instance, validated_data)