import io
from typing import List
from werkzeug.datastructures.file_storage import FileStorage
import csv

from src.exceptions.user_address_exceptions import UserAlreadyExists
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

    def import_user_address(self, file: FileStorage | None) -> List[int]:
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
        rows_with_error = []

        for row_number, row in enumerate(csv_input, start=1):
            try:
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
            except UserAlreadyExists:
                rows_with_error.append(row_number)
                continue

        return rows_with_error

    def create_user_address(self, data: dict):
        user_address = UserAddressSchema.load(data)
        self.user_address_service.create_user_address(user_address)

    def _convert_file_to_csv(self, file: FileStorage):
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        csv_input = csv.DictReader(stream)

        return csv_input

    def get_users_address(self, page_size: int, page_number: int) -> dict:
        if page_size > 100:
            page_size = 100

        if page_number < 0:
            page_number = 0

        users, total_pages = self.user_address_service.get_user_addresses(
            page_size, page_number
        )
        return {
            "data": users,
            "pagination": {
                "current_page": page_number,
                "total_pages": total_pages,
                "page_size": page_size,
            },
        }
