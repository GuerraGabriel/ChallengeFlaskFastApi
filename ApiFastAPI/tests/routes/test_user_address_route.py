from unittest import mock
import pytest
from fastapi.testclient import TestClient
from container import Container

from dependency_injector import providers
from app import app
from src.services.user_address_service import UserAddressService


@pytest.fixture(autouse=True)
def override_container():
    """Substitui o serviço no container para testes."""
    container = Container()
    container.init_resources()
    container.wire(modules=["src.routes.user_address_route"])

    mock_service = mock.AsyncMock(spec=UserAddressService)
    container.user_address_service.override(providers.Object(mock_service))

    yield mock_service

    container.unwire()
    container.shutdown_resources()


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_user_addresses_no_users_found_200_success(
    test_client, override_container
):
    expected_response = {"data": [], "message": "No users found"}
    override_container.get_users_addresses.return_value = []
    response = test_client.get("/user-addresses")

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_user_addresses_users_found_200_success(
    test_client, override_container, user_data_from_external_service
):
    expected_response = {
        "data": [user_data_from_external_service],
        "message": "Users found",
    }
    override_container.get_users_addresses.return_value = [
        user_data_from_external_service
    ]
    response = test_client.get("/user-addresses")

    assert response.status_code == 200
    assert response.json() == expected_response
