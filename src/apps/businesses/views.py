from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.users.models import User

from .models import Business, Service
from .serializers import BusinessSerializer, BusinessSummarySerializer, BusinessWriteSerializer, ServiceSerializer, ServiceWriteSerializer
from .services import BusinessService


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


def require_owner(request):
    if request.user.role != User.Role.BUSINESS_OWNER:
        raise PermissionDenied("Only Business Owners may perform this action.")


class BusinessListCreateView(APIView):
    pagination_class = StandardPagination

    @extend_schema(
        operation_id="list_businesses",
        parameters=[
            OpenApiParameter("category", str, OpenApiParameter.QUERY),
            OpenApiParameter("search", str, OpenApiParameter.QUERY),
            OpenApiParameter("page", int, OpenApiParameter.QUERY),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY),
        ],
        responses={200: BusinessSerializer(many=True)},
    )
    def get(self, request):
        businesses = Business.objects.select_related("owner").prefetch_related("services").order_by("-created_at", "-id")
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        if category:
            businesses = businesses.filter(category__iexact=category)
        if search:
            businesses = businesses.filter(name__icontains=search)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(businesses, request)
        return paginator.get_paginated_response(BusinessSerializer(page, many=True).data)

    @extend_schema(operation_id="create_business", request=BusinessWriteSerializer, responses={201: BusinessSerializer})
    def post(self, request):
        require_owner(request)
        serializer = BusinessWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business = BusinessService().create_business(request.user, **serializer.validated_data)
        return Response(BusinessSerializer(business).data, status=status.HTTP_201_CREATED)


class BusinessDetailView(APIView):
    def get_object(self, business_id):
        return get_object_or_404(Business.objects.prefetch_related("services"), id=business_id)

    @extend_schema(operation_id="get_business", responses={200: BusinessSerializer})
    def get(self, request, business_id):
        return Response(BusinessSerializer(self.get_object(business_id)).data)

    @extend_schema(operation_id="update_business", request=BusinessWriteSerializer, responses={200: BusinessSerializer})
    def patch(self, request, business_id):
        require_owner(request)
        business = self.get_object(business_id)
        if business.owner_id != request.user.id:
            raise PermissionDenied("You do not own this business.")
        serializer = BusinessWriteSerializer(business, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(BusinessSerializer(business).data)

    @extend_schema(operation_id="delete_business", responses={204: None})
    def delete(self, request, business_id):
        require_owner(request)
        business = self.get_object(business_id)
        if business.owner_id != request.user.id:
            raise PermissionDenied("You do not own this business.")
        business.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceCreateView(APIView):
    @extend_schema(operation_id="create_service", request=ServiceWriteSerializer, responses={201: ServiceSerializer})
    def post(self, request, business_id):
        require_owner(request)
        business = get_object_or_404(Business, id=business_id)
        if business.owner_id != request.user.id:
            raise PermissionDenied("You do not own this business.")
        serializer = ServiceWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = BusinessService().create_service(business, **serializer.validated_data)
        return Response(ServiceSerializer(service).data, status=status.HTTP_201_CREATED)


class ServiceDetailView(APIView):
    def get_object(self, service_id):
        return get_object_or_404(Service.objects.select_related("business"), id=service_id)

    @extend_schema(operation_id="update_service", request=ServiceWriteSerializer, responses={200: ServiceSerializer})
    def patch(self, request, service_id):
        require_owner(request)
        service = self.get_object(service_id)
        if service.business.owner_id != request.user.id:
            raise PermissionDenied("You do not own this service.")
        serializer = ServiceWriteSerializer(service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ServiceSerializer(service).data)

    @extend_schema(operation_id="delete_service", responses={204: None})
    def delete(self, request, service_id):
        require_owner(request)
        service = self.get_object(service_id)
        if service.business.owner_id != request.user.id:
            raise PermissionDenied("You do not own this service.")
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessSummaryView(APIView):
    @extend_schema(operation_id="business_summary", responses={200: BusinessSummarySerializer(many=True)})
    def get(self, request, business_id):
        require_owner(request)
        business = get_object_or_404(Business, id=business_id)
        if business.owner_id != request.user.id:
            raise PermissionDenied("You do not own this business.")
        services = BusinessService().service_summary(business)
        return Response([
            {
                "service_id": service.id,
                "service_name": service.name,
                "upcoming_appointments_count": service.upcoming_appointments_count,
                "expected_revenue": f"{service.expected_revenue:.2f}",
            }
            for service in services
        ])
