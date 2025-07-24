import pytest
from unittest.mock import MagicMock

from src.services.user_address_service import UserAddressService
from src.schemas.user_address_schema import UserAddressSchema
from src.dtos.user_address_dto import UserAddressDTO


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    return UserAddressService(user_address_repository=mock_repository)


@pytest.fixture
def user_address_dto():
    data = {
        "nome": "Gabriel",
        "nome_social": "Gabe",
        "email": "gabe@example.com",
        "idade": 30,
        "profissao": "Developer",
        "cep": "12345678",
        "numero": "100",
        "rua": "Rua A",
        "bairro": "Bairro B",
        "cidade": "Cidade C",
        "estado": "SP",
        "pais": "Brasil",
    }
    return UserAddressSchema.load(data)


def test_create_user_address_success(service, mock_repository, user_address_dto):

    result = service.create_user_address(user_address_dto)

    assert mock_repository.create.call_count == 1

    called_user = mock_repository.create.call_args[0][0]

    assert called_user.email == "gabe@example.com"
    assert called_user.address.cep == "12345678"

    assert result is None


def test_create_user_address_failure(service, mock_repository, user_address_dto):

    mock_repository.create.side_effect = Exception("DB error")

    with pytest.raises(ValueError) as exc_info:
        service.create_user_address(user_address_dto)

    assert "Failed to create user address" in str(exc_info.value)
