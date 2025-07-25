import io
from unittest import mock
import pytest
from app import create_app
from container import Container
from src.exceptions.import_exceptions import (
    NoFileProvided,
    InvalidFileType,
    MissMatchColumnsError,
    NoColumnsError,
)
from sqlalchemy.exc import DatabaseError


@pytest.fixture
def mock_get_users_address():
    return mock.MagicMock()


@pytest.fixture
def mock_import_user_address():
    return mock.MagicMock()


@pytest.fixture
def mock_container(mock_import_user_address, mock_get_users_address):
    container_mock = mock.MagicMock(spec=Container)
    container_mock.user_address_controller.return_value.import_user_address = (
        mock_import_user_address
    )
    container_mock.user_address_controller.return_value.get_users_address = (
        mock_get_users_address
    )
    return container_mock


@pytest.fixture
def client(mock_container):
    app = create_app()
    app.testing = True
    app.container = mock_container
    return app.test_client()


@pytest.fixture
def mock_data(csv_content):
    data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test_users.csv")}
    return data


def test_import_user_address_success_201(client, mock_data, mock_import_user_address):
    mock_import_user_address.return_value = []
    expected_response = {"message": "User addresses imported successfully"}
    response = client.post(
        "/users/import-address", data=mock_data, content_type="multipart/form-data"
    )
    assert response.status_code == 201
    assert response.json == expected_response


def test_import_user_address_no_file_400(client, mock_container):
    error_message = "error message"
    mock_container.user_address_controller.return_value.import_user_address.side_effect = NoFileProvided(
        error_message
    )
    response = client.post("/users/import-address")
    assert response.status_code == 400
    assert response.json["error"] == error_message


def test_import_user_address_invalid_file_type_400(client, mock_container):
    error_message = "error message"

    mock_container.user_address_controller.return_value.import_user_address.side_effect = InvalidFileType(
        error_message
    )
    response = client.post("/users/import-address")
    assert response.status_code == 400
    assert response.json["error"] == error_message


def test_import_user_address_columns_mismatch_400(client, mock_container):
    error_message = "error message"

    mock_container.user_address_controller.return_value.import_user_address.side_effect = MissMatchColumnsError(
        error_message
    )
    response = client.post("/users/import-address")
    assert response.status_code == 400
    assert response.json["error"] == error_message


def test_import_user_address_empty_file_400(client, mock_container):
    error_message = "error message"
    mock_container.user_address_controller.return_value.import_user_address.side_effect = NoColumnsError(
        error_message
    )
    response = client.post("/users/import-address")
    assert response.status_code == 400
    assert response.json["error"] == error_message


@pytest.mark.parametrize(
    "side_effect_error", [Exception, ValueError, KeyError, DatabaseError]
)
def test_import_user_address_random_error_500(
    side_effect_error, client, mock_container
):
    expected_response = {
        "error": "Unexpected error. Try again later or contact support."
    }
    mock_container.user_address_controller.return_value.import_user_address.side_effect = (
        side_effect_error
    )
    response = client.post("/users/import-address")
    assert response.status_code == 500
    assert response.json == expected_response


def test_import_user_address_partial_success_207(
    client, mock_data, mock_import_user_address
):
    mock_import_user_address.return_value = [1]
    expected_response = {
        "message": "User addresses partial imported",
        "rows_with_errors": [1],
    }
    response = client.post(
        "/users/import-address", data=mock_data, content_type="multipart/form-data"
    )
    assert response.status_code == 207
    assert response.json == expected_response


def test_get_addresses_success(client, mock_get_users_address):
    mock_get_users_address.return_value = {
        "data": [
            {
                "bairro": "Neighborhood",
                "cep": "12345-678",
                "cidade": "City",
                "email": "test@example.com",
                "estado": "State",
                "idade": None,
                "nome": "John Doe",
                "nome_social": None,
                "numero": "123",
                "pais": "Country",
                "profissao": None,
                "rua": "Main St",
            }
        ],
        "page": {"current_page": 1, "page_size": 10, "total_pages": 1},
    }
    response = client.get("/users/addresses")
    assert response.status_code == 200
