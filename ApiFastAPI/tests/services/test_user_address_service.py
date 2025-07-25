from unittest import mock
import httpx
import pytest

from src.exceptions.external_service_exception import UnkownErrorFromExternalService
from src.schemas.user_address_schema import UserAddressExternalSchema
from src.services.user_address_service import UserAddressService


@pytest.fixture
def mock_http_client():
    return mock.AsyncMock()


@pytest.fixture
def user_address_service(mock_http_client):
    return UserAddressService(mock_http_client, "")


@pytest.mark.asyncio
async def test_get_users_from_external_service_success(
    user_address_service, mock_http_client, user_data_from_external_service
):
    expected_user = UserAddressExternalSchema(**user_data_from_external_service)
    mock_http_client.get.return_value.json = mock.MagicMock(
        return_value={
            "data": [user_data_from_external_service],
            "pagination": {
                "total_pages": 1,
                "current_page": 1,
                "page_size": 10,
            },
        }
    )
    users, total_pages = await user_address_service._get_users_from_external_service(
        page_size=10, page_number=1
    )

    assert total_pages == 1
    assert users == [expected_user]


@pytest.mark.asyncio
async def test_get_users_from_external_service_timeout(
    user_address_service, mock_http_client
):

    mock_http_client.get.side_effect = httpx.TimeoutException("message")
    with pytest.raises(httpx.TimeoutException):
        await user_address_service._get_users_from_external_service(
            page_size=10, page_number=1
        )


@pytest.mark.asyncio
async def test_get_users_from_external_service_unkown_error(
    user_address_service, mock_http_client
):

    mock_http_client.get.side_effect = httpx.ConnectError("message")
    with pytest.raises(UnkownErrorFromExternalService):
        await user_address_service._get_users_from_external_service(
            page_size=10, page_number=1
        )


@pytest.mark.asyncio
async def test_get_users_addresses_one_page_sucess(user_address_service):

    mock_get_users_from_external_service = mock.AsyncMock(
        return_value=([UserAddressExternalSchema], 1)
    )

    user_address_service._get_users_from_external_service = (
        mock_get_users_from_external_service
    )
    users = await user_address_service.get_users_addresses()

    mock_get_users_from_external_service.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_users_addresses_two_pages_sucess(user_address_service):

    expected_result = [
        {"data": "data"},
        {"data": "data"},
    ]
    mock_get_users_from_external_service = mock.AsyncMock(
        return_value=([{"data": "data"}], 2)
    )

    user_address_service._get_users_from_external_service = (
        mock_get_users_from_external_service
    )
    result = await user_address_service.get_users_addresses()

    mock_get_users_from_external_service.assert_awaited()
    assert mock_get_users_from_external_service.call_count == 2
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_users_addresses_many_pages_sucess(user_address_service):

    expected_result = [
        {"1": "data"},
        {"2": "data"},
        {"3": "data"},
        {"4": "data"},
        {"5": "data"},
    ]
    mock_get_users_from_external_service = mock.AsyncMock(
        side_effect=[
            (
                [{"1": "data"}],
                5,
            ),
            (
                [{"2": "data"}],
                5,
            ),
            (
                [{"3": "data"}],
                5,
            ),
            (
                [{"4": "data"}],
                5,
            ),
            (
                [{"5": "data"}],
                5,
            ),
        ]
    )

    user_address_service._get_users_from_external_service = (
        mock_get_users_from_external_service
    )
    result = await user_address_service.get_users_addresses()

    mock_get_users_from_external_service.assert_awaited()
    assert mock_get_users_from_external_service.call_count == 5
    assert result == expected_result
