from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.users.models import User
from apps.businesses.models import Service

from .models import Appointment
from .serializers import AppointmentCreateSerializer, AppointmentSerializer, AppointmentStatusSerializer
from .services import AppointmentService


class AppointmentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


def appointment_queryset():
    return Appointment.objects.select_related("service__business", "client")


class AppointmentListCreateView(APIView):
    pagination_class = AppointmentPagination

    @extend_schema(
        operation_id="list_appointments",
        parameters=[
            OpenApiParameter("from", str, OpenApiParameter.QUERY),
            OpenApiParameter("to", str, OpenApiParameter.QUERY),
            OpenApiParameter("status", str, OpenApiParameter.QUERY),
            OpenApiParameter("page", int, OpenApiParameter.QUERY),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY),
        ],
        responses={200: AppointmentSerializer(many=True)},
    )
    def get(self, request):
        if request.user.role == User.Role.CLIENT:
            appointments = appointment_queryset().filter(client=request.user)
            include_client = False
        else:
            appointments = appointment_queryset().filter(service__business__owner=request.user)
            include_client = True
        from_time = request.query_params.get("from")
        to_time = request.query_params.get("to")
        status_value = request.query_params.get("status")
        if from_time:
            appointments = appointments.filter(start_time__gte=from_time)
        if to_time:
            appointments = appointments.filter(start_time__lt=to_time)
        if status_value:
            if status_value not in Appointment.Status.values:
                raise ValidationError({"status": ["Invalid status."]})
            appointments = appointments.filter(status=status_value)
        appointments = appointments.order_by("start_time", "id")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(appointments, request)
        return paginator.get_paginated_response(AppointmentSerializer(page, many=True, context={"include_client": include_client}).data)

    @extend_schema(operation_id="create_appointment", request=AppointmentCreateSerializer, responses={201: AppointmentSerializer})
    def post(self, request):
        if request.user.role != User.Role.CLIENT:
            raise PermissionDenied("Only Clients may create appointments.")
        serializer = AppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(Service, id=serializer.validated_data["service_id"])
        try:
            appointment = AppointmentService().create_appointment(request.user, **serializer.validated_data)
        except ValueError as error:
            raise ValidationError({"start_time": [str(error)]}) from error
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)


class AppointmentStatusView(APIView):
    @extend_schema(operation_id="update_appointment_status", request=AppointmentStatusSerializer, responses={200: AppointmentSerializer})
    def patch(self, request, appointment_id):
        appointment = get_object_or_404(appointment_queryset(), id=appointment_id)
        serializer = AppointmentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_status = serializer.validated_data["status"]
        service = AppointmentService()
        try:
            if target_status == Appointment.Status.CONFIRMED:
                if request.user.role != User.Role.BUSINESS_OWNER:
                    raise PermissionDenied("Only Business Owners may confirm appointments.")
                appointment = service.confirm_appointment(appointment, request.user)
            else:
                appointment = service.cancel_appointment(appointment, request.user)
        except PermissionError as error:
            raise PermissionDenied(str(error)) from error
        except ValueError as error:
            raise ValidationError({"status": [str(error)]}) from error
        include_client = request.user.role == User.Role.BUSINESS_OWNER
        return Response(AppointmentSerializer(appointment, context={"include_client": include_client}).data)
