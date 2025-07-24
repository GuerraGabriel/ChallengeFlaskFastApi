import io
from werkzeug.datastructures.file_storage import FileStorage
import csv

from src.schemas.user_address_schema import UserAddressSchema
from src.services.user_address_service import UserAddressService
from src.exceptions.import_exceptions import (
    InvalidFileType,
    MissMatchColumnsError,
    NoColumnsError,
    NoFileProvided,
)


class UserAddressController:
    def __init__(self, user_address_service: UserAddressService):
        self.user_address_service = user_address_service

    def import_user_address(self, file: FileStorage | None):
        COLUMNS_NAME = [
            "Nome",
            "Nome social",
            "Email",
            "Idade",
            "CEP",
            "Número",
            "Rua",
            "Bairro",
            "Cidade",
            "Estado",
            "País",
            "Profissão",
        ]
        if not file:
            raise NoFileProvided("No file provided")

        if file.content_type != "text/csv":
            raise InvalidFileType("Invalid file type received")

        csv_input = self._convert_file_to_csv(file)
        if not csv_input.fieldnames:
            raise NoColumnsError("No columns found. Is the file correctly formatted?")

        columns_received = {column for column in csv_input.fieldnames}

        if columns_received != set(COLUMNS_NAME):
            raise MissMatchColumnsError(
                f"Invalid columns received. Expected {COLUMNS_NAME}, got {columns_received}"
            )

        for row in csv_input:
            self.create_user_address(
                {
                    "nome": row["Nome"],
                    "nome_social": row["Nome social"],
                    "email": row["Email"],
                    "idade": row["Idade"],
                    "profissao": row["Profissão"],
                    "cep": row["CEP"],
                    "numero": row["Número"],
                    "rua": row["Rua"],
                    "bairro": row["Bairro"],
                    "cidade": row["Cidade"],
                    "estado": row["Estado"],
                    "pais": row["País"],
                }
            )

        return None

    def create_user_address(self, data: dict) -> None:
        user_address = UserAddressSchema.load(data)
        self.user_address_service.create_user_address(user_address)

    def _convert_file_to_csv(self, file: FileStorage):
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        csv_input = csv.DictReader(stream)

        return csv_input
