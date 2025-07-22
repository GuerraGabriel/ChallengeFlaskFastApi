import io
import pytest
from werkzeug.datastructures.file_storage import FileStorage
from unittest import mock

from src.exceptions.import_exceptions import (
    InvalidFileContentType,
    MissMatchColumnsError,
    NoColumnsError,
    NoFileProvided,
)
from src.controllers.user_controller import UserAddressController


@pytest.fixture
def controller():
    return UserAddressController()


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

    with pytest.raises(InvalidFileContentType):
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
    result = controller.import_user_address(mock_file)

    assert result is None
