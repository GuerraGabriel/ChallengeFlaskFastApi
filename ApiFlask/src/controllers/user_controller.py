import io
from werkzeug.datastructures.file_storage import FileStorage
import csv

from src.exceptions.import_exceptions import (
    InvalidFileType,
    MissMatchColumnsError,
    NoColumnsError,
    NoFileProvided,
)


class UserAddressController:
    def __init__(self): ...

    def import_user_address(self, file: FileStorage | None):
        COLUMNS_NAME = {
            "nome",
            "nome social",
            "email",
            "idade",
            "cep",
            "numero",
            "rua",
            "bairro",
            "cidade",
            "estado",
            "país",
            "profissão",
        }
        if not file:
            raise NoFileProvided("No file provided")

        if file.content_type != "text/csv":
            raise InvalidFileType("Invalid file type received")

        csv_input = self._convert_file_to_csv(file)
        if not csv_input.fieldnames:
            raise NoColumnsError("No columns found. Is the file correctly formatted?")

        columns_received = {column.lower() for column in csv_input.fieldnames}

        if columns_received != COLUMNS_NAME:
            raise MissMatchColumnsError(
                f"Invalid columns received. Expected {COLUMNS_NAME}, got {columns_received}"
            )

        return None

    def _convert_file_to_csv(self, file: FileStorage):
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        csv_input = csv.DictReader(stream)

        return csv_input
