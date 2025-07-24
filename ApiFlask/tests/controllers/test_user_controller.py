import io
import pytest
from werkzeug.datastructures.file_storage import FileStorage
from unittest import mock

from src.dtos.user_address_dto import UserAddressDTO
from src.services.user_address_service import UserAddressService
from src.exceptions.import_exceptions import (
    InvalidFileType,
    MissMatchColumnsError,
    NoColumnsError,
    NoFileProvided,
)
from src.controllers.user_controller import UserAddressController


@pytest.fixture
def controller():
    user_address_service = mock.MagicMock(spec=UserAddressService)
    return UserAddressController(user_address_service)


@pytest.fixture
def mock_file(csv_content):
    mock_file = mock.MagicMock(spec=FileStorage)
    mock_file.content_type = "text/csv"
    mock_file.stream = io.BytesIO(bytes(csv_content, encoding="utf-8"))
    return mock_file


def test_import_user_address_no_file_provided(controller, mock_file):
    with pytest.raises(NoFileProvided):
        controller.import_user_address(None)


def test_import_user_address_missmatch_content_type_error(controller, mock_file):
    mock_file.content_type = "text/plain"

    with pytest.raises(InvalidFileType):
        controller.import_user_address(mock_file)


def test_import_user_address_missmatch_columns_error(controller, mock_file):
    content = """name,cep
algo,00000000
outracoisa,0000001
"""
    mock_file.stream = io.BytesIO(bytes(content, encoding="utf-8"))
    with pytest.raises(MissMatchColumnsError):
        controller.import_user_address(mock_file)


def test_import_user_address_no_columns_error(controller, mock_file):
    content = ""
    mock_file.stream = io.BytesIO(bytes(content, encoding="utf-8"))
    with pytest.raises(NoColumnsError):
        controller.import_user_address(mock_file)


def test_import_user_address_success(controller, mock_file):
    expected_dto_called_with = UserAddressDTO(
        nome="Filomeno",
        nome_social="Astrucio",
        email="none@example.com",
        idade=99,
        cep="00000000",
        numero="100",
        rua="Rua A",
        bairro="Bairro B",
        cidade="Cidade C",
        estado="SP",
        pais="Brasil",
        profissao="Vendedor de sonhos",
    )

    result = controller.import_user_address(mock_file)

    assert controller.user_address_service.create_user_address.call_count == 2
    assert (
        expected_dto_called_with
        == controller.user_address_service.create_user_address.call_args[0][0]
    )
    assert result is None
