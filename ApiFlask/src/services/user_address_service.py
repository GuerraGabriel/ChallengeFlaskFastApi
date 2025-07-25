from typing import List, Tuple
from src.exceptions.user_address_exceptions import UserAlreadyExists
from src.dtos.user_address_dto import UserAddressDTO
from src.models.address import Address
from src.models.user import User
from src.repositories.user_address_repository import UserAddressRepository
from sqlalchemy.exc import IntegrityError


class UserAddressService:
    def __init__(self, user_address_repository: UserAddressRepository):
        self.user_address_repository = user_address_repository

    def create_user_address(self, user_address: UserAddressDTO) -> None:
        address = Address(
            cep=user_address.cep,
            number=user_address.numero,
            street=user_address.rua,
            neighborhood=user_address.bairro,
            city=user_address.cidade,
            state=user_address.estado,
            country=user_address.pais,
        )
        user = User(
            name=user_address.nome,
            preferred_name=user_address.nome_social,
            email=user_address.email,
            age=user_address.idade,
            occupation=user_address.profissao,
            address=address,
        )
        try:
            self.user_address_repository.create(user)
        except IntegrityError as e:
            raise UserAlreadyExists("User already exists") from e
        except Exception as e:
            raise ValueError(f"Failed to create user address: {e}") from e

    def get_user_addresses(
        self,
        page_size: int,
        page_number: int,
    ) -> Tuple[List[UserAddressDTO], int]:
        users_addresses, total_pages = self.user_address_repository.get_users_paginated(
            page_size, page_number
        )
        user_address_dto = [
            UserAddressDTO(
                nome=user.name,
                nome_social=user.preferred_name,
                email=user.email,
                idade=user.age,
                cep=user.address.cep,
                numero=user.address.number,
                rua=user.address.street,
                bairro=user.address.neighborhood,
                cidade=user.address.city,
                estado=user.address.state,
                pais=user.address.country,
                profissao=user.occupation,
            )
            for user in users_addresses
        ]

        return user_address_dto, total_pages
