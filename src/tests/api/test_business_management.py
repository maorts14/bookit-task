import pytest
from rest_framework.test import APIClient

from apps.appointments.models import Appointment
from apps.businesses.models import Business, Service


@pytest.mark.django_db
def test_business_list_combines_case_insensitive_category_and_name_search(client, owner):
    matching = Business.objects.create(owner=owner, name="Dana Hair Studio", category="Barber")
    Business.objects.create(owner=owner, name="Dana Physio", category="Physiotherapy")
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.get("/api/businesses?category=barber&search=hair")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == str(matching.id)


@pytest.mark.django_db
def test_authenticated_client_can_read_business_detail_with_services(service, client):
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.get(f"/api/businesses/{service.business_id}")

    assert response.status_code == 200
    assert response.data["services"][0]["id"] == str(service.id)


@pytest.mark.django_db
def test_business_owner_can_create_update_and_delete_owned_business(owner):
    api_client = APIClient()
    api_client.force_authenticate(owner)

    create_response = api_client.post("/api/businesses", {"name": "New Studio", "category": "Barber"}, format="json")
    business_id = create_response.data["id"]
    update_response = api_client.patch(f"/api/businesses/{business_id}", {"category": "Salon"}, format="json")
    delete_response = api_client.delete(f"/api/businesses/{business_id}")

    assert create_response.status_code == 201
    assert update_response.status_code == 200
    assert update_response.data["category"] == "Salon"
    assert delete_response.status_code == 204
    assert not Business.objects.filter(id=business_id).exists()


@pytest.mark.django_db
def test_owner_cannot_modify_another_owners_business(service, other_owner):
    api_client = APIClient()
    api_client.force_authenticate(other_owner)

    response = api_client.patch(f"/api/businesses/{service.business_id}", {"name": "Stolen Studio"}, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_client_cannot_create_business(client):
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.post("/api/businesses", {"name": "Client Studio", "category": "Barber"}, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_deleting_service_cascades_to_its_appointments(service, owner, client, future_time):
    appointment = Appointment.objects.create(service=service, client=client, start_time=future_time)
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.delete(f"/api/services/{service.id}")

    assert response.status_code == 204
    assert not Service.objects.filter(id=service.id).exists()
    assert not Appointment.objects.filter(id=appointment.id).exists()


@pytest.mark.django_db
def test_service_validation_rejects_zero_duration_and_negative_price(service, owner):
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.patch(f"/api/services/{service.id}", {"duration_minutes": 0, "price": "-1.00"}, format="json")

    assert response.status_code == 400
    assert "duration_minutes" in response.data
    assert "price" in response.data


@pytest.mark.django_db
def test_owner_can_create_service_but_other_owner_cannot(service, owner, other_owner):
    api_client = APIClient()
    api_client.force_authenticate(owner)

    create_response = api_client.post(f"/api/businesses/{service.business_id}/services", {
        "name": "Beard trim with Dana",
        "duration_minutes": 20,
        "price": "25.00",
    }, format="json")
    api_client.force_authenticate(other_owner)
    forbidden_response = api_client.post(f"/api/businesses/{service.business_id}/services", {
        "name": "Unauthorized service",
        "duration_minutes": 20,
        "price": "25.00",
    }, format="json")

    assert create_response.status_code == 201
    assert forbidden_response.status_code == 403


@pytest.mark.django_db
def test_deleting_business_cascades_services_and_appointments(service, owner, client, future_time):
    appointment = Appointment.objects.create(service=service, client=client, start_time=future_time)
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.delete(f"/api/businesses/{service.business_id}")

    assert response.status_code == 204
    assert not Business.objects.filter(id=service.business_id).exists()
    assert not Service.objects.filter(id=service.id).exists()
    assert not Appointment.objects.filter(id=appointment.id).exists()
