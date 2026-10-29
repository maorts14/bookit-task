import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User


@pytest.mark.django_db
def test_duplicate_email_is_case_insensitive(client):
    api_client = APIClient()

    response = api_client.post("/api/auth/register", {
        "email": client.email.upper(),
        "password": "A-strong-password-123",
        "full_name": "Duplicate Client",
        "role": "Client",
    }, format="json")

    assert response.status_code == 400
    assert "email" in response.data


@pytest.mark.django_db
def test_registration_rejects_weak_password():
    response = APIClient().post("/api/auth/register", {
        "email": "weak@example.com",
        "password": "12345678",
        "full_name": "Weak Password",
        "role": "Client",
    }, format="json")

    assert response.status_code == 400
    assert "password" in response.data


@pytest.mark.django_db
def test_invalid_login_does_not_disclose_whether_email_exists(client):
    api_client = APIClient()

    unknown_response = api_client.post("/api/auth/login", {"email": "unknown@example.com", "password": "wrong"}, format="json")
    wrong_password_response = api_client.post("/api/auth/login", {"email": client.email, "password": "wrong"}, format="json")

    assert unknown_response.status_code == 401
    assert wrong_password_response.status_code == 401
    assert unknown_response.data == wrong_password_response.data == {"detail": "Invalid credentials."}


@pytest.mark.django_db
def test_login_token_contains_user_id_and_role_claims(owner):
    response = APIClient().post("/api/auth/login", {"email": owner.email, "password": "BookItDemo123!"}, format="json")
    token = AccessToken(response.data["access_token"])

    assert response.status_code == 200
    assert token["user_id"] == str(owner.id)
    assert token["role"] == User.Role.BUSINESS_OWNER
