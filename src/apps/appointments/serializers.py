from rest_framework import serializers

from .models import Appointment


class AppointmentCreateSerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    start_time = serializers.DateTimeField()


class AppointmentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[Appointment.Status.CONFIRMED, Appointment.Status.CANCELLED])


class AppointmentFilterSerializer(serializers.Serializer):
    from_time = serializers.DateTimeField(required=False)
    to_time = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(choices=Appointment.Status.values, required=False)

    def validate(self, attrs):
        from_time = attrs.get("from_time")
        to_time = attrs.get("to_time")
        if from_time and to_time and from_time >= to_time:
            raise serializers.ValidationError({"to": ["Must be later than from."]})
        return attrs


class AppointmentSerializer(serializers.ModelSerializer):
    service_id = serializers.UUIDField(source="service.id", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    business_id = serializers.UUIDField(source="service.business.id", read_only=True)
    business_name = serializers.CharField(source="service.business.name", read_only=True)
    client_id = serializers.UUIDField(source="client.id", read_only=True)
    client_full_name = serializers.CharField(source="client.full_name", read_only=True)
    client_email = serializers.EmailField(source="client.email", read_only=True)

    class Meta:
        model = Appointment
        fields = (
            "id", "service_id", "service_name", "business_id", "business_name", "client_id",
            "client_full_name", "client_email", "start_time", "status", "created_at", "updated_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.context.get("include_client"):
            representation.pop("client_id")
            representation.pop("client_full_name")
            representation.pop("client_email")
        return representation
