import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_register_and_login_user(async_client):
    register_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    response = await async_client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == register_data["email"]
    assert "id" in data

    login_data = {
        "username": "testuser@example.com",
        "password": "password123"
    }
    response = await async_client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

async def test_create_product_unauthorized(async_client):
    product_data = {
        "title": "Test Laptop",
        "description": "Gaming laptop",
        "price": 1200.00,
        "stock": 10
    }
    response = await async_client.post("/api/v1/products", json=product_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_get_products_list_public(async_client):
    response = await async_client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)