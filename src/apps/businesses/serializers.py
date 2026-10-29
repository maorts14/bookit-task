from rest_framework import serializers

from .models import Business, Service


class ServiceSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(source="business.id", read_only=True)

    class Meta:
        model = Service
        fields = ("id", "business_id", "name", "duration_minutes", "price", "created_at", "updated_at")

    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ensure this value is greater than 0.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ensure this value is greater than or equal to 0.")
        return value


class BusinessSerializer(serializers.ModelSerializer):
    owner_id = serializers.UUIDField(source="owner.id", read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Business
        fields = ("id", "name", "category", "owner_id", "created_at", "updated_at", "services")


class BusinessWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ("name", "category")


class ServiceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("name", "duration_minutes", "price")

    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ensure this value is greater than 0.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ensure this value is greater than or equal to 0.")
        return value


class BusinessSummarySerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    service_name = serializers.CharField()
    upcoming_appointments_count = serializers.IntegerField()
    expected_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
